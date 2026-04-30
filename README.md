# RecoMart End-to-End Data Management Pipeline for Recommendation System

This repository is a complete assignment submission package for a recommendation system data management pipeline.

## Business problem
RecoMart wants to improve customer engagement and cross-selling by recommending relevant products to users based on clickstream behavior, purchase history, product metadata, and external API-style popularity/sentiment attributes.

## How to run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m src.orchestration.run_pipeline
```

## Data sources used

1. Clickstream CSV: user events such as view, cart, wishlist, and purchase.
2. Product API JSON: simulated REST API payload containing product catalog, popularity, and sentiment data.
3. Transaction CSV: purchase quantity, price, discounts, and total amount.

## Model baseline

The submitted baseline is collaborative filtering using SVD-style matrix factorization on a user-item interaction matrix.

Current local metrics:

- Precision@5: 0.04
- Recall@5: 0.2
- NDCG@5: 0.1055

## Demo video guide

Use `docs/demo_video_script.md` to record a 5-10 minute walkthrough.
