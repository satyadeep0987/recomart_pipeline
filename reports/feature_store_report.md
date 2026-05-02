# Feature Store Report

**Generated At:** 2026-05-02 10:16:41 UTC

**Project:** RecoMart Recommendation Data Pipeline

---
## Feature Registry Summary

**CSV Export:** `reports/exports/feature_registry_summary.csv`

| FEATURE_GROUP   | ENTITY_TYPE   | FEATURE_VERSION   |   FEATURE_COUNT |
|:----------------|:--------------|:------------------|----------------:|
| interaction     | user_item     | v1                |               5 |
| item_popularity | item          | v1                |              25 |
| training_label  | user_item     | v1                |               5 |
| user_activity   | user          | v1                |              25 |

---
## Offline Feature Store Summary

**CSV Export:** `reports/exports/offline_feature_store_summary.csv`

| FEATURE_VERSION   |   SOURCE_VALIDATION_BATCH_ID |   OFFLINE_FEATURE_ROWS | FIRST_PUBLISHED_TS         | LAST_PUBLISHED_TS          |
|:------------------|-----------------------------:|-----------------------:|:---------------------------|:---------------------------|
| v1                |               20260502031153 |                2145179 | 2026-05-02 03:16:18.401000 | 2026-05-02 03:16:18.401000 |
| v1                |               20260502024231 |                2145179 | 2026-05-02 02:46:27.317000 | 2026-05-02 02:46:27.317000 |
| v1                |               20260430081645 |                2145179 | 2026-04-30 08:19:53.258000 | 2026-04-30 08:19:53.258000 |
| v1                |               20260430075931 |                2145179 | 2026-04-30 08:03:26.606000 | 2026-04-30 08:03:26.606000 |
| v1                |               20260430030321 |                2145179 | 2026-04-30 07:39:48.625000 | 2026-04-30 07:39:48.625000 |

---
## Online Feature Sample

**CSV Export:** `reports/exports/online_feature_sample.csv`

|   USER_ID |   ITEM_ID | USER_ACTIVITY_LEVEL   |   ITEM_POPULARITY_SCORE |   ITEM_CONVERSION_RATE |   USER_ITEM_IMPLICIT_SCORE |   RECOMMENDATION_CANDIDATE_SCORE | FEATURE_VERSION   |   SOURCE_VALIDATION_BATCH_ID |
|----------:|----------:|:----------------------|------------------------:|-----------------------:|---------------------------:|---------------------------------:|:------------------|-----------------------------:|
|   1150086 |    461686 | HIGH                  |                    4115 |               0.052403 |                         45 |                          1257.01 | v1                |               20260502031153 |
|   1150086 |    461686 | HIGH                  |                    4115 |               0.052403 |                         45 |                          1257.01 | v1                |               20260430081645 |
|   1150086 |    461686 | HIGH                  |                    4115 |               0.052403 |                         45 |                          1257.01 | v1                |               20260430075931 |
|   1150086 |    461686 | HIGH                  |                    4115 |               0.052403 |                         45 |                          1257.01 | v1                |               20260430030321 |
|   1150086 |    461686 | HIGH                  |                    4115 |               0.052403 |                         45 |                          1257.01 | v1                |               20260502024231 |
|     90729 |    461686 | MEDIUM                |                    4115 |               0.052403 |                         32 |                          1250.51 | v1                |               20260502031153 |
|     90729 |    461686 | MEDIUM                |                    4115 |               0.052403 |                         32 |                          1250.51 | v1                |               20260430081645 |
|     90729 |    461686 | MEDIUM                |                    4115 |               0.052403 |                         32 |                          1250.51 | v1                |               20260502024231 |
|     90729 |    461686 | MEDIUM                |                    4115 |               0.052403 |                         32 |                          1250.51 | v1                |               20260430075931 |
|     90729 |    461686 | MEDIUM                |                    4115 |               0.052403 |                         32 |                          1250.51 | v1                |               20260430030321 |
|    968159 |    461686 | HIGH                  |                    4115 |               0.052403 |                         28 |                          1248.51 | v1                |               20260430030321 |
|    968159 |    461686 | HIGH                  |                    4115 |               0.052403 |                         28 |                          1248.51 | v1                |               20260430081645 |
|    968159 |    461686 | HIGH                  |                    4115 |               0.052403 |                         28 |                          1248.51 | v1                |               20260502024231 |
|    968159 |    461686 | HIGH                  |                    4115 |               0.052403 |                         28 |                          1248.51 | v1                |               20260502031153 |
|    968159 |    461686 | HIGH                  |                    4115 |               0.052403 |                         28 |                          1248.51 | v1                |               20260430075931 |
|    672218 |    461686 | HIGH                  |                    4115 |               0.052403 |                         27 |                          1248.01 | v1                |               20260430030321 |
|    672218 |    461686 | HIGH                  |                    4115 |               0.052403 |                         27 |                          1248.01 | v1                |               20260430081645 |
|    672218 |    461686 | HIGH                  |                    4115 |               0.052403 |                         27 |                          1248.01 | v1                |               20260502031153 |
|    672218 |    461686 | HIGH                  |                    4115 |               0.052403 |                         27 |                          1248.01 | v1                |               20260502024231 |
|    672218 |    461686 | HIGH                  |                    4115 |               0.052403 |                         27 |                          1248.01 | v1                |               20260430075931 |

---
## Feature Retrieval Logs

**CSV Export:** `reports/exports/feature_retrieval_logs.csv`

| REQUEST_ID                           |   USER_ID | ITEM_ID   | FEATURE_VERSION   |   SOURCE_VALIDATION_BATCH_ID | REQUEST_TYPE          | REQUEST_TS                 | STATUS   | MESSAGE                                                      |
|:-------------------------------------|----------:|:----------|:------------------|-----------------------------:|:----------------------|:---------------------------|:---------|:-------------------------------------------------------------|
| ceb379a3-6d0d-455d-998e-748866522e87 |   1150086 |           | v1                |               20260502031153 | ONLINE_INFERENCE_DEMO | 2026-05-02 03:16:23.876000 | SUCCESS  | Retrieved top online recommendation features for sample user |
| 4abe8a89-7889-4252-a3f5-6d11a9fd84e9 |   1150086 |           | v1                |               20260502024231 | ONLINE_INFERENCE_DEMO | 2026-05-02 02:46:32.239000 | SUCCESS  | Retrieved top online recommendation features for sample user |
| 63b64518-5298-421a-bb8f-5caaf475c503 |   1150086 |           | v1                |               20260430081645 | ONLINE_INFERENCE_DEMO | 2026-04-30 08:19:57.590000 | SUCCESS  | Retrieved top online recommendation features for sample user |
| 168ae7d0-bc52-41c3-bf3d-0f4d5fa062fe |   1150086 |           | v1                |               20260430075931 | ONLINE_INFERENCE_DEMO | 2026-04-30 08:03:31.899000 | SUCCESS  | Retrieved top online recommendation features for sample user |
| bbe12ed0-9719-4c8a-86a3-ddeef595a531 |   1150086 |           | v1                |               20260430030321 | ONLINE_INFERENCE_DEMO | 2026-04-30 07:40:06.723000 | SUCCESS  | Retrieved top online recommendation features for sample user |
| ac34c2c8-e64b-4ef0-81a0-93a4f4fb5b96 |   1150086 |           | v1                |               20260430030321 | ONLINE_INFERENCE_DEMO | 2026-04-30 05:07:34.086000 | SUCCESS  | Retrieved top online recommendation features for sample user |
| b7b89c83-c85c-47b2-8b8c-fef2f72f68ac |   1150086 |           | v1                |               20260430030321 | ONLINE_INFERENCE_DEMO | 2026-04-30 04:25:32.422000 | SUCCESS  | Retrieved top online recommendation features for sample user |

---
