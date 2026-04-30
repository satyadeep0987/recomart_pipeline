#!/bin/bash

set -euo pipefail

PROJECT_HOME="/Users/sd/Desktop/recomart_pipeline"
AIRFLOW_VENV="${PROJECT_HOME}/airflow_cli_venv"
AIRFLOW_HOME_DIR="${PROJECT_HOME}/airflow_cli_home"
PROJECT_PYTHON="${PROJECT_HOME}/.venv/bin/python"
DAG_ID="recomart_cli_end_to_end_pipeline"
EXECUTION_DATE="2026-04-30"
LOG_DIR="${PROJECT_HOME}/logs/airflow"
LOG_FILE="${LOG_DIR}/recomart_airflow_dag_success.log"

echo "============================================================"
echo "RecoMart Airflow DAG Execution Started"
echo "Project Home       : ${PROJECT_HOME}"
echo "Airflow Home       : ${AIRFLOW_HOME_DIR}"
echo "Project Python     : ${PROJECT_PYTHON}"
echo "DAG ID             : ${DAG_ID}"
echo "Execution Date     : ${EXECUTION_DATE}"
echo "Log File           : ${LOG_FILE}"
echo "============================================================"

mkdir -p "${LOG_DIR}"

if [ ! -d "${AIRFLOW_VENV}" ]; then
  echo "ERROR: Airflow virtual environment not found: ${AIRFLOW_VENV}"
  exit 1
fi

if [ ! -x "${PROJECT_PYTHON}" ]; then
  echo "ERROR: Project Python not found or not executable: ${PROJECT_PYTHON}"
  exit 1
fi

cd "${PROJECT_HOME}"

source "${AIRFLOW_VENV}/bin/activate"

export AIRFLOW_HOME="${AIRFLOW_HOME_DIR}"
export RECOMART_PROJECT_HOME="${PROJECT_HOME}"
export RECOMART_PROJECT_PYTHON="${PROJECT_PYTHON}"

echo "Checking Airflow DAG availability..."
airflow dags list | grep "${DAG_ID}"

echo "Running Airflow DAG..."
airflow dags test "${DAG_ID}" "${EXECUTION_DATE}" 2>&1 | tee "${LOG_FILE}"

EXIT_CODE=${PIPESTATUS[0]}

if [ "${EXIT_CODE}" -eq 0 ]; then
  echo "============================================================"
  echo "RecoMart Airflow DAG completed successfully"
  echo "Log saved at: ${LOG_FILE}"
  echo "============================================================"
else
  echo "============================================================"
  echo "RecoMart Airflow DAG failed"
  echo "Check log at: ${LOG_FILE}"
  echo "============================================================"
fi

exit "${EXIT_CODE}"