# RecoMart Recommendation Pipeline: Folder Structure and Objectives

## 1. Project Overview

RecoMart is an end-to-end data management and recommendation pipeline for an e-commerce platform. The pipeline collects user behavior, product metadata, category hierarchy, and external product enrichment data; stores raw data in Amazon S3; loads it into Snowflake; validates and prepares the data; creates recommendation features; publishes features to a feature store; tracks data lineage and model metadata; trains a recommendation model; orchestrates execution with Airflow; and generates reports for assignment submission.

The pipeline follows this flow:

```text
Source Data / External API
        ↓
Amazon S3 Raw Data Lake
        ↓
Snowflake RAW Layer
        ↓
Snowflake VALIDATED Layer
        ↓
Snowflake CURATED Layer
        ↓
Feature Engineering Tables
        ↓
Feature Store
        ↓
Model Training and Evaluation
        ↓
Reports and Orchestration Logs
```

---

## 2. Recommended Root Folder Structure

```text
recomart_pipeline/
│
├── config/
│   └── config.yaml
│
├── data/
│   ├── source/
│   │   └── recomart/
│   │       ├── events.csv
│   │       ├── item_properties_part1.csv
│   │       ├── item_properties_part2.csv
│   │       ├── category_tree.csv
│   │       ├── events.csv.dvc
│   │       ├── item_properties_part1.csv.dvc
│   │       ├── item_properties_part2.csv.dvc
│   │       └── category_tree.csv.dvc
│   │
│   └── metadata/
│       └── dataset_version_manifest.json
│
├── ingestion/
│   ├── __init__.py
│   ├── ingest_recomart_to_s3.py
│   ├── ingest_external_api_to_s3.py
│   └── run_ingestion.py
│
├── snowflake_load/
│   ├── __init__.py
│   └── load_raw_from_s3.py
│
├── validation/
│   ├── __init__.py
│   └── run_validation.py
│
├── preparation/
│   ├── __init__.py
│   └── run_preparation.py
│
├── feature_engineering/
│   ├── __init__.py
│   └── run_feature_engineering.py
│
├── feature_store/
│   ├── __init__.py
│   └── run_feature_store.py
│
├── lineage/
│   ├── __init__.py
│   ├── generate_dataset_manifest.py
│   └── run_lineage_tracking.py
│
├── model_training/
│   ├── __init__.py
│   ├── config.yaml
│   └── train_recommendation_model.py
│
├── orchestration/
│   ├── __init__.py
│   └── run_sql_file.py
│
├── dags/
│   └── recomart_cli_orchestration_dag.py
│
├── reporting/
│   ├── __init__.py
│   └── generate_reports.py
│
├── sql/
│   ├── load_raw_from_s3.sql
│   │
│   ├── validation/
│   │   ├── 00_add_validation_audit_columns.sql
│   │   ├── 01_profile_raw_data.sql
│   │   ├── 02_validate_raw_to_validated.sql
│   │   ├── 03_data_quality_checks.sql
│   │   └── 04_data_quality_report_queries.sql
│   │
│   ├── preparation/
│   │   ├── 00_add_preparation_objects.sql
│   │   ├── 01_prepare_clean_datasets.sql
│   │   ├── 02_create_user_item_interactions.sql
│   │   ├── 03_create_user_item_features.sql
│   │   └── 04_eda_queries.sql
│   │
│   ├── feature_engineering/
│   │   ├── 00_create_feature_objects.sql
│   │   ├── 01_create_user_activity_features.sql
│   │   ├── 02_create_item_popularity_features.sql
│   │   ├── 03_create_user_category_affinity.sql
│   │   ├── 04_create_item_similarity_features.sql
│   │   └── 05_create_training_dataset.sql
│   │
│   ├── feature_store/
│   │   ├── 00_create_feature_store_objects.sql
│   │   ├── 01_register_feature_metadata.sql
│   │   ├── 02_publish_offline_features.sql
│   │   ├── 03_publish_online_features.sql
│   │   └── 04_feature_retrieval_demo.sql
│   │
│   ├── lineage/
│   │   ├── 00_create_lineage_objects.sql
│   │   ├── 01_insert_dataset_version_registry.sql
│   │   ├── 02_insert_data_lineage.sql
│   │   └── 03_lineage_report_queries.sql
│   │
│   ├── model_training/
│   │   ├── 00_create_model_tracking_objects.sql
│   │   └── 01_model_report_queries.sql
│   │
│   └── orchestration/
│       └── final_health_check.sql
│
├── reports/
│   ├── exports/
│   ├── data_quality_report.md
│   ├── eda_report.md
│   ├── feature_engineering_report.md
│   ├── feature_store_report.md
│   ├── lineage_report.md
│   ├── model_performance_report.md
│   ├── orchestration_report.md
│   └── report_index.md
│
├── models/
│   └── recommendation_model/
│
├── notebooks/
│   └── eda_recomart.ipynb
│
├── docs/
│   ├── problem_formulation.md
│   ├── data_versioning_and_lineage.md
│   └── project_structure_and_objectives.md
│
├── logs/
│   ├── ingestion.log
│   ├── snowflake_load.log
│   ├── validation.log
│   ├── preparation.log
│   ├── feature_engineering.log
│   ├── feature_store.log
│   ├── lineage.log
│   ├── model_training.log
│   ├── reporting.log
│   └── airflow/
│       ├── recomart_airflow_dag_success.log
│       ├── 01_check_environment.log
│       ├── 02_ingestion_and_raw_load.log
│       ├── 04_validation.log
│       ├── 05_preparation.log
│       ├── 06_feature_engineering.log
│       ├── 07_feature_store.log
│       ├── 08_lineage.log
│       ├── 09_model_training.log
│       ├── 10_generate_reports.log
│       └── 11_final_health_check.log
│
├── airflow_cli_home/
├── airflow_cli_venv/
├── .dvc/
├── .dvcignore
├── dvc.yaml
├── dvc.lock
├── .env
├── .gitignore
├── requirements.txt
├── run_airflow_dag.sh
└── README.md
```

---

## 3. Section-wise Folder Objectives

## 3.1 `config/`

### Folder Structure

```text
config/
└── config.yaml
```

### Objective

The `config/` folder stores common project-level configuration values such as project name, environment, AWS region, S3 bucket name, S3 raw folder paths, local source file paths, and external API details.

### Main Responsibilities

- Centralize configuration for ingestion.
- Avoid hardcoding bucket names and local paths inside Python scripts.
- Make the pipeline easier to move between environments such as development, test, and production.

---

## 3.2 `data/`

### Folder Structure

```text
data/
├── source/
│   └── recomart/
│       ├── events.csv
│       ├── item_properties_part1.csv
│       ├── item_properties_part2.csv
│       ├── category_tree.csv
│       └── *.dvc
│
└── metadata/
    └── dataset_version_manifest.json
```

### Objective

The `data/` folder stores local source datasets and generated dataset metadata. The large CSV files are tracked using DVC instead of being committed directly to Git.

### Main Responsibilities

- Store local copies of raw input datasets.
- Maintain DVC pointer files for dataset versioning.
- Store dataset manifest metadata such as row count, file size, hash, source path, and target Snowflake table.

---

## 3.3 `ingestion/`

### Folder Structure

```text
ingestion/
├── __init__.py
├── ingest_recomart_to_s3.py
├── ingest_external_api_to_s3.py
└── run_ingestion.py
```

### Objective

The `ingestion/` folder contains Python scripts responsible for collecting source data and uploading it to Amazon S3.

### Main Responsibilities

- Upload local RecoMart CSV files to S3.
- Fetch external product enrichment data from an API.
- Upload external API JSON data to S3.
- Trigger automated S3-to-Snowflake loading after S3 upload completes.
- Write ingestion logs for monitoring and debugging.

### Pipeline Stage

```text
Local CSV/API → S3 Raw Data Lake
```

---

## 3.4 `snowflake_load/`

### Folder Structure

```text
snowflake_load/
├── __init__.py
└── load_raw_from_s3.py
```

### Objective

The `snowflake_load/` folder automates loading data from S3 into Snowflake RAW tables.

### Main Responsibilities

- Connect to Snowflake using environment variables.
- Execute `sql/load_raw_from_s3.sql` automatically.
- Run `COPY INTO` commands to load staged S3 files into RAW tables.
- Generate a common load batch ID for all RAW tables in one run.
- Write load logs into `logs/snowflake_load.log`.

### Pipeline Stage

```text
S3 Raw Data Lake → Snowflake RAW Schema
```

---

## 3.5 `validation/`

### Folder Structure

```text
validation/
├── __init__.py
└── run_validation.py

sql/validation/
├── 00_add_validation_audit_columns.sql
├── 01_profile_raw_data.sql
├── 02_validate_raw_to_validated.sql
├── 03_data_quality_checks.sql
└── 04_data_quality_report_queries.sql
```

### Objective

The `validation/` section performs data profiling and validation after the raw data has been loaded into Snowflake.

### Main Responsibilities

- Profile RAW tables.
- Check missing values, duplicate records, invalid event types, and transaction ID issues.
- Move validated records into the `VALIDATED` schema.
- Store `IS_VALID`, `VALIDATION_MESSAGE`, `VALIDATION_BATCH_ID`, `VALIDATION_RUN_TS`, and `VALIDATED_BY`.
- Store data quality results in `OPS.DATA_QUALITY_RESULTS`.

### Pipeline Stage

```text
Snowflake RAW Schema → Snowflake VALIDATED Schema
```

---

## 3.6 `preparation/`

### Folder Structure

```text
preparation/
├── __init__.py
└── run_preparation.py

sql/preparation/
├── 00_add_preparation_objects.sql
├── 01_prepare_clean_datasets.sql
├── 02_create_user_item_interactions.sql
├── 03_create_user_item_features.sql
└── 04_eda_queries.sql
```

### Objective

The `preparation/` section converts validated data into clean, curated, analysis-ready, and model-ready datasets.

### Main Responsibilities

- Select only valid records from the validated layer.
- Convert timestamps into event date, hour, and day-of-week fields.
- Encode event types numerically.
- Apply implicit event weights:
  - `view = 1`
  - `addtocart = 3`
  - `transaction = 5`
- Create user-item interaction tables.
- Create user features, item features, and product catalog features.
- Support EDA queries.

### Pipeline Stage

```text
Snowflake VALIDATED Schema → Snowflake CURATED Schema
```

---

## 3.7 `feature_engineering/`

### Folder Structure

```text
feature_engineering/
├── __init__.py
└── run_feature_engineering.py

sql/feature_engineering/
├── 00_create_feature_objects.sql
├── 01_create_user_activity_features.sql
├── 02_create_item_popularity_features.sql
├── 03_create_user_category_affinity.sql
├── 04_create_item_similarity_features.sql
└── 05_create_training_dataset.sql
```

### Objective

The `feature_engineering/` section creates advanced recommendation features from curated data.

### Main Responsibilities

- Create user activity features.
- Create item popularity and conversion features.
- Create category affinity features.
- Create item co-occurrence features.
- Create item similarity features.
- Build the final model-ready training dataset.
- Maintain feature version and source validation batch lineage.

### Pipeline Stage

```text
CURATED Clean Tables → Recommendation Feature Tables
```

---

## 3.8 `feature_store/`

### Folder Structure

```text
feature_store/
├── __init__.py
└── run_feature_store.py

sql/feature_store/
├── 00_create_feature_store_objects.sql
├── 01_register_feature_metadata.sql
├── 02_publish_offline_features.sql
├── 03_publish_online_features.sql
└── 04_feature_retrieval_demo.sql
```

### Objective

The `feature_store/` section manages reusable, versioned features for model training and inference.

### Main Responsibilities

- Create the `FEATURE_STORE` Snowflake schema.
- Register feature metadata in `FEATURE_REGISTRY`.
- Publish offline features for model training.
- Publish online features for inference use cases.
- Track feature version, source validation batch ID, and retrieval logs.
- Reduce training-serving skew by using consistent feature definitions.

### Pipeline Stage

```text
Feature Engineering Tables → Feature Store Tables
```

---

## 3.9 `lineage/`

### Folder Structure

```text
lineage/
├── __init__.py
├── generate_dataset_manifest.py
└── run_lineage_tracking.py

sql/lineage/
├── 00_create_lineage_objects.sql
├── 01_insert_dataset_version_registry.sql
├── 02_insert_data_lineage.sql
└── 03_lineage_report_queries.sql
```

### Objective

The `lineage/` section tracks dataset versions and end-to-end pipeline lineage.

### Main Responsibilities

- Generate dataset version manifest.
- Calculate file hash, file size, and row count.
- Register dataset versions in Snowflake.
- Track source-to-target transformation flow.
- Maintain batch-level traceability from raw source data to features and model output.

### Pipeline Stage

```text
Dataset Files + Pipeline Metadata → Version Registry + Data Lineage Tables
```

---

## 3.10 `model_training/`

### Folder Structure

```text
model_training/
├── __init__.py
├── config.yaml
└── train_recommendation_model.py

sql/model_training/
├── 00_create_model_tracking_objects.sql
└── 01_model_report_queries.sql

models/
└── recommendation_model/
```

### Objective

The `model_training/` section trains and evaluates the recommendation model.

### Main Responsibilities

- Load offline training features from the feature store.
- Train a collaborative filtering model using Matrix Factorization with Truncated SVD.
- Evaluate the model using ranking metrics:
  - Precision@K
  - Recall@K
  - NDCG@K
  - Hit Rate@K
- Track experiment metadata using MLflow.
- Store model metadata and metrics in Snowflake `ML_MONITORING` tables.
- Save model artifacts under `models/recommendation_model/`.

### Pipeline Stage

```text
Feature Store Offline Features → Model Training → Metrics + Recommendations
```

---

## 3.11 `orchestration/` and `dags/`

### Folder Structure

```text
orchestration/
├── __init__.py
└── run_sql_file.py

dags/
└── recomart_cli_orchestration_dag.py

sql/orchestration/
└── final_health_check.sql
```

### Objective

The orchestration section automates the complete end-to-end pipeline using Apache Airflow.

### Main Responsibilities

- Define Airflow DAG task dependencies.
- Execute each pipeline stage in the correct order.
- Run SQL files through a reusable Snowflake SQL runner.
- Capture task-level logs.
- Track task failures through callback logic.
- Execute a final health check after model training and reporting.

### Pipeline Stage

```text
Airflow DAG → End-to-End Pipeline Automation
```

---

## 3.12 `reporting/`

### Folder Structure

```text
reporting/
├── __init__.py
└── generate_reports.py

reports/
├── exports/
├── data_quality_report.md
├── eda_report.md
├── feature_engineering_report.md
├── feature_store_report.md
├── lineage_report.md
├── model_performance_report.md
├── orchestration_report.md
└── report_index.md
```

### Objective

The `reporting/` section generates final Markdown reports and CSV exports from Snowflake and pipeline logs.

### Main Responsibilities

- Generate data quality report.
- Generate EDA report.
- Generate feature engineering report.
- Generate feature store report.
- Generate lineage report.
- Generate model performance report.
- Generate orchestration report.
- Save detailed query outputs as CSV files under `reports/exports/`.
- Create a central `report_index.md` file.

### Pipeline Stage

```text
Snowflake Metadata + Pipeline Logs → Markdown Reports + CSV Exports
```

---

## 3.13 `sql/`

### Folder Structure

```text
sql/
├── load_raw_from_s3.sql
├── validation/
├── preparation/
├── feature_engineering/
├── feature_store/
├── lineage/
├── model_training/
└── orchestration/
```

### Objective

The `sql/` folder stores all Snowflake SQL scripts used by the pipeline.

### Main Responsibilities

- Keep transformation logic separate from Python orchestration logic.
- Make SQL scripts reusable from local execution, Airflow, or manual Snowflake testing.
- Organize SQL by pipeline phase.
- Support debugging by allowing each phase to be run independently.

---

## 3.14 `logs/`

### Folder Structure

```text
logs/
├── ingestion.log
├── snowflake_load.log
├── validation.log
├── preparation.log
├── feature_engineering.log
├── feature_store.log
├── lineage.log
├── model_training.log
├── reporting.log
└── airflow/
```

### Objective

The `logs/` folder stores execution logs from all pipeline stages.

### Main Responsibilities

- Capture operational logs for each script.
- Store Airflow CLI task logs.
- Provide evidence of successful execution for assignment submission.
- Support debugging in case of pipeline failure.

---

## 3.15 `docs/`

### Folder Structure

```text
docs/
├── problem_formulation.md
├── data_versioning_and_lineage.md
└── project_structure_and_objectives.md
```

### Objective

The `docs/` folder stores written documentation for the assignment.

### Main Responsibilities

- Document business problem formulation.
- Document data source and pipeline design.
- Document versioning and lineage workflow.
- Document folder structure and section objectives.
- Provide clear explanation for assignment evaluation.

---

## 3.16 `.env`, `.gitignore`, `requirements.txt`, and `run_airflow_dag.sh`

### Folder Structure

```text
.env
.gitignore
requirements.txt
run_airflow_dag.sh
```

### Objective

These files support environment configuration, dependency management, Git hygiene, and pipeline execution.

### Main Responsibilities

- `.env` stores local environment variables and credentials.
- `.gitignore` prevents secrets, logs, virtual environments, and raw CSV data from being committed.
- `requirements.txt` lists project Python dependencies.
- `run_airflow_dag.sh` executes the Airflow DAG in CLI mode and saves execution logs.

---

## 4. Pipeline Section Mapping

| Assignment Section | Main Folder | Main Output |
|---|---|---|
| Problem Formulation | `docs/` | Problem definition and pipeline objectives |
| Data Collection and Ingestion | `ingestion/` | S3 raw files |
| Raw Data Storage and Snowflake Loading | `snowflake_load/`, `sql/load_raw_from_s3.sql` | Snowflake RAW tables |
| Data Profiling and Validation | `validation/`, `sql/validation/` | VALIDATED tables and DQ results |
| Data Preparation and EDA | `preparation/`, `sql/preparation/` | CURATED clean datasets and EDA outputs |
| Feature Engineering and Transformation | `feature_engineering/`, `sql/feature_engineering/` | Feature tables and training dataset |
| Feature Store | `feature_store/`, `sql/feature_store/` | Offline and online feature tables |
| Data Versioning and Lineage | `lineage/`, `sql/lineage/`, `.dvc/` | Dataset registry and lineage flow |
| Model Training and Evaluation | `model_training/`, `models/`, `mlruns/` | Model artifact, metrics, MLflow run |
| Pipeline Orchestration | `dags/`, `orchestration/` | Airflow DAG and execution logs |
| Reporting | `reporting/`, `reports/` | Markdown reports and CSV exports |

---

## 5. Execution Order

```text
1. ingestion/run_ingestion.py
2. snowflake_load/load_raw_from_s3.py
3. validation/run_validation.py
4. preparation/run_preparation.py
5. feature_engineering/run_feature_engineering.py
6. feature_store/run_feature_store.py
7. lineage/generate_dataset_manifest.py
8. lineage/run_lineage_tracking.py
9. model_training/train_recommendation_model.py
10. reporting/generate_reports.py
11. run_airflow_dag.sh
```

In the automated Airflow flow, these steps are executed through the DAG:

```text
check_environment
        ↓
ingest_source_data_to_s3_and_load_raw_snowflake
        ↓
validate_raw_data
        ↓
prepare_curated_data
        ↓
run_feature_engineering
        ↓
publish_feature_store
        ↓
track_versioning_and_lineage
        ↓
train_and_evaluate_model
        ↓
generate_reports
        ↓
final_health_check
```

---

## 6. Final Deliverables Produced

| Deliverable | Location |
|---|---|
| Problem formulation report | `docs/problem_formulation.md` |
| Ingestion scripts | `ingestion/` |
| S3 to Snowflake load script | `snowflake_load/load_raw_from_s3.py`, `sql/load_raw_from_s3.sql` |
| Validation SQL and runner | `validation/`, `sql/validation/` |
| Data preparation SQL and runner | `preparation/`, `sql/preparation/` |
| Feature engineering SQL and runner | `feature_engineering/`, `sql/feature_engineering/` |
| Feature store implementation | `feature_store/`, `sql/feature_store/` |
| DVC dataset versioning files | `.dvc/`, `dvc.yaml`, `dvc.lock`, `*.dvc` |
| Dataset manifest | `data/metadata/dataset_version_manifest.json` |
| Lineage tracking tables/scripts | `lineage/`, `sql/lineage/` |
| Model training script | `model_training/train_recommendation_model.py` |
| Model artifacts | `models/recommendation_model/` |
| MLflow runs | `mlruns/` |
| Airflow DAG | `dags/recomart_cli_orchestration_dag.py` |
| Airflow execution logs | `logs/airflow/` |
| Generated reports | `reports/` |
| CSV report exports | `reports/exports/` |

---

## 7. Summary

This folder structure keeps the RecoMart pipeline modular, maintainable, and assignment-ready. Each phase of the pipeline has a dedicated folder, clear responsibility, separate SQL scripts, separate Python runners, and separate logs. This makes it easy to debug individual phases, rerun specific stages, and present deliverables clearly during assignment evaluation.
