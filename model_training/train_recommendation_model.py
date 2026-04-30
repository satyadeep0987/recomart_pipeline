import os
import json
import uuid
import yaml
import joblib
import logging
from pathlib import Path
from datetime import datetime, timezone

import numpy as np
import pandas as pd
import mlflow
import snowflake.connector

from tqdm.auto import tqdm
from dotenv import load_dotenv
from scipy.sparse import csr_matrix
from sklearn.decomposition import TruncatedSVD


load_dotenv()


def setup_logger() -> logging.Logger:
    os.makedirs("logs", exist_ok=True)

    logger = logging.getLogger("recomart_model_training")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        file_handler = logging.FileHandler("logs/model_training.log")
        console_handler = logging.StreamHandler()

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )

        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger


def load_config(config_path: str = "model_training/config.yaml") -> dict:
    with open(config_path, "r") as file:
        return yaml.safe_load(file)


def utc_now_string() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")


def get_snowflake_connection():
    return snowflake.connector.connect(
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        role=os.getenv("SNOWFLAKE_ROLE", "ACCOUNTADMIN"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE", "RECOMART_WH"),
        database=os.getenv("SNOWFLAKE_DATABASE", "RECOMART_DB"),
    )


def execute_sql_file(cursor, sql_file_path: str) -> None:
    path = Path(sql_file_path)

    if not path.exists():
        raise FileNotFoundError(f"SQL file not found: {sql_file_path}")

    sql_text = path.read_text()

    for statement in sql_text.split(";"):
        cleaned_statement = statement.strip()

        if cleaned_statement:
            cursor.execute(cleaned_statement)


def get_latest_feature_batch(cursor, feature_version: str) -> str:
    cursor.execute(
        """
        SELECT SOURCE_VALIDATION_BATCH_ID
        FROM FEATURE_STORE.OFFLINE_RECOMMENDATION_FEATURES
        WHERE FEATURE_VERSION = %(feature_version)s
          AND SOURCE_VALIDATION_BATCH_ID IS NOT NULL
        ORDER BY FEATURE_PUBLISHED_TS DESC
        LIMIT 1
        """,
        {"feature_version": feature_version},
    )

    result = cursor.fetchone()

    if not result or not result[0]:
        raise ValueError(
            "No feature batch found in FEATURE_STORE.OFFLINE_RECOMMENDATION_FEATURES."
        )

    return result[0]


def load_training_data(
    cursor,
    config: dict,
    source_validation_batch_id: str,
) -> pd.DataFrame:
    feature_version = config["training"]["feature_version"]
    min_user_interactions = int(config["training"]["min_user_interactions"])
    max_users = int(config["training"]["max_users"])
    max_items = int(config["training"]["max_items"])
    max_training_rows = int(config["training"]["max_training_rows"])

    query = f"""
    WITH user_rank AS (
        SELECT
            USER_ID,
            COUNT(*) AS INTERACTION_COUNT,
            SUM(USER_ITEM_IMPLICIT_SCORE) AS TOTAL_SCORE
        FROM FEATURE_STORE.OFFLINE_RECOMMENDATION_FEATURES
        WHERE FEATURE_VERSION = %(feature_version)s
          AND SOURCE_VALIDATION_BATCH_ID = %(source_validation_batch_id)s
        GROUP BY USER_ID
        HAVING COUNT(*) >= %(min_user_interactions)s
        ORDER BY TOTAL_SCORE DESC
        LIMIT {max_users}
    ),
    item_rank AS (
        SELECT
            ITEM_ID,
            COUNT(*) AS INTERACTION_COUNT,
            SUM(USER_ITEM_IMPLICIT_SCORE) AS TOTAL_SCORE
        FROM FEATURE_STORE.OFFLINE_RECOMMENDATION_FEATURES
        WHERE FEATURE_VERSION = %(feature_version)s
          AND SOURCE_VALIDATION_BATCH_ID = %(source_validation_batch_id)s
        GROUP BY ITEM_ID
        ORDER BY TOTAL_SCORE DESC
        LIMIT {max_items}
    )
    SELECT
        f.USER_ID,
        f.ITEM_ID,
        f.USER_ITEM_IMPLICIT_SCORE,
        f.TARGET_LABEL
    FROM FEATURE_STORE.OFFLINE_RECOMMENDATION_FEATURES f
    INNER JOIN user_rank u
        ON f.USER_ID = u.USER_ID
    INNER JOIN item_rank i
        ON f.ITEM_ID = i.ITEM_ID
    WHERE f.FEATURE_VERSION = %(feature_version)s
      AND f.SOURCE_VALIDATION_BATCH_ID = %(source_validation_batch_id)s
      AND f.USER_ITEM_IMPLICIT_SCORE > 0
    ORDER BY f.USER_ITEM_IMPLICIT_SCORE DESC
    LIMIT {max_training_rows}
    """

    cursor.execute(
        query,
        {
            "feature_version": feature_version,
            "source_validation_batch_id": source_validation_batch_id,
            "min_user_interactions": min_user_interactions,
        },
    )

    rows = cursor.fetchall()
    columns = [column[0].lower() for column in cursor.description]

    return pd.DataFrame(rows, columns=columns)


def train_test_split_by_user(
    df: pd.DataFrame,
    random_state: int,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    rng = np.random.default_rng(random_state)
    test_indices = []

    for _, group in df.groupby("user_id"):
        if len(group) >= 2:
            selected_index = rng.choice(group.index.to_numpy(), size=1)[0]
            test_indices.append(selected_index)

    test_df = df.loc[test_indices].copy()
    train_df = df.drop(index=test_indices).copy()

    return train_df, test_df


def build_interaction_matrix(train_df: pd.DataFrame):
    user_ids = sorted(train_df["user_id"].unique())
    item_ids = sorted(train_df["item_id"].unique())

    user_to_index = {user_id: index for index, user_id in enumerate(user_ids)}
    item_to_index = {item_id: index for index, item_id in enumerate(item_ids)}

    index_to_user = {index: user_id for user_id, index in user_to_index.items()}
    index_to_item = {index: item_id for item_id, index in item_to_index.items()}

    row_indices = train_df["user_id"].map(user_to_index).to_numpy()
    col_indices = train_df["item_id"].map(item_to_index).to_numpy()
    values = train_df["user_item_implicit_score"].astype(float).to_numpy()

    interaction_matrix = csr_matrix(
        (values, (row_indices, col_indices)),
        shape=(len(user_ids), len(item_ids)),
    )

    return interaction_matrix, user_to_index, item_to_index, index_to_user, index_to_item


def evaluate_model(
    train_matrix,
    user_factors: np.ndarray,
    item_factors: np.ndarray,
    test_df: pd.DataFrame,
    user_to_index: dict,
    item_to_index: dict,
    top_k: int,
) -> dict:
    hits = 0
    total_precision = 0.0
    total_recall = 0.0
    total_ndcg = 0.0
    evaluated_users = 0

    test_grouped = test_df.groupby("user_id")["item_id"].apply(set).to_dict()

    for user_id, relevant_items in tqdm(
        test_grouped.items(),
        total=len(test_grouped),
        desc=f"Evaluating Precision/Recall/NDCG@{top_k}",
        unit="user",
    ):
        if user_id not in user_to_index:
            continue

        relevant_item_indices = {
            item_to_index[item_id]
            for item_id in relevant_items
            if item_id in item_to_index
        }

        if not relevant_item_indices:
            continue

        user_index = user_to_index[user_id]
        scores = user_factors[user_index].dot(item_factors.T)

        known_items = train_matrix[user_index].indices
        scores[known_items] = -np.inf

        k = min(top_k, len(scores))

        top_item_indices = np.argpartition(-scores, k - 1)[:k]
        top_item_indices = top_item_indices[np.argsort(-scores[top_item_indices])]

        hit_positions = [
            rank + 1
            for rank, item_index in enumerate(top_item_indices)
            if item_index in relevant_item_indices
        ]

        user_hits = len(hit_positions)

        hits += user_hits
        total_precision += user_hits / top_k
        total_recall += user_hits / len(relevant_item_indices)

        if hit_positions:
            dcg = sum(1.0 / np.log2(position + 1) for position in hit_positions)
            ideal_hits = min(len(relevant_item_indices), top_k)
            idcg = sum(
                1.0 / np.log2(position + 1)
                for position in range(1, ideal_hits + 1)
            )
            total_ndcg += dcg / idcg
        else:
            total_ndcg += 0.0

        evaluated_users += 1

    if evaluated_users == 0:
        return {
            "precision_at_k": 0.0,
            "recall_at_k": 0.0,
            "ndcg_at_k": 0.0,
            "hit_rate_at_k": 0.0,
            "evaluated_users": 0,
        }

    return {
        "precision_at_k": total_precision / evaluated_users,
        "recall_at_k": total_recall / evaluated_users,
        "ndcg_at_k": total_ndcg / evaluated_users,
        "hit_rate_at_k": hits / evaluated_users,
        "evaluated_users": evaluated_users,
    }


def generate_sample_recommendations(
    train_matrix,
    user_factors: np.ndarray,
    item_factors: np.ndarray,
    index_to_user: dict,
    index_to_item: dict,
    top_k: int,
    max_users: int = 100,
) -> pd.DataFrame:
    recommendation_rows = []
    total_users = min(max_users, user_factors.shape[0])

    for user_index in tqdm(
        range(total_users),
        desc="Generating sample recommendations",
        unit="user",
    ):
        scores = user_factors[user_index].dot(item_factors.T)

        known_items = train_matrix[user_index].indices
        scores[known_items] = -np.inf

        k = min(top_k, len(scores))

        top_item_indices = np.argpartition(-scores, k - 1)[:k]
        top_item_indices = top_item_indices[np.argsort(-scores[top_item_indices])]

        for rank, item_index in enumerate(top_item_indices, start=1):
            recommendation_rows.append(
                {
                    "user_id": index_to_user[user_index],
                    "item_id": index_to_item[item_index],
                    "rank_position": rank,
                    "recommendation_score": float(scores[item_index]),
                }
            )

    return pd.DataFrame(recommendation_rows)


def insert_model_run(
    cursor,
    run_id: str,
    mlflow_run_id: str,
    config: dict,
    source_validation_batch_id: str,
    training_start_ts: str,
    training_end_ts: str,
    parameters: dict,
    metrics: dict,
    artifact_path: str,
) -> None:
    cursor.execute(
        """
        INSERT INTO ML_MONITORING.MODEL_RUNS (
            RUN_ID,
            MODEL_NAME,
            MODEL_VERSION,
            MODEL_TYPE,
            TRAINING_START_TS,
            TRAINING_END_TS,
            TRAINING_STATUS,
            TRAINING_DATASET,
            FEATURE_VERSION,
            SOURCE_VALIDATION_BATCH_ID,
            PARAMETERS,
            METRICS,
            MODEL_ARTIFACT_PATH,
            MLFLOW_RUN_ID
        )
        SELECT
            %(run_id)s,
            %(model_name)s,
            %(model_version)s,
            %(model_type)s,
            %(training_start_ts)s,
            %(training_end_ts)s,
            'SUCCESS',
            'FEATURE_STORE.OFFLINE_RECOMMENDATION_FEATURES',
            %(feature_version)s,
            %(source_validation_batch_id)s,
            PARSE_JSON(%(parameters_json)s),
            PARSE_JSON(%(metrics_json)s),
            %(artifact_path)s,
            %(mlflow_run_id)s
        """,
        {
            "run_id": run_id,
            "model_name": config["model"]["name"],
            "model_version": config["model"]["version"],
            "model_type": config["model"]["type"],
            "training_start_ts": training_start_ts,
            "training_end_ts": training_end_ts,
            "feature_version": config["training"]["feature_version"],
            "source_validation_batch_id": source_validation_batch_id,
            "parameters_json": json.dumps(parameters),
            "metrics_json": json.dumps(metrics),
            "artifact_path": artifact_path,
            "mlflow_run_id": mlflow_run_id,
        },
    )


def insert_model_metrics(
    cursor,
    run_id: str,
    config: dict,
    source_validation_batch_id: str,
    metrics: dict,
) -> None:
    metric_rows = [
        ("precision_at_k", metrics["precision_at_k"]),
        ("recall_at_k", metrics["recall_at_k"]),
        ("ndcg_at_k", metrics["ndcg_at_k"]),
        ("hit_rate_at_k", metrics["hit_rate_at_k"]),
        ("evaluated_users", metrics["evaluated_users"]),
    ]

    insert_sql = """
    INSERT INTO ML_MONITORING.MODEL_METRICS (
        RUN_ID,
        MODEL_NAME,
        MODEL_VERSION,
        METRIC_NAME,
        METRIC_VALUE,
        K_VALUE,
        FEATURE_VERSION,
        SOURCE_VALIDATION_BATCH_ID,
        EVALUATION_DATE
    )
    VALUES (
        %(run_id)s,
        %(model_name)s,
        %(model_version)s,
        %(metric_name)s,
        %(metric_value)s,
        %(k_value)s,
        %(feature_version)s,
        %(source_validation_batch_id)s,
        CURRENT_DATE()
    )
    """

    payload = [
        {
            "run_id": run_id,
            "model_name": config["model"]["name"],
            "model_version": config["model"]["version"],
            "metric_name": metric_name,
            "metric_value": float(metric_value),
            "k_value": config["model"]["top_k"],
            "feature_version": config["training"]["feature_version"],
            "source_validation_batch_id": source_validation_batch_id,
        }
        for metric_name, metric_value in metric_rows
    ]

    cursor.executemany(insert_sql, payload)


def insert_sample_recommendations(
    cursor,
    recommendations_df: pd.DataFrame,
    config: dict,
    source_validation_batch_id: str,
) -> None:
    request_id = str(uuid.uuid4())

    insert_sql = """
    INSERT INTO ML_MONITORING.RECOMMENDATION_RESULTS (
        REQUEST_ID,
        USER_ID,
        ITEM_ID,
        RANK_POSITION,
        RECOMMENDATION_SCORE,
        MODEL_NAME,
        MODEL_VERSION,
        FEATURE_VERSION,
        SOURCE_VALIDATION_BATCH_ID
    )
    VALUES (
        %(request_id)s,
        %(user_id)s,
        %(item_id)s,
        %(rank_position)s,
        %(recommendation_score)s,
        %(model_name)s,
        %(model_version)s,
        %(feature_version)s,
        %(source_validation_batch_id)s
    )
    """

    payload = []

    for row in tqdm(
        recommendations_df.itertuples(index=False),
        total=len(recommendations_df),
        desc="Preparing recommendation insert payload",
        unit="row",
    ):
        payload.append(
            {
                "request_id": request_id,
                "user_id": int(row.user_id),
                "item_id": int(row.item_id),
                "rank_position": int(row.rank_position),
                "recommendation_score": float(row.recommendation_score),
                "model_name": config["model"]["name"],
                "model_version": config["model"]["version"],
                "feature_version": config["training"]["feature_version"],
                "source_validation_batch_id": source_validation_batch_id,
            }
        )

    if payload:
        cursor.executemany(insert_sql, payload)


def write_model_report(
    config: dict,
    run_id: str,
    source_validation_batch_id: str,
    metrics: dict,
    parameters: dict,
    artifact_path: str,
) -> None:
    report_path = Path(config["artifacts"]["report_path"])
    report_path.parent.mkdir(parents=True, exist_ok=True)

    top_k = parameters["top_k"]

    content = f"""# Model Performance Report

## Model Summary

| Field | Value |
|---|---|
| Model Name | {config["model"]["name"]} |
| Model Version | {config["model"]["version"]} |
| Model Type | {config["model"]["type"]} |
| Run ID | {run_id} |
| Source Validation Batch ID | {source_validation_batch_id} |
| Feature Version | {config["training"]["feature_version"]} |
| Model Artifact Path | {artifact_path} |

## Parameters

| Parameter | Value |
|---|---|
| n_components | {parameters["n_components"]} |
| top_k | {parameters["top_k"]} |
| random_state | {parameters["random_state"]} |
| train_rows | {parameters["train_rows"]} |
| test_rows | {parameters["test_rows"]} |
| users | {parameters["users"]} |
| items | {parameters["items"]} |

## Evaluation Metrics

| Metric | Value |
|---|---|
| Precision@{top_k} | {metrics["precision_at_k"]:.6f} |
| Recall@{top_k} | {metrics["recall_at_k"]:.6f} |
| NDCG@{top_k} | {metrics["ndcg_at_k"]:.6f} |
| Hit Rate@{top_k} | {metrics["hit_rate_at_k"]:.6f} |
| Evaluated Users | {metrics["evaluated_users"]} |

## Interpretation

RecoMart uses a collaborative filtering model based on Matrix Factorization using Truncated SVD.

The source dataset contains implicit user behavior. Therefore, user actions are converted into weighted scores:

- Product view = 1
- Add to cart = 3
- Transaction = 5

The model learns latent user and item representations from the user-item interaction matrix and generates top-K product recommendations based on predicted affinity scores.
"""

    report_path.write_text(content)


def main() -> None:
    logger = setup_logger()
    config = load_config()

    run_id = str(uuid.uuid4())
    training_start_ts = utc_now_string()

    logger.info(f"Starting model training. run_id={run_id}")

    connection = None

    try:
        with tqdm(
            total=12,
            desc="RecoMart model training pipeline",
            unit="step",
        ) as progress:
            progress.set_description("Connecting to Snowflake")
            connection = get_snowflake_connection()
            cursor = connection.cursor()
            progress.update(1)

            progress.set_description("Creating model tracking objects")
            execute_sql_file(
                cursor,
                "sql/model_training/00_create_model_tracking_objects.sql",
            )
            progress.update(1)

            progress.set_description("Finding latest feature batch")
            source_validation_batch_id = get_latest_feature_batch(
                cursor,
                config["training"]["feature_version"],
            )
            logger.info(f"Using source_validation_batch_id={source_validation_batch_id}")
            progress.update(1)

            progress.set_description("Loading training data")
            df = load_training_data(cursor, config, source_validation_batch_id)

            if df.empty:
                raise ValueError(
                    "Training dataset is empty. Check FEATURE_STORE.OFFLINE_RECOMMENDATION_FEATURES."
                )

            logger.info(f"Loaded training rows: {len(df)}")
            progress.update(1)

            progress.set_description("Splitting train/test data")
            train_df, test_df = train_test_split_by_user(
                df,
                random_state=config["model"]["random_state"],
            )

            if train_df.empty or test_df.empty:
                raise ValueError(
                    "Train or test dataset is empty. Increase dataset size or lower min_user_interactions."
                )

            progress.update(1)

            progress.set_description("Building user-item matrix")
            (
                train_matrix,
                user_to_index,
                item_to_index,
                index_to_user,
                index_to_item,
            ) = build_interaction_matrix(train_df)

            progress.update(1)

            progress.set_description("Training SVD model")
            n_components = min(
                config["model"]["n_components"],
                max(1, min(train_matrix.shape) - 1),
            )

            svd = TruncatedSVD(
                n_components=n_components,
                random_state=config["model"]["random_state"],
            )

            user_factors = svd.fit_transform(train_matrix)
            item_factors = svd.components_.T

            progress.update(1)

            progress.set_description("Evaluating model")
            metrics = evaluate_model(
                train_matrix=train_matrix,
                user_factors=user_factors,
                item_factors=item_factors,
                test_df=test_df,
                user_to_index=user_to_index,
                item_to_index=item_to_index,
                top_k=config["model"]["top_k"],
            )

            progress.update(1)

            progress.set_description("Saving model artifact")
            parameters = {
                "n_components": int(n_components),
                "top_k": int(config["model"]["top_k"]),
                "random_state": int(config["model"]["random_state"]),
                "train_rows": int(len(train_df)),
                "test_rows": int(len(test_df)),
                "users": int(train_matrix.shape[0]),
                "items": int(train_matrix.shape[1]),
            }

            model_dir = Path(config["artifacts"]["model_dir"])
            model_dir.mkdir(parents=True, exist_ok=True)

            artifact_path = model_dir / f"{config['model']['name']}_{run_id}.joblib"

            model_bundle = {
                "model": svd,
                "user_to_index": user_to_index,
                "item_to_index": item_to_index,
                "index_to_user": index_to_user,
                "index_to_item": index_to_item,
                "config": config,
                "metrics": metrics,
                "parameters": parameters,
                "source_validation_batch_id": source_validation_batch_id,
            }

            joblib.dump(model_bundle, artifact_path)

            progress.update(1)

            progress.set_description("Generating recommendations")
            recommendations_df = generate_sample_recommendations(
                train_matrix=train_matrix,
                user_factors=user_factors,
                item_factors=item_factors,
                index_to_user=index_to_user,
                index_to_item=index_to_item,
                top_k=config["model"]["top_k"],
                max_users=int(config["training"]["recommendation_sample_users"]),
            )

            recommendation_artifact_path = (
                model_dir / f"sample_recommendations_{run_id}.csv"
            )
            recommendations_df.to_csv(recommendation_artifact_path, index=False)

            progress.update(1)

            progress.set_description("Writing model report")
            write_model_report(
                config=config,
                run_id=run_id,
                source_validation_batch_id=source_validation_batch_id,
                metrics=metrics,
                parameters=parameters,
                artifact_path=str(artifact_path),
            )

            progress.update(1)

            progress.set_description("Logging to MLflow")
            mlflow.set_tracking_uri(config["mlflow"]["tracking_uri"])
            mlflow.set_experiment(config["mlflow"]["experiment_name"])

            with mlflow.start_run(
                run_name=f"{config['model']['name']}_{run_id}"
            ) as mlflow_run:
                mlflow_run_id = mlflow_run.info.run_id

                mlflow.log_params(parameters)
                mlflow.log_metrics(metrics)
                mlflow.log_artifact(str(artifact_path))
                mlflow.log_artifact(str(recommendation_artifact_path))
                mlflow.log_artifact(config["artifacts"]["report_path"])

            progress.update(1)

            progress.set_description("Writing metadata to Snowflake")
            training_end_ts = utc_now_string()

            insert_model_run(
                cursor=cursor,
                run_id=run_id,
                mlflow_run_id=mlflow_run_id,
                config=config,
                source_validation_batch_id=source_validation_batch_id,
                training_start_ts=training_start_ts,
                training_end_ts=training_end_ts,
                parameters=parameters,
                metrics=metrics,
                artifact_path=str(artifact_path),
            )

            insert_model_metrics(
                cursor=cursor,
                run_id=run_id,
                config=config,
                source_validation_batch_id=source_validation_batch_id,
                metrics=metrics,
            )

            insert_sample_recommendations(
                cursor=cursor,
                recommendations_df=recommendations_df,
                config=config,
                source_validation_batch_id=source_validation_batch_id,
            )

            progress.update(1)
            progress.set_description("Model training completed")

        logger.info(f"Model training completed successfully. run_id={run_id}")
        logger.info(f"Metrics: {json.dumps(metrics, indent=2)}")

    except Exception as error:
        logger.error(f"Model training failed. run_id={run_id}. Error: {error}")
        raise

    finally:
        if connection:
            connection.close()
            logger.info("Snowflake connection closed")


if __name__ == "__main__":
    main()