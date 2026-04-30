import os
import sys
import json
import logging
from pathlib import Path
from datetime import datetime, timezone

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from ingestion.ingest_recomart_to_s3 import ingest_recomart_files
from ingestion.ingest_external_api_to_s3 import ingest_external_products
from snowflake_load.load_raw_from_s3 import load_raw_from_s3


def setup_logger() -> logging.Logger:
    os.makedirs("logs", exist_ok=True)

    logger = logging.getLogger("run_ingestion")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        file_handler = logging.FileHandler("logs/ingestion.log")
        console_handler = logging.StreamHandler()

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )

        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger


def main() -> None:
    logger = setup_logger()

    pipeline_start_time = datetime.now(timezone.utc).isoformat()

    logger.info("Starting RecoMart ingestion pipeline")

    recomart_result = ingest_recomart_files()
    external_api_result = ingest_external_products()

    if recomart_result["status"] not in ("SUCCESS", "PARTIAL_FAILURE"):
        raise RuntimeError("RecoMart CSV ingestion failed before Snowflake RAW load")

    if external_api_result["status"] != "SUCCESS":
        raise RuntimeError("External API ingestion failed before Snowflake RAW load")

    logger.info("S3 upload completed. Starting automated S3 to Snowflake RAW load.")

    load_raw_from_s3()

    pipeline_result = {
        "pipeline_name": "recomart_raw_data_ingestion_and_snowflake_load",
        "pipeline_start_time": pipeline_start_time,
        "pipeline_end_time": datetime.now(timezone.utc).isoformat(),
        "recomart_csv_ingestion": recomart_result,
        "external_api_ingestion": external_api_result,
        "snowflake_raw_load": "SUCCESS",
    }

    logger.info("RecoMart ingestion + Snowflake RAW load pipeline completed")
    logger.info(json.dumps(pipeline_result, indent=2))


if __name__ == "__main__":
    main()