# Model Performance Report

## Model Summary

| Field | Value |
|---|---|
| Model Name | recomart_svd_recommender |
| Model Version | v1 |
| Model Type | collaborative_filtering_svd |
| Run ID | 26046283-e600-4c8c-84a4-991880d319dd |
| Source Validation Batch ID | 20260430030321 |
| Feature Version | v1 |
| Model Artifact Path | models/recommendation_model/recomart_svd_recommender_26046283-e600-4c8c-84a4-991880d319dd.joblib |

## Parameters

| Parameter | Value |
|---|---|
| n_components | 20 |
| top_k | 10 |
| random_state | 42 |
| train_rows | 10287 |
| test_rows | 388 |
| users | 435 |
| items | 912 |

## Evaluation Metrics

| Metric | Value |
|---|---|
| Precision@10 | 0.010594 |
| Recall@10 | 0.105943 |
| NDCG@10 | 0.065897 |
| Hit Rate@10 | 0.105943 |
| Evaluated Users | 387 |

## Interpretation

RecoMart uses a collaborative filtering model based on Matrix Factorization using Truncated SVD.

The source dataset contains implicit user behavior. Therefore, user actions are converted into weighted scores:

- Product view = 1
- Add to cart = 3
- Transaction = 5

The model learns latent user and item representations from the user-item interaction matrix and generates top-K product recommendations based on predicted affinity scores.
