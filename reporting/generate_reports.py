import os
import json
import logging
from pathlib import Path
from datetime import datetime, timezone
from typing import Any

import pandas as pd
import snowflake.connector
from dotenv import load_dotenv


load_dotenv()


REPORTS_DIR = Path("reports")
EXPORTS_DIR = REPORTS_DIR / "exports"


def setup_logger() -> logging.Logger:
    os.makedirs("logs", exist_ok=True)

    logger = logging.getLogger("recomart_report_generator")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        file_handler = logging.FileHandler("logs/reporting.log")
        console_handler = logging.StreamHandler()

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )

        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger


def get_snowflake_connection():
    return snowflake.connector.connect(
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        role=os.getenv("SNOWFLAKE_ROLE", "ACCOUNTADMIN"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH"),
        database=os.getenv("SNOWFLAKE_DATABASE", "RECOMART_DB"),
    )


def ensure_report_dirs() -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)


def run_query(cursor, query: str) -> pd.DataFrame:
    cursor.execute(query)
    rows = cursor.fetchall()

    if cursor.description is None:
        return pd.DataFrame()

    columns = [col[0] for col in cursor.description]
    return pd.DataFrame(rows, columns=columns)


def safe_query(cursor, query: str, logger: logging.Logger, report_name: str) -> pd.DataFrame:
    try:
        return run_query(cursor, query)
    except Exception as error:
        logger.error(f"Failed query for {report_name}: {error}")
        return pd.DataFrame({"ERROR": [str(error)]})


def dataframe_to_markdown(df: pd.DataFrame) -> str:
    if df.empty:
        return "_No records found._"

    return df.to_markdown(index=False)


def save_export(df: pd.DataFrame, export_name: str) -> str:
    export_path = EXPORTS_DIR / f"{export_name}.csv"
    df.to_csv(export_path, index=False)
    return str(export_path)


def write_report(file_name: str, content: str) -> str:
    report_path = REPORTS_DIR / file_name
    report_path.write_text(content)
    return str(report_path)


def report_header(title: str) -> str:
    generated_ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    return f"""# {title}

**Generated At:** {generated_ts}

**Project:** RecoMart Recommendation Data Pipeline

---
"""


def section(title: str, df: pd.DataFrame, export_name: str) -> str:
    export_path = save_export(df, export_name)

    return f"""## {title}

**CSV Export:** `{export_path}`

{dataframe_to_markdown(df)}

---
"""


def generate_data_quality_report(cursor, logger: logging.Logger) -> str:
    report_name = "data_quality_report"

    dq_summary = safe_query(
        cursor,
        """
        SELECT
            BATCH_ID AS VALIDATION_BATCH_ID,
            STATUS,
            COUNT(*) AS RULE_COUNT,
            MIN(EXECUTED_TS) AS FIRST_RULE_EXECUTED_TS,
            MAX(EXECUTED_TS) AS LAST_RULE_EXECUTED_TS
        FROM OPS.DATA_QUALITY_RESULTS
        GROUP BY BATCH_ID, STATUS
        ORDER BY FIRST_RULE_EXECUTED_TS DESC
        """,
        logger,
        report_name,
    )

    dq_details = safe_query(
        cursor,
        """
        SELECT
            BATCH_ID AS VALIDATION_BATCH_ID,
            RULE_ID,
            TARGET_TABLE,
            TOTAL_RECORDS,
            FAILED_RECORDS,
            PASSED_RECORDS,
            FAILURE_PERCENTAGE,
            STATUS,
            MESSAGE,
            EXECUTED_TS
        FROM OPS.DATA_QUALITY_RESULTS
        ORDER BY EXECUTED_TS DESC, RULE_ID
        """,
        logger,
        report_name,
    )

    event_validity = safe_query(
        cursor,
        """
        SELECT
            VALIDATION_BATCH_ID,
            VALIDATION_RUN_TS,
            IS_VALID,
            VALIDATION_MESSAGE,
            COUNT(*) AS RECORD_COUNT
        FROM VALIDATED.RECOMART_EVENTS
        GROUP BY
            VALIDATION_BATCH_ID,
            VALIDATION_RUN_TS,
            IS_VALID,
            VALIDATION_MESSAGE
        ORDER BY VALIDATION_RUN_TS DESC, RECORD_COUNT DESC
        """,
        logger,
        report_name,
    )

    content = report_header("Data Quality Report")
    content += section("Data Quality Summary", dq_summary, "dq_summary")
    content += section("Detailed Data Quality Results", dq_details, "dq_details")
    content += section("Validated Event Quality", event_validity, "validated_event_quality")

    return write_report("data_quality_report.md", content)


def generate_eda_report(cursor, logger: logging.Logger) -> str:
    report_name = "eda_report"

    clean_summary = safe_query(
        cursor,
        """
        SELECT
            COUNT(*) AS TOTAL_EVENTS,
            COUNT(DISTINCT USER_ID) AS UNIQUE_USERS,
            COUNT(DISTINCT ITEM_ID) AS UNIQUE_ITEMS,
            MIN(EVENT_TS) AS FIRST_EVENT_TS,
            MAX(EVENT_TS) AS LAST_EVENT_TS
        FROM CURATED.CLEAN_RECOMART_EVENTS
        """,
        logger,
        report_name,
    )

    event_distribution = safe_query(
        cursor,
        """
        SELECT
            EVENT_TYPE,
            COUNT(*) AS EVENT_COUNT,
            ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS EVENT_PERCENTAGE
        FROM CURATED.CLEAN_RECOMART_EVENTS
        GROUP BY EVENT_TYPE
        ORDER BY EVENT_COUNT DESC
        """,
        logger,
        report_name,
    )

    top_products = safe_query(
        cursor,
        """
        SELECT
            ITEM_ID,
            TOTAL_VIEWS,
            TOTAL_ADD_TO_CARTS,
            TOTAL_TRANSACTIONS,
            ITEM_POPULARITY_SCORE,
            CONVERSION_RATE
        FROM CURATED.ITEM_FEATURES
        ORDER BY ITEM_POPULARITY_SCORE DESC
        LIMIT 20
        """,
        logger,
        report_name,
    )

    sparsity = safe_query(
        cursor,
        """
        WITH counts AS (
            SELECT
                COUNT(DISTINCT USER_ID) AS USER_COUNT,
                COUNT(DISTINCT ITEM_ID) AS ITEM_COUNT,
                COUNT(*) AS OBSERVED_INTERACTIONS
            FROM CURATED.USER_ITEM_INTERACTIONS
        )
        SELECT
            USER_COUNT,
            ITEM_COUNT,
            OBSERVED_INTERACTIONS,
            USER_COUNT * ITEM_COUNT AS POSSIBLE_INTERACTIONS,
            ROUND(
                1 - OBSERVED_INTERACTIONS / NULLIF(USER_COUNT * ITEM_COUNT, 0),
                6
            ) AS SPARSITY_RATIO
        FROM counts
        """,
        logger,
        report_name,
    )

    content = report_header("Data Preparation and EDA Report")
    content += section("Clean Event Summary", clean_summary, "eda_clean_event_summary")
    content += section("Event Type Distribution", event_distribution, "eda_event_distribution")
    content += section("Top 20 Popular Products", top_products, "eda_top_products")
    content += section("User-Item Matrix Sparsity", sparsity, "eda_user_item_sparsity")

    return write_report("eda_report.md", content)


def generate_feature_engineering_report(cursor, logger: logging.Logger) -> str:
    report_name = "feature_engineering_report"

    feature_counts = safe_query(
        cursor,
        """
        SELECT 'FE_USER_ACTIVITY' AS FEATURE_TABLE, COUNT(*) AS ROW_COUNT FROM CURATED.FE_USER_ACTIVITY
        UNION ALL
        SELECT 'FE_ITEM_POPULARITY' AS FEATURE_TABLE, COUNT(*) AS ROW_COUNT FROM CURATED.FE_ITEM_POPULARITY
        UNION ALL
        SELECT 'FE_USER_CATEGORY_AFFINITY' AS FEATURE_TABLE, COUNT(*) AS ROW_COUNT FROM CURATED.FE_USER_CATEGORY_AFFINITY
        UNION ALL
        SELECT 'FE_ITEM_CO_OCCURRENCE' AS FEATURE_TABLE, COUNT(*) AS ROW_COUNT FROM CURATED.FE_ITEM_CO_OCCURRENCE
        UNION ALL
        SELECT 'FE_ITEM_SIMILARITY' AS FEATURE_TABLE, COUNT(*) AS ROW_COUNT FROM CURATED.FE_ITEM_SIMILARITY
        UNION ALL
        SELECT 'RECOMMENDATION_TRAINING_DATASET' AS FEATURE_TABLE, COUNT(*) AS ROW_COUNT FROM CURATED.RECOMMENDATION_TRAINING_DATASET
        """,
        logger,
        report_name,
    )

    top_similarity = safe_query(
        cursor,
        """
        SELECT
            ITEM_ID,
            SIMILAR_ITEM_ID,
            CO_INTERACTION_USERS,
            COSINE_SIMILARITY_SCORE,
            FEATURE_VERSION,
            SOURCE_VALIDATION_BATCH_ID
        FROM CURATED.FE_ITEM_SIMILARITY
        ORDER BY COSINE_SIMILARITY_SCORE DESC
        LIMIT 20
        """,
        logger,
        report_name,
    )

    training_sample = safe_query(
        cursor,
        """
        SELECT
            USER_ID,
            ITEM_ID,
            USER_TOTAL_VIEWS,
            USER_TOTAL_TRANSACTIONS,
            ITEM_POPULARITY_SCORE,
            USER_ITEM_IMPLICIT_SCORE,
            TARGET_LABEL,
            FEATURE_VERSION,
            SOURCE_VALIDATION_BATCH_ID
        FROM CURATED.RECOMMENDATION_TRAINING_DATASET
        LIMIT 20
        """,
        logger,
        report_name,
    )

    content = report_header("Feature Engineering and Transformation Report")
    content += section("Feature Table Row Counts", feature_counts, "feature_table_counts")
    content += section("Top Item Similarity Features", top_similarity, "top_item_similarity")
    content += section("Training Dataset Sample", training_sample, "training_dataset_sample")

    return write_report("feature_engineering_report.md", content)


def generate_feature_store_report(cursor, logger: logging.Logger) -> str:
    report_name = "feature_store_report"

    registry_summary = safe_query(
        cursor,
        """
        SELECT
            FEATURE_GROUP,
            ENTITY_TYPE,
            FEATURE_VERSION,
            COUNT(*) AS FEATURE_COUNT
        FROM FEATURE_STORE.FEATURE_REGISTRY
        WHERE IS_ACTIVE = TRUE
        GROUP BY FEATURE_GROUP, ENTITY_TYPE, FEATURE_VERSION
        ORDER BY FEATURE_GROUP, ENTITY_TYPE
        """,
        logger,
        report_name,
    )

    offline_summary = safe_query(
        cursor,
        """
        SELECT
            FEATURE_VERSION,
            SOURCE_VALIDATION_BATCH_ID,
            COUNT(*) AS OFFLINE_FEATURE_ROWS,
            MIN(FEATURE_PUBLISHED_TS) AS FIRST_PUBLISHED_TS,
            MAX(FEATURE_PUBLISHED_TS) AS LAST_PUBLISHED_TS
        FROM FEATURE_STORE.OFFLINE_RECOMMENDATION_FEATURES
        GROUP BY FEATURE_VERSION, SOURCE_VALIDATION_BATCH_ID
        ORDER BY LAST_PUBLISHED_TS DESC
        """,
        logger,
        report_name,
    )

    online_sample = safe_query(
        cursor,
        """
        SELECT
            USER_ID,
            ITEM_ID,
            USER_ACTIVITY_LEVEL,
            ITEM_POPULARITY_SCORE,
            ITEM_CONVERSION_RATE,
            USER_ITEM_IMPLICIT_SCORE,
            RECOMMENDATION_CANDIDATE_SCORE,
            FEATURE_VERSION,
            SOURCE_VALIDATION_BATCH_ID
        FROM FEATURE_STORE.ONLINE_RECOMMENDATION_FEATURES
        ORDER BY RECOMMENDATION_CANDIDATE_SCORE DESC
        LIMIT 20
        """,
        logger,
        report_name,
    )

    retrieval_log = safe_query(
        cursor,
        """
        SELECT
            REQUEST_ID,
            USER_ID,
            ITEM_ID,
            FEATURE_VERSION,
            SOURCE_VALIDATION_BATCH_ID,
            REQUEST_TYPE,
            REQUEST_TS,
            STATUS,
            MESSAGE
        FROM FEATURE_STORE.FEATURE_RETRIEVAL_LOG
        ORDER BY REQUEST_TS DESC
        LIMIT 20
        """,
        logger,
        report_name,
    )

    content = report_header("Feature Store Report")
    content += section("Feature Registry Summary", registry_summary, "feature_registry_summary")
    content += section("Offline Feature Store Summary", offline_summary, "offline_feature_store_summary")
    content += section("Online Feature Sample", online_sample, "online_feature_sample")
    content += section("Feature Retrieval Logs", retrieval_log, "feature_retrieval_logs")

    return write_report("feature_store_report.md", content)


def generate_lineage_report(cursor, logger: logging.Logger) -> str:
    report_name = "lineage_report"

    dataset_versions = safe_query(
        cursor,
        """
        SELECT
            DATASET_NAME,
            SOURCE_TYPE,
            LOCAL_PATH,
            S3_RAW_PATH,
            TARGET_TABLE,
            FILE_SIZE_BYTES,
            ROW_COUNT,
            SHA256_HASH,
            VERSIONING_TOOL,
            VERSION_STATUS,
            MANIFEST_CREATED_TS,
            REGISTERED_TS
        FROM OPS.DATASET_VERSION_REGISTRY
        ORDER BY REGISTERED_TS DESC
        """,
        logger,
        report_name,
    )

    lineage_flow = safe_query(
        cursor,
        """
        SELECT
            BATCH_ID,
            SOURCE_LAYER,
            SOURCE_OBJECT,
            TARGET_LAYER,
            TARGET_OBJECT,
            TRANSFORMATION_NAME,
            TRANSFORMATION_TYPE,
            TRANSFORMATION_LOGIC,
            STATUS,
            CREATED_TS
        FROM OPS.DATA_LINEAGE
        ORDER BY CREATED_TS
        """,
        logger,
        report_name,
    )

    content = report_header("Data Versioning and Lineage Report")
    content += section("Dataset Version Registry", dataset_versions, "dataset_version_registry")
    content += section("Pipeline Lineage Flow", lineage_flow, "pipeline_lineage_flow")

    return write_report("lineage_report.md", content)


def generate_model_performance_report(cursor, logger: logging.Logger) -> str:
    report_name = "model_performance_report"

    model_runs = safe_query(
        cursor,
        """
        SELECT
            RUN_ID,
            MODEL_NAME,
            MODEL_VERSION,
            MODEL_TYPE,
            TRAINING_STATUS,
            FEATURE_VERSION,
            SOURCE_VALIDATION_BATCH_ID,
            MODEL_ARTIFACT_PATH,
            MLFLOW_RUN_ID,
            TRAINING_START_TS,
            TRAINING_END_TS,
            CREATED_TS
        FROM ML_MONITORING.MODEL_RUNS
        ORDER BY CREATED_TS DESC
        LIMIT 10
        """,
        logger,
        report_name,
    )

    model_metrics = safe_query(
        cursor,
        """
        SELECT
            RUN_ID,
            MODEL_NAME,
            MODEL_VERSION,
            METRIC_NAME,
            METRIC_VALUE,
            K_VALUE,
            FEATURE_VERSION,
            SOURCE_VALIDATION_BATCH_ID,
            EVALUATION_DATE,
            CREATED_TS
        FROM ML_MONITORING.MODEL_METRICS
        ORDER BY CREATED_TS DESC, METRIC_NAME
        LIMIT 100
        """,
        logger,
        report_name,
    )

    recommendations = safe_query(
        cursor,
        """
        SELECT
            REQUEST_ID,
            USER_ID,
            ITEM_ID,
            RANK_POSITION,
            RECOMMENDATION_SCORE,
            MODEL_NAME,
            MODEL_VERSION,
            FEATURE_VERSION,
            SOURCE_VALIDATION_BATCH_ID,
            GENERATED_TS
        FROM ML_MONITORING.RECOMMENDATION_RESULTS
        ORDER BY GENERATED_TS DESC, USER_ID, RANK_POSITION
        LIMIT 50
        """,
        logger,
        report_name,
    )

    content = report_header("Model Performance Report")
    content += section("Latest Model Runs", model_runs, "latest_model_runs")
    content += section("Model Metrics", model_metrics, "model_metrics")
    content += section("Sample Recommendation Results", recommendations, "sample_recommendation_results")

    return write_report("model_performance_report.md", content)


def generate_orchestration_report(logger: logging.Logger) -> str:
    airflow_log_dir = Path("logs/airflow")

    log_files = [
        "recomart_airflow_dag_success.log",
        "01_check_environment.log",
        "02_ingestion_and_raw_load.log",
        "04_validation.log",
        "05_preparation.log",
        "06_feature_engineering.log",
        "07_feature_store.log",
        "08_lineage.log",
        "09_model_training.log",
        "10_final_health_check.log",
    ]

    rows: list[dict[str, Any]] = []

    for log_file in log_files:
        path = airflow_log_dir / log_file

        if path.exists():
            content = path.read_text(errors="ignore")
            status = "SUCCESS" if "exit code 0" in content or "SUCCESS" in content else "CHECK_LOG"
            rows.append(
                {
                    "LOG_FILE": str(path),
                    "STATUS": status,
                    "SIZE_BYTES": path.stat().st_size,
                    "LAST_MODIFIED": datetime.fromtimestamp(path.stat().st_mtime).isoformat(),
                }
            )
        else:
            rows.append(
                {
                    "LOG_FILE": str(path),
                    "STATUS": "MISSING",
                    "SIZE_BYTES": 0,
                    "LAST_MODIFIED": None,
                }
            )

    orchestration_df = pd.DataFrame(rows)

    content = report_header("Pipeline Orchestration Report")
    content += section("Airflow Execution Logs", orchestration_df, "airflow_execution_logs")
    content += """
## Orchestration Summary

The RecoMart pipeline is orchestrated using Apache Airflow CLI mode. The DAG executes ingestion, raw Snowflake loading, validation, data preparation, feature engineering, feature store publishing, lineage tracking, model training, and final health checks.

The execution logs stored under `logs/airflow/` are used as orchestration evidence for the assignment submission.

---
"""

    return write_report("orchestration_report.md", content)


def generate_report_index(report_paths: list[str]) -> str:
    generated_ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    lines = [
        "# RecoMart Report Index",
        "",
        f"**Generated At:** {generated_ts}",
        "",
        "| Report | Path |",
        "|---|---|",
    ]

    for path in report_paths:
        report_file = Path(path)
        lines.append(f"| {report_file.stem.replace('_', ' ').title()} | `{path}` |")

    lines.extend(
        [
            "",
            "## Exported CSV Files",
            "",
            "Detailed query outputs are stored under:",
            "",
            "`reports/exports/`",
            "",
        ]
    )

    content = "\n".join(lines)
    return write_report("report_index.md", content)


def display_report_summary(report_paths: list[str]) -> None:
    print("\nRecoMart Reports Generated")
    print("=" * 60)

    for path in report_paths:
        print(f"- {path}")

    print("=" * 60)
    print("Detailed CSV exports are available under reports/exports/")


def main() -> None:
    logger = setup_logger()
    ensure_report_dirs()

    logger.info("Starting RecoMart report generation")

    report_paths: list[str] = []

    connection = None

    try:
        connection = get_snowflake_connection()
        cursor = connection.cursor()

        report_paths.append(generate_data_quality_report(cursor, logger))
        report_paths.append(generate_eda_report(cursor, logger))
        report_paths.append(generate_feature_engineering_report(cursor, logger))
        report_paths.append(generate_feature_store_report(cursor, logger))
        report_paths.append(generate_lineage_report(cursor, logger))
        report_paths.append(generate_model_performance_report(cursor, logger))
        report_paths.append(generate_orchestration_report(logger))

        report_paths.append(generate_report_index(report_paths))

        display_report_summary(report_paths)

        logger.info("RecoMart report generation completed successfully")

    except Exception as error:
        logger.error(f"Report generation failed: {error}")
        raise

    finally:
        if connection:
            connection.close()
            logger.info("Snowflake connection closed")


if __name__ == "__main__":
    main()