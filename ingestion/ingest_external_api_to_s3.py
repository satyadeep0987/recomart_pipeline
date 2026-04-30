import os
import json
import uuid
import yaml
import boto3
import logging
import requests
from datetime import datetime, timezone
from botocore.exceptions import ClientError
from dotenv import load_dotenv


load_dotenv()


def setup_logger() -> logging.Logger:
    os.makedirs("logs", exist_ok=True)

    logger = logging.getLogger("external_api_ingestion")
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


def fetch_products_from_api(api_url: str, limit: int, logger: logging.Logger) -> dict:
    try:
        params = {"limit": limit}

        logger.info(f"Fetching external product data from API: {api_url}")

        response = requests.get(
            api_url,
            params=params,
            timeout=30,
        )

        response.raise_for_status()

        logger.info("External API fetch successful")

        return response.json()

    except requests.exceptions.Timeout as error:
        logger.error(f"External API request timed out: {error}")
        raise

    except requests.exceptions.HTTPError as error:
        logger.error(f"External API HTTP error: {error}")
        raise

    except requests.exceptions.RequestException as error:
        logger.error(f"External API request failed: {error}")
        raise


def upload_json_to_s3(
    s3_client,
    bucket_name: str,
    s3_key: str,
    payload: dict,
    logger: logging.Logger,
) -> None:
    try:
        logger.info(f"Uploading external API JSON to s3://{bucket_name}/{s3_key}")

        s3_client.put_object(
            Bucket=bucket_name,
            Key=s3_key,
            Body=json.dumps(payload, indent=2),
            ContentType="application/json",
        )

        logger.info(f"Upload successful: s3://{bucket_name}/{s3_key}")

    except ClientError as error:
        logger.error(f"AWS S3 JSON upload failed: {error}")
        raise

    except Exception as error:
        logger.error(f"Unexpected error while uploading API data: {error}")
        raise


def ingest_external_products() -> dict:
    logger = setup_logger()
    config = load_config()

    batch_id = str(uuid.uuid4())
    ingestion_date = get_ingestion_date()

    bucket_name = config["aws"]["s3_bucket"]
    api_url = config["external_api"]["products_url"]
    limit = config["external_api"]["limit"]

    s3_key = (
        f"{config['s3_paths']['external_products']}/"
        f"ingestion_date={ingestion_date}/"
        f"products.json"
    )

    results = {
        "batch_id": batch_id,
        "ingestion_date": ingestion_date,
        "source_name": "dummyjson_products_api",
        "status": "SUCCESS",
        "s3_path": f"s3://{bucket_name}/{s3_key}",
    }

    logger.info(f"Starting external API ingestion. batch_id={batch_id}")

    try:
        payload = fetch_products_from_api(
            api_url=api_url,
            limit=limit,
            logger=logger,
        )

        s3_client = boto3.client(
            "s3",
            region_name=config["aws"]["region"],
        )

        upload_json_to_s3(
            s3_client=s3_client,
            bucket_name=bucket_name,
            s3_key=s3_key,
            payload=payload,
            logger=logger,
        )

    except Exception as error:
        results["status"] = "FAILED"
        results["error"] = str(error)

    logger.info(f"External API ingestion completed with status={results['status']}")

    return results


if __name__ == "__main__":
    output = ingest_external_products()
    print(output)