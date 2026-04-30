# Data Versioning and Lineage Workflow

## Objective

RecoMart uses DVC and Snowflake lineage tables to track dataset versions, pipeline transformations, and feature lineage across the recommendation pipeline.

## Versioning Tool

DVC is used for dataset versioning because the project stores large raw datasets externally in Amazon S3. Git is used for source code, SQL scripts, and DVC pointer files. Raw CSV files are not committed directly to Git.

## DVC Remote

The DVC remote is configured as:

```text
s3://recomartdatalake/dvc-store