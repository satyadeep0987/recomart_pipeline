import os
import logging
from pathlib import Path

from dotenv import load_dotenv
import snowflake.connector


load_dotenv()


def setup_logger() -> logging.Logger:
    os.makedirs("logs", exist_ok=True)

    logger = logging.getLogger("snowflake_raw_loader")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        file_handler = logging.FileHandler("logs/snowflake_load.log")
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


def split_sql_statements(sql_text: str) -> list[str]:
    statements = []

    for statement in sql_text.split(";"):
        cleaned_statement = statement.strip()

        if cleaned_statement:
            statements.append(cleaned_statement)

    return statements


def run_sql_file(cursor, sql_file_path: str, logger: logging.Logger) -> None:
    path = Path(sql_file_path)

    if not path.exists():
        raise FileNotFoundError(f"SQL file not found: {sql_file_path}")

    sql_text = path.read_text()
    statements = split_sql_statements(sql_text)

    logger.info(f"Executing SQL file: {sql_file_path}")

    for index, statement in enumerate(statements, start=1):
        logger.info(f"Running statement {index}/{len(statements)}")

        try:
            cursor.execute(statement)
            logger.info(f"Statement {index} completed successfully")

        except Exception as error:
            logger.error(f"Statement {index} failed")
            logger.error(statement[:500])
            logger.error(str(error))
            raise


def load_raw_from_s3() -> None:
    logger = setup_logger()
    logger.info("Starting automated S3 to Snowflake RAW load")

    connection = None

    try:
        connection = get_snowflake_connection()
        cursor = connection.cursor()

        run_sql_file(
            cursor=cursor,
            sql_file_path="sql/load_raw_from_s3.sql",
            logger=logger,
        )

        logger.info("Automated S3 to Snowflake RAW load completed successfully")

    except Exception as error:
        logger.error(f"S3 to Snowflake RAW load failed: {error}")
        raise

    finally:
        if connection:
            connection.close()
            logger.info("Snowflake connection closed")


if __name__ == "__main__":
    load_raw_from_s3()