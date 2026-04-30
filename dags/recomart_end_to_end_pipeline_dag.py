from __future__ import annotations

import os
import json
from pathlib import Path
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from airflow.utils.trigger_rule import TriggerRule
from airflow.utils.dates import days_ago


PROJECT_HOME = os.environ.get(
    "RECOMART_PROJECT_HOME",
    "/Users/sd/Desktop/recomart_pipeline",
)

PROJECT_PYTHON = os.environ.get(
    "RECOMART_PROJECT_PYTHON",
    f"{PROJECT_HOME}/.venv/bin/python",
)

LOG_DIR = f"{PROJECT_HOME}/logs/airflow"


def task_failure_callback(context):
    Path(LOG_DIR).mkdir(parents=True, exist_ok=True)

    task_instance = context.get("task_instance")
    dag = context.get("dag")
    exception = context.get("exception")

    failure_payload = {
        "dag_id": dag.dag_id if dag else None,
        "task_id": task_instance.task_id if task_instance else None,
        "run_id": context.get("run_id"),
        "execution_date": str(context.get("execution_date")),
        "exception": str(exception),
        "failed_at": datetime.utcnow().isoformat(),
    }

    failure_file = Path(LOG_DIR) / "airflow_failure_event.json"

    with open(failure_file, "w") as file:
        json.dump(failure_payload, file, indent=2)

    print("RecoMart Airflow task failed")
    print(json.dumps(failure_payload, indent=2))


def build_bash_command(command: str, log_file: str) -> str:
    return f"""
    set -e
    cd "{PROJECT_HOME}"
    mkdir -p logs/airflow
    echo "============================================================" | tee -a "{log_file}"
    echo "Starting command at $(date)" | tee -a "{log_file}"
    echo "Command: {command}" | tee -a "{log_file}"
    echo "============================================================" | tee -a "{log_file}"
    {command} 2>&1 | tee -a "{log_file}"
    EXIT_CODE=${{PIPESTATUS[0]}}
    echo "============================================================" | tee -a "{log_file}"
    echo "Finished command at $(date) with exit code $EXIT_CODE" | tee -a "{log_file}"
    echo "============================================================" | tee -a "{log_file}"
    exit $EXIT_CODE
    """


default_args = {
    "owner": "recomart-data-platform",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
    "execution_timeout": timedelta(hours=3),
    "on_failure_callback": task_failure_callback,
}


with DAG(
    dag_id="recomart_cli_end_to_end_pipeline",
    description="CLI-only Airflow DAG for RecoMart recommendation pipeline",
    default_args=default_args,
    start_date=days_ago(1),
    schedule_interval=None,
    catchup=False,
    max_active_runs=1,
    tags=["recomart", "airflow-cli", "recommendation", "snowflake", "s3"],
) as dag:

    start_pipeline = EmptyOperator(
        task_id="start_pipeline",
    )

    check_environment = BashOperator(
        task_id="check_environment",
        bash_command=build_bash_command(
            command=(
                f'test -d "{PROJECT_HOME}" && '
                f'test -f "{PROJECT_HOME}/.env" && '
                f'test -x "{PROJECT_PYTHON}" && '
                f'"{PROJECT_PYTHON}" --version && '
                f'echo "Project environment check passed"'
            ),
            log_file=f"{LOG_DIR}/01_check_environment.log",
        ),
    )

    ingest_source_data_to_s3 = BashOperator(
        task_id="ingest_source_data_to_s3",
        bash_command=build_bash_command(
            command=f'"{PROJECT_PYTHON}" ingestion/run_ingestion.py',
            log_file=f"{LOG_DIR}/02_ingestion.log",
        ),
    )

    load_raw_data_to_snowflake = BashOperator(
        task_id="load_raw_data_to_snowflake",
        bash_command=build_bash_command(
            command=f'"{PROJECT_PYTHON}" orchestration/run_sql_file.py sql/load_raw_from_s3.sql',
            log_file=f"{LOG_DIR}/03_load_raw_to_snowflake.log",
        ),
    )

    validate_raw_data = BashOperator(
        task_id="validate_raw_data",
        bash_command=build_bash_command(
            command=f'"{PROJECT_PYTHON}" validation/run_validation.py',
            log_file=f"{LOG_DIR}/04_validation.log",
        ),
    )

    prepare_curated_data = BashOperator(
        task_id="prepare_curated_data",
        bash_command=build_bash_command(
            command=f'"{PROJECT_PYTHON}" preparation/run_preparation.py',
            log_file=f"{LOG_DIR}/05_preparation.log",
        ),
    )

    run_feature_engineering = BashOperator(
        task_id="run_feature_engineering",
        bash_command=build_bash_command(
            command=f'"{PROJECT_PYTHON}" feature_engineering/run_feature_engineering.py',
            log_file=f"{LOG_DIR}/06_feature_engineering.log",
        ),
    )

    publish_feature_store = BashOperator(
        task_id="publish_feature_store",
        bash_command=build_bash_command(
            command=f'"{PROJECT_PYTHON}" feature_store/run_feature_store.py',
            log_file=f"{LOG_DIR}/07_feature_store.log",
        ),
    )

    track_versioning_and_lineage = BashOperator(
        task_id="track_versioning_and_lineage",
        bash_command=build_bash_command(
            command=f'"{PROJECT_PYTHON}" lineage/run_lineage_tracking.py',
            log_file=f"{LOG_DIR}/08_lineage.log",
        ),
    )

    train_and_evaluate_model = BashOperator(
        task_id="train_and_evaluate_model",
        bash_command=build_bash_command(
            command=f'"{PROJECT_PYTHON}" model_training/train_recommendation_model.py',
            log_file=f"{LOG_DIR}/09_model_training.log",
        ),
    )

    final_health_check = BashOperator(
        task_id="final_health_check",
        bash_command=build_bash_command(
            command=(
                f'"{PROJECT_PYTHON}" orchestration/run_sql_file.py '
                f'sql/orchestration/final_health_check.sql'
            ),
            log_file=f"{LOG_DIR}/10_final_health_check.log",
        ),
    )

    pipeline_success = EmptyOperator(
        task_id="pipeline_success",
        trigger_rule=TriggerRule.ALL_SUCCESS,
    )

    pipeline_failure = EmptyOperator(
        task_id="pipeline_failure",
        trigger_rule=TriggerRule.ONE_FAILED,
    )

    (
        start_pipeline
        >> check_environment
        >> ingest_source_data_to_s3
        >> load_raw_data_to_snowflake
        >> validate_raw_data
        >> prepare_curated_data
        >> run_feature_engineering
        >> publish_feature_store
        >> track_versioning_and_lineage
        >> train_and_evaluate_model
        >> final_health_check
        >> pipeline_success
    )

    [
        check_environment,
        ingest_source_data_to_s3,
        load_raw_data_to_snowflake,
        validate_raw_data,
        prepare_curated_data,
        run_feature_engineering,
        publish_feature_store,
        track_versioning_and_lineage,
        train_and_evaluate_model,
        final_health_check,
    ] >> pipeline_failure