import json
import logging
from datetime import datetime, timezone

from ingest_recomart_to_s3 import ingest_recomart_files
from ingest_external_api_to_s3 import ingest_external_products


def setup_logger() -> logging.Logger:
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

    pipeline_result = {
        "pipeline_name": "recomart_raw_data_ingestion",
        "pipeline_start_time": pipeline_start_time,
        "pipeline_end_time": datetime.now(timezone.utc).isoformat(),
        "recomart_csv_ingestion": recomart_result,
        "external_api_ingestion": external_api_result,
    }

    logger.info("RecoMart ingestion pipeline completed")
    logger.info(json.dumps(pipeline_result, indent=2))


if __name__ == "__main__":
    main()