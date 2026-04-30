import os
import uuid
import yaml
import boto3
import logging
from datetime import datetime, timezone
from botocore.exceptions import ClientError
from dotenv import load_dotenv


load_dotenv()


def setup_logger() -> logging.Logger:
    os.makedirs("logs", exist_ok=True)

    logger = logging.getLogger("recomart_csv_ingestion")
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


def load_config(config_path: str = "config/config.yaml") -> dict:
    with open(config_path, "r") as file:
        return yaml.safe_load(file)


def get_ingestion_date() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def upload_file_to_s3(
    s3_client,
    bucket_name: str,
    local_file_path: str,
    s3_key: str,
    logger: logging.Logger,
) -> None:
    try:
        if not os.path.exists(local_file_path):
            raise FileNotFoundError(f"File not found: {local_file_path}")

        logger.info(f"Uploading {local_file_path} to s3://{bucket_name}/{s3_key}")

        s3_client.upload_file(
            Filename=local_file_path,
            Bucket=bucket_name,
            Key=s3_key,
        )

        logger.info(f"Upload successful: s3://{bucket_name}/{s3_key}")

    except FileNotFoundError as error:
        logger.error(f"Local file missing: {error}")
        raise

    except ClientError as error:
        logger.error(f"AWS S3 upload failed for {local_file_path}: {error}")
        raise

    except Exception as error:
        logger.error(f"Unexpected error while uploading {local_file_path}: {error}")
        raise


def ingest_recomart_files() -> dict:
    logger = setup_logger()
    config = load_config()

    batch_id = str(uuid.uuid4())
    ingestion_date = get_ingestion_date()

    bucket_name = config["aws"]["s3_bucket"]

    s3_client = boto3.client(
        "s3",
        region_name=config["aws"]["region"],
    )

    file_mappings = [
        {
            "source_name": "events",
            "local_path": config["local_paths"]["events"],
            "s3_prefix": config["s3_paths"]["events"],
            "target_file_name": "events.csv",
        },
        {
            "source_name": "item_properties_part1",
            "local_path": config["local_paths"]["item_properties_part1"],
            "s3_prefix": config["s3_paths"]["item_properties"],
            "target_file_name": "item_properties_part1.csv",
        },
        {
            "source_name": "item_properties_part2",
            "local_path": config["local_paths"]["item_properties_part2"],
            "s3_prefix": config["s3_paths"]["item_properties"],
            "target_file_name": "item_properties_part2.csv",
        },
        {
            "source_name": "category_tree",
            "local_path": config["local_paths"]["category_tree"],
            "s3_prefix": config["s3_paths"]["category_tree"],
            "target_file_name": "category_tree.csv",
        },
    ]

    results = {
        "batch_id": batch_id,
        "ingestion_date": ingestion_date,
        "status": "SUCCESS",
        "uploaded_files": [],
        "failed_files": [],
    }

    logger.info(f"Starting RecoMart CSV ingestion. batch_id={batch_id}")

    for mapping in file_mappings:
        s3_key = (
            f"{mapping['s3_prefix']}/"
            f"ingestion_date={ingestion_date}/"
            f"{mapping['target_file_name']}"
        )

        try:
            upload_file_to_s3(
                s3_client=s3_client,
                bucket_name=bucket_name,
                local_file_path=mapping["local_path"],
                s3_key=s3_key,
                logger=logger,
            )

            results["uploaded_files"].append(
                {
                    "source_name": mapping["source_name"],
                    "local_path": mapping["local_path"],
                    "s3_path": f"s3://{bucket_name}/{s3_key}",
                }
            )

        except Exception as error:
            results["status"] = "PARTIAL_FAILURE"
            results["failed_files"].append(
                {
                    "source_name": mapping["source_name"],
                    "local_path": mapping["local_path"],
                    "error": str(error),
                }
            )

    logger.info(f"RecoMart CSV ingestion completed with status={results['status']}")

    return results


if __name__ == "__main__":
    output = ingest_recomart_files()
    print(output)