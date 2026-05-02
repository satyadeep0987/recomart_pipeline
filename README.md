# RecoMart End-to-End Data Management Pipeline for Recommendation System

This repository is a complete assignment submission package for a recommendation system data management pipeline.

## Business problem
RecoMart wants to improve customer engagement and cross-selling by recommending relevant products to users based on clickstream behavior, purchase history, product metadata, and external API-style popularity/sentiment attributes.

## How to run locally

```bash

pipx install "dvc[s3]"

export AWS_ACCESS_KEY_ID="your_access_key_id"
export AWS_SECRET_ACCESS_KEY="your_secret_access_key"
export AWS_DEFAULT_REGION="ap-south-1"

aws configure --profile recomart

aws sts get-caller-identity --profile recomart
aws s3 ls s3://recomartdatalake --profile recomart

dvc remote modify --local recomart_s3_remote profile recomart
dvc remote modify --local recomart_s3_remote region ap-south-1

cd /Users/sd/Desktop/recomart_pipeline

dvc init

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

dvc remote add -d recomart_s3_remote s3://recomartdatalake/dvc-store
cat .dvc/config.local
dvc add data/source/recomart/events.csv
dvc add data/source/recomart/item_properties_part1.csv
dvc add data/source/recomart/item_properties_part2.csv
dvc add data/source/recomart/category_tree.csv

dvc push

python3 -m venv airflow_cli_venv
source airflow_cli_venv/bin/activate

AIRFLOW_VERSION=2.10.5
PYTHON_VERSION=3.11
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"

pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"

./run_airflow_dag.sh
```

To check mlflow:
```bash

mlflow ui --backend-store-uri ./mlruns --port 5000

```


## Data sources used

1. Data Setused: 
   [Retailrocket recommender system dataset](https://www.kaggle.com/datasets/retailrocket/ecommerce-dataset)
2. Product API JSON: simulated REST API payload containing product catalog, popularity, and sentiment data.
    [Retailrocket recommender system dataset](https://dummyjson.com/products)

## Model baseline

The submitted baseline is collaborative filtering using SVD-style matrix factorization on a user-item interaction matrix.

Current local metrics:

- Precision@5: 0.04
- Recall@5: 0.2
- NDCG@5: 0.1055
