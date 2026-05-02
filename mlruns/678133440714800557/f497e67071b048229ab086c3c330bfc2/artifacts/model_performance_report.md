# Model Performance Report

## Model Summary

| Field | Value |
|---|---|
| Model Name | recomart_svd_recommender |
| Model Version | v1 |
| Model Type | collaborative_filtering_svd |
| Run ID | bf8e9ced-46e7-4aa8-a376-95133dc88830 |
| Source Validation Batch ID | 20260502024231 |
| Feature Version | v1 |
| Model Artifact Path | models/recommendation_model/recomart_svd_recommender_bf8e9ced-46e7-4aa8-a376-95133dc88830.joblib |

## Parameters

| Parameter | Value |
|---|---|
| n_components | 20 |
| top_k | 10 |
| random_state | 42 |
| train_rows | 10354 |
| test_rows | 388 |
| users | 434 |
| items | 910 |

## Evaluation Metrics

| Metric | Value |
|---|---|
| Precision@10 | 0.010909 |
| Recall@10 | 0.109091 |
| NDCG@10 | 0.059628 |
| Hit Rate@10 | 0.109091 |
| Evaluated Users | 385 |

## Interpretation

RecoMart uses a collaborative filtering model based on Matrix Factorization using Truncated SVD.

The source dataset contains implicit user behavior. Therefore, user actions are converted into weighted scores:

- Product view = 1
- Add to cart = 3
- Transaction = 5

The model learns latent user and item representations from the user-item interaction matrix and generates top-K product recommendations based on predicted affinity scores.
