# Model Performance Report

## Model Summary

| Field | Value |
|---|---|
| Model Name | recomart_svd_recommender |
| Model Version | v1 |
| Model Type | collaborative_filtering_svd |
| Run ID | b14f3158-eb22-44e4-9a60-4c6ec3e0c8ea |
| Source Validation Batch ID | 20260502031153 |
| Feature Version | v1 |
| Model Artifact Path | models/recommendation_model/recomart_svd_recommender_b14f3158-eb22-44e4-9a60-4c6ec3e0c8ea.joblib |

## Parameters

| Parameter | Value |
|---|---|
| n_components | 20 |
| top_k | 10 |
| random_state | 42 |
| train_rows | 10305 |
| test_rows | 388 |
| users | 435 |
| items | 909 |

## Evaluation Metrics

| Metric | Value |
|---|---|
| Precision@10 | 0.008333 |
| Recall@10 | 0.083333 |
| NDCG@10 | 0.048749 |
| Hit Rate@10 | 0.083333 |
| Evaluated Users | 384 |

## Interpretation

RecoMart uses a collaborative filtering model based on Matrix Factorization using Truncated SVD.

The source dataset contains implicit user behavior. Therefore, user actions are converted into weighted scores:

- Product view = 1
- Add to cart = 3
- Transaction = 5

The model learns latent user and item representations from the user-item interaction matrix and generates top-K product recommendations based on predicted affinity scores.
