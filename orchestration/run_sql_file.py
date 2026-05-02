import os
import sys
import logging
from pathlib import Path
from typing import List

import snowflake.connector
from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ENV_FILE = PROJECT_ROOT / ".env"
LOG_DIR = PROJECT_ROOT / "logs"
LOG_FILE = LOG_DIR / "orchestration_sql_runner.log"

load_dotenv(dotenv_path=ENV_FILE)


def setup_logger() -> logging.Logger:
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("recomart_sql_runner")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )

        file_handler = logging.FileHandler(LOG_FILE)
        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger


def get_required_env(name: str) -> str:
    value = os.getenv(name)

    if not value:
        raise EnvironmentError(f"Missing required environment variable: {name}")

    return value


def get_snowflake_connection():
    return snowflake.connector.connect(
        account=get_required_env("SNOWFLAKE_ACCOUNT"),
        user=get_required_env("SNOWFLAKE_USER"),
        password=get_required_env("SNOWFLAKE_PASSWORD"),
        role=os.getenv("SNOWFLAKE_ROLE", "ACCOUNTADMIN"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE", "RECOMART_WH"),
        database=os.getenv("SNOWFLAKE_DATABASE", "RECOMART_DB"),
        autocommit=True,
    )


def remove_sql_comments(sql_text: str) -> str:
    cleaned_lines = []

    for line in sql_text.splitlines():
        stripped = line.strip()

        if stripped.startswith("--"):
            continue

        cleaned_lines.append(line)

    return "\n".join(cleaned_lines)


def split_sql_statements(sql_text: str) -> List[str]:
    """
    Splits SQL on semicolon, but ignores semicolons inside single/double quotes.
    This is safer than basic sql_text.split(';').
    """
    statements = []
    current = []

    in_single_quote = False
    in_double_quote = False
    escape_next = False

    for char in sql_text:
        if escape_next:
            current.append(char)
            escape_next = False
            continue

        if char == "\\":
            current.append(char)
            escape_next = True
            continue

        if char == "'" and not in_double_quote:
            in_single_quote = not in_single_quote
            current.append(char)
            continue

        if char == '"' and not in_single_quote:
            in_double_quote = not in_double_quote
            current.append(char)
            continue

        if char == ";" and not in_single_quote and not in_double_quote:
            statement = "".join(current).strip()

            if statement:
                statements.append(statement)

            current = []
            continue

        current.append(char)

    last_statement = "".join(current).strip()

    if last_statement:
        statements.append(last_statement)

    return statements


def resolve_sql_path(sql_file_path: str) -> Path:
    path = Path(sql_file_path)

    if path.is_absolute():
        return path

    return PROJECT_ROOT / path


def log_query_preview(cursor, logger: logging.Logger, statement_index: int) -> None:
    if cursor.description is None:
        return

    columns = [column[0] for column in cursor.description]
    rows = cursor.fetchmany(10)

    if not rows:
        logger.info(f"Statement {statement_index}: query returned no rows")
        return

    logger.info(f"Statement {statement_index}: result preview columns={columns}")

    for row in rows:
        logger.info(f"Statement {statement_index}: row={row}")


def execute_sql_file(cursor, sql_file_path: Path, logger: logging.Logger) -> None:
    if not sql_file_path.exists():
        raise FileNotFoundError(f"SQL file not found: {sql_file_path}")

    logger.info(f"Executing SQL file: {sql_file_path}")

    sql_text = sql_file_path.read_text(encoding="utf-8")
    sql_text = remove_sql_comments(sql_text)
    statements = split_sql_statements(sql_text)

    if not statements:
        logger.warning(f"No executable SQL statements found in: {sql_file_path}")
        return

    logger.info(f"Total SQL statements found: {len(statements)}")

    for index, statement in enumerate(statements, start=1):
        short_statement = " ".join(statement.split())[:300]

        logger.info("=" * 80)
        logger.info(f"Running statement {index}/{len(statements)}")
        logger.info(f"SQL preview: {short_statement}")

        try:
            cursor.execute(statement)
            logger.info(f"Statement {index} completed successfully")

            log_query_preview(
                cursor=cursor,
                logger=logger,
                statement_index=index,
            )

        except Exception as error:
            logger.error(f"Statement {index} failed")
            logger.error(f"Failed SQL preview: {short_statement}")
            logger.error(f"Error: {error}")
            raise


def run_sql_files(sql_file_paths: List[str]) -> None:
    logger = setup_logger()

    logger.info("=" * 80)
    logger.info("RecoMart SQL runner started")
    logger.info(f"Project root: {PROJECT_ROOT}")
    logger.info(f"Environment file: {ENV_FILE}")
    logger.info(f"SQL files received: {sql_file_paths}")

    connection = None

    try:
        connection = get_snowflake_connection()
        cursor = connection.cursor()

        logger.info("Connected to Snowflake successfully")

        for sql_file_path in sql_file_paths:
            resolved_path = resolve_sql_path(sql_file_path)
            execute_sql_file(
                cursor=cursor,
                sql_file_path=resolved_path,
                logger=logger,
            )

        logger.info("All SQL files executed successfully")

    except Exception as error:
        logger.error(f"SQL runner failed: {error}")
        raise

    finally:
        if connection:
            connection.close()
            logger.info("Snowflake connection closed")

        logger.info("RecoMart SQL runner finished")
        logger.info("=" * 80)


def main() -> None:
    if len(sys.argv) < 2:
        raise ValueError(
            "Usage: python orchestration/run_sql_file.py <sql_file_path_1> [sql_file_path_2 ...]"
        )

    sql_file_paths = sys.argv[1:]
    run_sql_files(sql_file_paths)


if __name__ == "__main__":
    main()