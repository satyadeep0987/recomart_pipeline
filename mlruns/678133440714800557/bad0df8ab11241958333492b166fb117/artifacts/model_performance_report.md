# Model Performance Report

## Model Summary

| Field | Value |
|---|---|
| Model Name | recomart_svd_recommender |
| Model Version | v1 |
| Model Type | collaborative_filtering_svd |
| Run ID | 8dab2e16-c85e-40da-a9b5-029bc9d33414 |
| Source Validation Batch ID | 20260430081645 |
| Feature Version | v1 |
| Model Artifact Path | models/recommendation_model/recomart_svd_recommender_8dab2e16-c85e-40da-a9b5-029bc9d33414.joblib |

## Parameters

| Parameter | Value |
|---|---|
| n_components | 20 |
| top_k | 10 |
| random_state | 42 |
| train_rows | 10321 |
| test_rows | 388 |
| users | 434 |
| items | 910 |

## Evaluation Metrics

| Metric | Value |
|---|---|
| Precision@10 | 0.007792 |
| Recall@10 | 0.077922 |
| NDCG@10 | 0.049773 |
| Hit Rate@10 | 0.077922 |
| Evaluated Users | 385 |

## Interpretation

RecoMart uses a collaborative filtering model based on Matrix Factorization using Truncated SVD.

The source dataset contains implicit user behavior. Therefore, user actions are converted into weighted scores:

- Product view = 1
- Add to cart = 3
- Transaction = 5

The model learns latent user and item representations from the user-item interaction matrix and generates top-K product recommendations based on predicted affinity scores.
