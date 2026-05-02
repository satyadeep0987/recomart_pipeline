#!/bin/bash

set -euo pipefail

# --- Configuration ---
PROJECT_HOME="/Users/sd/Desktop/recomart_pipeline"
AIRFLOW_VENV="${PROJECT_HOME}/airflow_cli_venv"
AIRFLOW_HOME_DIR="${PROJECT_HOME}/airflow_cli_home"
PROJECT_PYTHON="${PROJECT_HOME}/.venv/bin/python"
DAG_ID="recomart_cli_end_to_end_pipeline"

# Using a dynamic timestamp to avoid "Success" state collisions in the local DB
# and to ensure the date is always >= days_ago(1).
EXECUTION_DATE=$(date +"%Y-%m-%dT%H:%M:%S")

LOG_DIR="${PROJECT_HOME}/logs/airflow"
LOG_FILE="${LOG_DIR}/recomart_airflow_dag_$(date +'%Y%m%d_%H%M%S').log"

echo "============================================================"
echo "RecoMart Airflow DAG Execution Started"
echo "Project Home       : ${PROJECT_HOME}"
echo "Airflow Home       : ${AIRFLOW_HOME_DIR}"
echo "Project Python     : ${PROJECT_PYTHON}"
echo "DAG ID             : ${DAG_ID}"
echo "Execution Date     : ${EXECUTION_DATE}"
echo "Log File           : ${LOG_FILE}"
echo "============================================================"

# --- Environment Setup ---
mkdir -p "${LOG_DIR}"
mkdir -p "${AIRFLOW_HOME_DIR}/dags"

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

# --- Airflow Environment Variables ---
export AIRFLOW_HOME="${AIRFLOW_HOME_DIR}"
export AIRFLOW__CORE__LOAD_EXAMPLES="False"
export AIRFLOW__CORE__DAGS_ARE_PAUSED_AT_CREATION="False"
export AIRFLOW__CORE__DAGS_FOLDER="${AIRFLOW_HOME_DIR}/dags"

# Project runtime paths used inside the DAG
export RECOMART_PROJECT_HOME="${PROJECT_HOME}"
export RECOMART_PROJECT_PYTHON="${PROJECT_PYTHON}"
export PYTHONPATH="${PROJECT_HOME}:${PYTHONPATH:-}"

# --- Fresh Start Logic ---
# Optional: Uncomment the line below if you want to wipe previous run history 
# from the local SQLite DB every time you run this script.
# rm -f "${AIRFLOW_HOME_DIR}/airflow.db"

echo "Checking Airflow DAG availability..."
if ! airflow dags list | grep -q "${DAG_ID}"; then
  echo "ERROR: DAG ${DAG_ID} not found in ${AIRFLOW__CORE__DAGS_FOLDER}"
  exit 1
fi

echo "Running Airflow DAG..."
# Using the absolute path to airflow to ensure the venv version is used.
"${AIRFLOW_VENV}/bin/airflow" dags test "${DAG_ID}" "${EXECUTION_DATE}" 2>&1 | tee "${LOG_FILE}"

EXIT_CODE=${PIPESTATUS[0]}

# --- Result Handling ---
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