# Model Performance Report

## Model Summary

| Field | Value |
|---|---|
| Model Name | recomart_svd_recommender |
| Model Version | v1 |
| Model Type | collaborative_filtering_svd |
| Run ID | 3571852c-5f20-4896-9202-1069a909c253 |
| Source Validation Batch ID | 20260430030321 |
| Feature Version | v1 |
| Model Artifact Path | models/recommendation_model/recomart_svd_recommender_3571852c-5f20-4896-9202-1069a909c253.joblib |

## Parameters

| Parameter | Value |
|---|---|
| n_components | 20 |
| top_k | 10 |
| random_state | 42 |
| train_rows | 10289 |
| test_rows | 388 |
| users | 435 |
| items | 909 |

## Evaluation Metrics

| Metric | Value |
|---|---|
| Precision@10 | 0.008854 |
| Recall@10 | 0.088542 |
| NDCG@10 | 0.055634 |
| Hit Rate@10 | 0.088542 |
| Evaluated Users | 384 |

## Interpretation

RecoMart uses a collaborative filtering model based on Matrix Factorization using Truncated SVD.

The source dataset contains implicit user behavior. Therefore, user actions are converted into weighted scores:

- Product view = 1
- Add to cart = 3
- Transaction = 5

The model learns latent user and item representations from the user-item interaction matrix and generates top-K product recommendations based on predicted affinity scores.
