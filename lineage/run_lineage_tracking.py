import os
import json
import logging
import uuid
from pathlib import Path
from dotenv import load_dotenv
import snowflake.connector


load_dotenv()


MANIFEST_PATH = "data/metadata/dataset_version_manifest.json"


def setup_logger() -> logging.Logger:
    os.makedirs("logs", exist_ok=True)

    logger = logging.getLogger("recomart_lineage")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        file_handler = logging.FileHandler("logs/lineage.log")
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
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE", "RECOMART_WH"),
        database=os.getenv("SNOWFLAKE_DATABASE", "RECOMART_DB"),
    )


def load_manifest() -> dict:
    path = Path(MANIFEST_PATH)

    if not path.exists():
        raise FileNotFoundError(f"Manifest file not found: {MANIFEST_PATH}")

    with open(path, "r") as file:
        return json.load(file)


def create_objects(cursor) -> None:
    sql_path = Path("sql/lineage/00_create_lineage_objects.sql")
    sql_text = sql_path.read_text()

    for statement in sql_text.split(";"):
        if statement.strip():
            cursor.execute(statement.strip())


def register_dataset_versions(cursor, manifest: dict, logger: logging.Logger) -> None:
    versioning_tool = manifest["versioning_tool"]
    dvc_remote = manifest["dvc_remote"]
    manifest_created_ts = manifest["manifest_created_ts"]

    for dataset in manifest["datasets"]:
        dataset_version_id = f"{dataset['dataset_name']}::{dataset['sha256_hash']}"

        cursor.execute(
            """
            INSERT INTO OPS.DATASET_VERSION_REGISTRY (
                DATASET_VERSION_ID,
                DATASET_NAME,
                SOURCE_TYPE,
                LOCAL_PATH,
                S3_RAW_PATH,
                TARGET_TABLE,
                DVC_REMOTE_PATH,
                FILE_SIZE_BYTES,
                ROW_COUNT,
                SHA256_HASH,
                VERSIONING_TOOL,
                VERSION_STATUS,
                MANIFEST_CREATED_TS
            )
            SELECT
                %(dataset_version_id)s,
                %(dataset_name)s,
                %(source_type)s,
                %(local_path)s,
                %(s3_raw_path)s,
                %(target_table)s,
                %(dvc_remote_path)s,
                %(file_size_bytes)s,
                %(row_count)s,
                %(sha256_hash)s,
                %(versioning_tool)s,
                %(version_status)s,
                %(manifest_created_ts)s
            WHERE NOT EXISTS (
                SELECT 1
                FROM OPS.DATASET_VERSION_REGISTRY
                WHERE DATASET_VERSION_ID = %(dataset_version_id)s
            )
            """,
            {
                "dataset_version_id": dataset_version_id,
                "dataset_name": dataset["dataset_name"],
                "source_type": dataset["source_type"],
                "local_path": dataset["local_path"],
                "s3_raw_path": dataset["s3_raw_path"],
                "target_table": dataset["target_table"],
                "dvc_remote_path": dvc_remote,
                "file_size_bytes": dataset["file_size_bytes"],
                "row_count": dataset["row_count"],
                "sha256_hash": dataset["sha256_hash"],
                "versioning_tool": versioning_tool,
                "version_status": dataset["status"],
                "manifest_created_ts": manifest_created_ts,
            },
        )

        logger.info(f"Registered dataset version: {dataset_version_id}")


def get_latest_batch_id(cursor) -> str:
    batch_queries = [
        """
        SELECT SOURCE_VALIDATION_BATCH_ID
        FROM FEATURE_STORE.OFFLINE_RECOMMENDATION_FEATURES
        WHERE SOURCE_VALIDATION_BATCH_ID IS NOT NULL
        ORDER BY FEATURE_PUBLISHED_TS DESC
        LIMIT 1
        """,
        """
        SELECT SOURCE_VALIDATION_BATCH_ID
        FROM CURATED.RECOMMENDATION_TRAINING_DATASET
        WHERE SOURCE_VALIDATION_BATCH_ID IS NOT NULL
        ORDER BY FEATURE_RUN_TS DESC
        LIMIT 1
        """,
        """
        SELECT VALIDATION_BATCH_ID
        FROM VALIDATED.RECOMART_EVENTS
        WHERE VALIDATION_BATCH_ID IS NOT NULL
        ORDER BY VALIDATION_RUN_TS DESC
        LIMIT 1
        """,
        """
        SELECT BATCH_ID
        FROM RAW.RAW_RECOMART_EVENTS
        WHERE BATCH_ID IS NOT NULL
        ORDER BY LOAD_TS DESC
        LIMIT 1
        """
    ]

    for query in batch_queries:
        cursor.execute(query)
        result = cursor.fetchone()

        if result and result[0]:
            return result[0]

    raise ValueError("No valid batch ID found from feature store, curated, validated, or raw tables.")


def insert_pipeline_lineage(cursor, logger: logging.Logger) -> None:
    latest_batch_id = get_latest_batch_id(cursor)

    logger.info(f"Using latest batch id for lineage: {latest_batch_id}")

    lineage_rows = [
        {
            "lineage_id": str(uuid.uuid4()),
            "batch_id": latest_batch_id,
            "source": "s3://recomartdatalake/raw/",
            "target": "RECOMART_DB.RAW",
            "name": "s3_to_raw_load",
            "type": "COPY_INTO",
            "logic": "Load RecoMart CSV and JSON files from S3 into Snowflake RAW schema",
            "source_layer": "S3_RAW",
            "target_layer": "SNOWFLAKE_RAW",
        },
        {
            "lineage_id": str(uuid.uuid4()),
            "batch_id": latest_batch_id,
            "source": "RECOMART_DB.RAW",
            "target": "RECOMART_DB.VALIDATED",
            "name": "raw_to_validated",
            "type": "VALIDATION",
            "logic": "Apply null checks, duplicate checks, event type checks, validation flags, validation batch ID, and validation timestamp",
            "source_layer": "SNOWFLAKE_RAW",
            "target_layer": "SNOWFLAKE_VALIDATED",
        },
        {
            "lineage_id": str(uuid.uuid4()),
            "batch_id": latest_batch_id,
            "source": "RECOMART_DB.VALIDATED",
            "target": "RECOMART_DB.CURATED",
            "name": "validated_to_curated_preparation",
            "type": "CLEANING_PREPARATION",
            "logic": "Clean valid records, transform timestamps, encode event types, normalize values, and create user-item interactions",
            "source_layer": "SNOWFLAKE_VALIDATED",
            "target_layer": "SNOWFLAKE_CURATED",
        },
        {
            "lineage_id": str(uuid.uuid4()),
            "batch_id": latest_batch_id,
            "source": "RECOMART_DB.CURATED",
            "target": "RECOMART_DB.CURATED feature tables",
            "name": "curated_to_feature_engineering",
            "type": "FEATURE_ENGINEERING",
            "logic": "Create user activity, item popularity, category affinity, co-occurrence, item similarity, and training dataset features",
            "source_layer": "SNOWFLAKE_CURATED",
            "target_layer": "SNOWFLAKE_FEATURES",
        },
        {
            "lineage_id": str(uuid.uuid4()),
            "batch_id": latest_batch_id,
            "source": "RECOMART_DB.CURATED.RECOMMENDATION_TRAINING_DATASET",
            "target": "RECOMART_DB.FEATURE_STORE",
            "name": "feature_publish",
            "type": "FEATURE_STORE_PUBLISH",
            "logic": "Publish offline and online recommendation features with feature version and source validation batch ID",
            "source_layer": "SNOWFLAKE_FEATURES",
            "target_layer": "SNOWFLAKE_FEATURE_STORE",
        },
    ]

    for row in lineage_rows:
        cursor.execute(
            """
            INSERT INTO OPS.DATA_LINEAGE (
                LINEAGE_ID,
                BATCH_ID,
                SOURCE_OBJECT,
                TARGET_OBJECT,
                TRANSFORMATION_NAME,
                TRANSFORMATION_TYPE,
                TRANSFORMATION_LOGIC,
                SOURCE_LAYER,
                TARGET_LAYER,
                START_TS,
                END_TS,
                STATUS
            )
            VALUES (
                %(lineage_id)s,
                %(batch_id)s,
                %(source)s,
                %(target)s,
                %(name)s,
                %(type)s,
                %(logic)s,
                %(source_layer)s,
                %(target_layer)s,
                CURRENT_TIMESTAMP(),
                CURRENT_TIMESTAMP(),
                'SUCCESS'
            )
            """,
            row,
        )

        logger.info(f"Inserted lineage step: {row['name']}")

        
def main() -> None:
    logger = setup_logger()
    logger.info("Starting RecoMart data versioning and lineage tracking")

    connection = None

    try:
        manifest = load_manifest()

        connection = get_snowflake_connection()
        cursor = connection.cursor()

        create_objects(cursor)
        register_dataset_versions(cursor, manifest, logger)
        insert_pipeline_lineage(cursor, logger)

        logger.info("RecoMart lineage tracking completed successfully")

    except Exception as error:
        logger.error(f"Lineage tracking failed: {error}")
        raise

    finally:
        if connection:
            connection.close()
            logger.info("Snowflake connection closed")


if __name__ == "__main__":
    main()