import os
import logging
from pathlib import Path

from dotenv import load_dotenv
import snowflake.connector


load_dotenv()


SQL_FILES = [
    "sql/feature_store/00_create_feature_store_objects.sql",
    "sql/feature_store/01_register_feature_metadata.sql",
    "sql/feature_store/02_publish_offline_features.sql",
    "sql/feature_store/03_publish_online_features.sql",
    "sql/feature_store/04_feature_retrieval_demo.sql",
]


def setup_logger() -> logging.Logger:
    os.makedirs("logs", exist_ok=True)

    logger = logging.getLogger("recomart_feature_store")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        file_handler = logging.FileHandler("logs/feature_store.log")
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


def execute_sql_file(cursor, sql_file_path: str, logger: logging.Logger) -> None:
    path = Path(sql_file_path)

    if not path.exists():
        raise FileNotFoundError(f"SQL file not found: {sql_file_path}")

    logger.info(f"Executing SQL file: {sql_file_path}")

    sql_text = path.read_text()
    statements = split_sql_statements(sql_text)

    for statement in statements:
        try:
            cursor.execute(statement)
            logger.info("Statement executed successfully")
        except Exception as error:
            logger.error(f"Failed SQL statement: {statement[:300]}")
            logger.error(f"Error: {error}")
            raise


def main() -> None:
    logger = setup_logger()
    logger.info("Starting RecoMart feature store pipeline")

    connection = None

    try:
        connection = get_snowflake_connection()
        cursor = connection.cursor()

        for sql_file in SQL_FILES:
            execute_sql_file(cursor, sql_file, logger)

        logger.info("RecoMart feature store pipeline completed successfully")

    except Exception as error:
        logger.error(f"Feature store pipeline failed: {error}")
        raise

    finally:
        if connection:
            connection.close()
            logger.info("Snowflake connection closed")


if __name__ == "__main__":
    main()