# Model Performance Report

**Generated At:** 2026-04-30 15:20:22 UTC

**Project:** RecoMart Recommendation Data Pipeline

---
## Latest Model Runs

**CSV Export:** `reports/exports/latest_model_runs.csv`

| RUN_ID                               | MODEL_NAME               | MODEL_VERSION   | MODEL_TYPE                  | TRAINING_STATUS   | FEATURE_VERSION   |   SOURCE_VALIDATION_BATCH_ID | MODEL_ARTIFACT_PATH                                                                              | MLFLOW_RUN_ID                    | TRAINING_START_TS          | TRAINING_END_TS            | CREATED_TS                 |
|:-------------------------------------|:-------------------------|:----------------|:----------------------------|:------------------|:------------------|-----------------------------:|:-------------------------------------------------------------------------------------------------|:---------------------------------|:---------------------------|:---------------------------|:---------------------------|
| 8dab2e16-c85e-40da-a9b5-029bc9d33414 | recomart_svd_recommender | v1              | collaborative_filtering_svd | SUCCESS           | v1                |               20260430081645 | models/recommendation_model/recomart_svd_recommender_8dab2e16-c85e-40da-a9b5-029bc9d33414.joblib | bad0df8ab11241958333492b166fb117 | 2026-04-30 15:20:08        | 2026-04-30 15:20:12        | 2026-04-30 08:20:12.420000 |
| b34eab25-6666-46fc-9022-db9515a8df24 | recomart_svd_recommender | v1              | collaborative_filtering_svd | SUCCESS           | v1                |               20260430075931 | models/recommendation_model/recomart_svd_recommender_b34eab25-6666-46fc-9022-db9515a8df24.joblib | 2a5ed43456e54fe3b4a3ec8ff716c031 | 2026-04-30 15:03:42        | 2026-04-30 15:03:48        | 2026-04-30 08:03:48.603000 |
| 26046283-e600-4c8c-84a4-991880d319dd | recomart_svd_recommender | v1              | collaborative_filtering_svd | SUCCESS           | v1                |               20260430030321 | models/recommendation_model/recomart_svd_recommender_26046283-e600-4c8c-84a4-991880d319dd.joblib | cddf0b467df440f39099c64ed4b8f807 | 2026-04-30 14:40:34        | 2026-04-30 14:40:39        | 2026-04-30 07:40:39.401000 |
| 3571852c-5f20-4896-9202-1069a909c253 | recomart_svd_recommender | v1              | collaborative_filtering_svd | SUCCESS           | v1                |               20260430030321 | models/recommendation_model/recomart_svd_recommender_3571852c-5f20-4896-9202-1069a909c253.joblib | a00b9c185b854e0ca2fd593246a79f23 | 2026-04-30 13:28:11        | 2026-04-30 13:28:23        | 2026-04-30 06:28:24.033000 |
| c9ad0eb2-6594-45fa-b99a-54a485a014bc | recomart_svd_recommender | v1              | collaborative_filtering_svd | SUCCESS           | v1                |               20260430030321 | models/recommendation_model/recomart_svd_recommender_c9ad0eb2-6594-45fa-b99a-54a485a014bc.joblib | dde43bcf756145fbb3f0dc019415853b | 2026-04-30 12:59:11.406786 | 2026-04-30 13:00:18.226006 | 2026-04-30 06:00:19.367000 |

---
## Model Metrics

**CSV Export:** `reports/exports/model_metrics.csv`

| RUN_ID                               | MODEL_NAME               | MODEL_VERSION   | METRIC_NAME     |   METRIC_VALUE |   K_VALUE | FEATURE_VERSION   |   SOURCE_VALIDATION_BATCH_ID | EVALUATION_DATE   | CREATED_TS                 |
|:-------------------------------------|:-------------------------|:----------------|:----------------|---------------:|----------:|:------------------|-----------------------------:|:------------------|:---------------------------|
| 8dab2e16-c85e-40da-a9b5-029bc9d33414 | recomart_svd_recommender | v1              | evaluated_users |   385          |        10 | v1                |               20260430081645 | 2026-04-30        | 2026-04-30 08:20:13.116000 |
| 8dab2e16-c85e-40da-a9b5-029bc9d33414 | recomart_svd_recommender | v1              | hit_rate_at_k   |     0.0779221  |        10 | v1                |               20260430081645 | 2026-04-30        | 2026-04-30 08:20:13.116000 |
| 8dab2e16-c85e-40da-a9b5-029bc9d33414 | recomart_svd_recommender | v1              | ndcg_at_k       |     0.0497729  |        10 | v1                |               20260430081645 | 2026-04-30        | 2026-04-30 08:20:13.116000 |
| 8dab2e16-c85e-40da-a9b5-029bc9d33414 | recomart_svd_recommender | v1              | precision_at_k  |     0.00779221 |        10 | v1                |               20260430081645 | 2026-04-30        | 2026-04-30 08:20:13.116000 |
| 8dab2e16-c85e-40da-a9b5-029bc9d33414 | recomart_svd_recommender | v1              | recall_at_k     |     0.0779221  |        10 | v1                |               20260430081645 | 2026-04-30        | 2026-04-30 08:20:13.116000 |
| b34eab25-6666-46fc-9022-db9515a8df24 | recomart_svd_recommender | v1              | evaluated_users |   385          |        10 | v1                |               20260430075931 | 2026-04-30        | 2026-04-30 08:03:49.313000 |
| b34eab25-6666-46fc-9022-db9515a8df24 | recomart_svd_recommender | v1              | hit_rate_at_k   |     0.0779221  |        10 | v1                |               20260430075931 | 2026-04-30        | 2026-04-30 08:03:49.313000 |
| b34eab25-6666-46fc-9022-db9515a8df24 | recomart_svd_recommender | v1              | ndcg_at_k       |     0.0494592  |        10 | v1                |               20260430075931 | 2026-04-30        | 2026-04-30 08:03:49.313000 |
| b34eab25-6666-46fc-9022-db9515a8df24 | recomart_svd_recommender | v1              | precision_at_k  |     0.00779221 |        10 | v1                |               20260430075931 | 2026-04-30        | 2026-04-30 08:03:49.313000 |
| b34eab25-6666-46fc-9022-db9515a8df24 | recomart_svd_recommender | v1              | recall_at_k     |     0.0779221  |        10 | v1                |               20260430075931 | 2026-04-30        | 2026-04-30 08:03:49.313000 |
| 26046283-e600-4c8c-84a4-991880d319dd | recomart_svd_recommender | v1              | evaluated_users |   387          |        10 | v1                |               20260430030321 | 2026-04-30        | 2026-04-30 07:40:39.828000 |
| 26046283-e600-4c8c-84a4-991880d319dd | recomart_svd_recommender | v1              | hit_rate_at_k   |     0.105943   |        10 | v1                |               20260430030321 | 2026-04-30        | 2026-04-30 07:40:39.828000 |
| 26046283-e600-4c8c-84a4-991880d319dd | recomart_svd_recommender | v1              | ndcg_at_k       |     0.0658971  |        10 | v1                |               20260430030321 | 2026-04-30        | 2026-04-30 07:40:39.828000 |
| 26046283-e600-4c8c-84a4-991880d319dd | recomart_svd_recommender | v1              | precision_at_k  |     0.0105943  |        10 | v1                |               20260430030321 | 2026-04-30        | 2026-04-30 07:40:39.828000 |
| 26046283-e600-4c8c-84a4-991880d319dd | recomart_svd_recommender | v1              | recall_at_k     |     0.105943   |        10 | v1                |               20260430030321 | 2026-04-30        | 2026-04-30 07:40:39.828000 |
| 3571852c-5f20-4896-9202-1069a909c253 | recomart_svd_recommender | v1              | evaluated_users |   384          |        10 | v1                |               20260430030321 | 2026-04-30        | 2026-04-30 06:28:33.765000 |
| 3571852c-5f20-4896-9202-1069a909c253 | recomart_svd_recommender | v1              | hit_rate_at_k   |     0.0885417  |        10 | v1                |               20260430030321 | 2026-04-30        | 2026-04-30 06:28:33.765000 |
| 3571852c-5f20-4896-9202-1069a909c253 | recomart_svd_recommender | v1              | ndcg_at_k       |     0.0556339  |        10 | v1                |               20260430030321 | 2026-04-30        | 2026-04-30 06:28:33.765000 |
| 3571852c-5f20-4896-9202-1069a909c253 | recomart_svd_recommender | v1              | precision_at_k  |     0.00885417 |        10 | v1                |               20260430030321 | 2026-04-30        | 2026-04-30 06:28:33.765000 |
| 3571852c-5f20-4896-9202-1069a909c253 | recomart_svd_recommender | v1              | recall_at_k     |     0.0885417  |        10 | v1                |               20260430030321 | 2026-04-30        | 2026-04-30 06:28:33.765000 |
| c9ad0eb2-6594-45fa-b99a-54a485a014bc | recomart_svd_recommender | v1              | evaluated_users |  4344          |        10 | v1                |               20260430030321 | 2026-04-30        | 2026-04-30 06:00:22.444000 |
| c9ad0eb2-6594-45fa-b99a-54a485a014bc | recomart_svd_recommender | v1              | hit_rate_at_k   |     0.0393646  |        10 | v1                |               20260430030321 | 2026-04-30        | 2026-04-30 06:00:22.089000 |
| c9ad0eb2-6594-45fa-b99a-54a485a014bc | recomart_svd_recommender | v1              | ndcg_at_k       |     0.0245337  |        10 | v1                |               20260430030321 | 2026-04-30        | 2026-04-30 06:00:21.410000 |
| c9ad0eb2-6594-45fa-b99a-54a485a014bc | recomart_svd_recommender | v1              | recall_at_k     |     0.0393646  |        10 | v1                |               20260430030321 | 2026-04-30        | 2026-04-30 06:00:20.952000 |
| c9ad0eb2-6594-45fa-b99a-54a485a014bc | recomart_svd_recommender | v1              | precision_at_k  |     0.00393646 |        10 | v1                |               20260430030321 | 2026-04-30        | 2026-04-30 06:00:20.635000 |

---
## Sample Recommendation Results

**CSV Export:** `reports/exports/sample_recommendation_results.csv`

| REQUEST_ID                           |   USER_ID |   ITEM_ID |   RANK_POSITION |   RECOMMENDATION_SCORE | MODEL_NAME               | MODEL_VERSION   | FEATURE_VERSION   |   SOURCE_VALIDATION_BATCH_ID | GENERATED_TS               |
|:-------------------------------------|----------:|----------:|----------------:|-----------------------:|:-------------------------|:----------------|:------------------|-----------------------------:|:---------------------------|
| 7fab0a90-b393-4bb1-acab-b70ed11bb487 |      1879 |     38965 |               1 |              0.522387  | recomart_svd_recommender | v1              | v1                |               20260430081645 | 2026-04-30 08:20:13.550000 |
| 7fab0a90-b393-4bb1-acab-b70ed11bb487 |      1879 |    252319 |               2 |              0.294346  | recomart_svd_recommender | v1              | v1                |               20260430081645 | 2026-04-30 08:20:13.550000 |
| 7fab0a90-b393-4bb1-acab-b70ed11bb487 |      1879 |    283115 |               3 |              0.291627  | recomart_svd_recommender | v1              | v1                |               20260430081645 | 2026-04-30 08:20:13.550000 |
| 7fab0a90-b393-4bb1-acab-b70ed11bb487 |      1879 |    241555 |               4 |              0.197739  | recomart_svd_recommender | v1              | v1                |               20260430081645 | 2026-04-30 08:20:13.550000 |
| 7fab0a90-b393-4bb1-acab-b70ed11bb487 |      1879 |      9877 |               5 |              0.138568  | recomart_svd_recommender | v1              | v1                |               20260430081645 | 2026-04-30 08:20:13.550000 |
| 7fab0a90-b393-4bb1-acab-b70ed11bb487 |      1879 |    162139 |               6 |              0.111133  | recomart_svd_recommender | v1              | v1                |               20260430081645 | 2026-04-30 08:20:13.550000 |
| 7fab0a90-b393-4bb1-acab-b70ed11bb487 |      1879 |    318333 |               7 |              0.106477  | recomart_svd_recommender | v1              | v1                |               20260430081645 | 2026-04-30 08:20:13.550000 |
| 7fab0a90-b393-4bb1-acab-b70ed11bb487 |      1879 |    248455 |               8 |              0.101562  | recomart_svd_recommender | v1              | v1                |               20260430081645 | 2026-04-30 08:20:13.550000 |
| 7fab0a90-b393-4bb1-acab-b70ed11bb487 |      1879 |     57245 |               9 |              0.100327  | recomart_svd_recommender | v1              | v1                |               20260430081645 | 2026-04-30 08:20:13.550000 |
| 7fab0a90-b393-4bb1-acab-b70ed11bb487 |      1879 |    137697 |              10 |              0.0986475 | recomart_svd_recommender | v1              | v1                |               20260430081645 | 2026-04-30 08:20:13.550000 |
| 7fab0a90-b393-4bb1-acab-b70ed11bb487 |      2194 |    119736 |               1 |              0.0834457 | recomart_svd_recommender | v1              | v1                |               20260430081645 | 2026-04-30 08:20:13.550000 |
| 7fab0a90-b393-4bb1-acab-b70ed11bb487 |      2194 |     48030 |               2 |              0.0779686 | recomart_svd_recommender | v1              | v1                |               20260430081645 | 2026-04-30 08:20:13.550000 |
| 7fab0a90-b393-4bb1-acab-b70ed11bb487 |      2194 |      9877 |               3 |              0.0638925 | recomart_svd_recommender | v1              | v1                |               20260430081645 | 2026-04-30 08:20:13.550000 |
| 7fab0a90-b393-4bb1-acab-b70ed11bb487 |      2194 |    369158 |               4 |              0.0511054 | recomart_svd_recommender | v1              | v1                |               20260430081645 | 2026-04-30 08:20:13.550000 |
| 7fab0a90-b393-4bb1-acab-b70ed11bb487 |      2194 |    420960 |               5 |              0.048984  | recomart_svd_recommender | v1              | v1                |               20260430081645 | 2026-04-30 08:20:13.550000 |
| 7fab0a90-b393-4bb1-acab-b70ed11bb487 |      2194 |    387373 |               6 |              0.0470614 | recomart_svd_recommender | v1              | v1                |               20260430081645 | 2026-04-30 08:20:13.550000 |
| 7fab0a90-b393-4bb1-acab-b70ed11bb487 |      2194 |     23762 |               7 |              0.0457858 | recomart_svd_recommender | v1              | v1                |               20260430081645 | 2026-04-30 08:20:13.550000 |
| 7fab0a90-b393-4bb1-acab-b70ed11bb487 |      2194 |     17478 |               8 |              0.0452273 | recomart_svd_recommender | v1              | v1                |               20260430081645 | 2026-04-30 08:20:13.550000 |
| 7fab0a90-b393-4bb1-acab-b70ed11bb487 |      2194 |    144704 |               9 |              0.0450743 | recomart_svd_recommender | v1              | v1                |               20260430081645 | 2026-04-30 08:20:13.550000 |
| 7fab0a90-b393-4bb1-acab-b70ed11bb487 |      2194 |    204494 |              10 |              0.0429503 | recomart_svd_recommender | v1              | v1                |               20260430081645 | 2026-04-30 08:20:13.550000 |
| 7fab0a90-b393-4bb1-acab-b70ed11bb487 |      6699 |     46156 |               1 |              1.20271   | recomart_svd_recommender | v1              | v1                |               20260430081645 | 2026-04-30 08:20:13.550000 |
| 7fab0a90-b393-4bb1-acab-b70ed11bb487 |      6699 |    387373 |               2 |              0.896777  | recomart_svd_recommender | v1              | v1                |               20260430081645 | 2026-04-30 08:20:13.550000 |
| 7fab0a90-b393-4bb1-acab-b70ed11bb487 |      6699 |    314789 |               3 |              0.710255  | recomart_svd_recommender | v1              | v1                |               20260430081645 | 2026-04-30 08:20:13.550000 |
| 7fab0a90-b393-4bb1-acab-b70ed11bb487 |      6699 |    144704 |               4 |              0.688277  | recomart_svd_recommender | v1              | v1                |               20260430081645 | 2026-04-30 08:20:13.550000 |
| 7fab0a90-b393-4bb1-acab-b70ed11bb487 |      6699 |    369447 |               5 |              0.670206  | recomart_svd_recommender | v1              | v1                |               20260430081645 | 2026-04-30 08:20:13.550000 |
| 7fab0a90-b393-4bb1-acab-b70ed11bb487 |      6699 |    115258 |               6 |              0.614229  | recomart_svd_recommender | v1              | v1                |               20260430081645 | 2026-04-30 08:20:13.550000 |
| 7fab0a90-b393-4bb1-acab-b70ed11bb487 |      6699 |    315543 |               7 |              0.608949  | recomart_svd_recommender | v1              | v1                |               20260430081645 | 2026-04-30 08:20:13.550000 |
| 7fab0a90-b393-4bb1-acab-b70ed11bb487 |      6699 |     85579 |               8 |              0.587252  | recomart_svd_recommender | v1              | v1                |               20260430081645 | 2026-04-30 08:20:13.550000 |
| 7fab0a90-b393-4bb1-acab-b70ed11bb487 |      6699 |     37029 |               9 |              0.574147  | recomart_svd_recommender | v1              | v1                |               20260430081645 | 2026-04-30 08:20:13.550000 |
| 7fab0a90-b393-4bb1-acab-b70ed11bb487 |      6699 |     23762 |              10 |              0.5235    | recomart_svd_recommender | v1              | v1                |               20260430081645 | 2026-04-30 08:20:13.550000 |
| 7fab0a90-b393-4bb1-acab-b70ed11bb487 |      9535 |    461686 |               1 |              0.0646409 | recomart_svd_recommender | v1              | v1                |               20260430081645 | 2026-04-30 08:20:13.550000 |
| 7fab0a90-b393-4bb1-acab-b70ed11bb487 |      9535 |    320130 |               2 |              0.0604587 | recomart_svd_recommender | v1              | v1                |               20260430081645 | 2026-04-30 08:20:13.550000 |
| 7fab0a90-b393-4bb1-acab-b70ed11bb487 |      9535 |      9877 |               3 |              0.0543909 | recomart_svd_recommender | v1              | v1                |               20260430081645 | 2026-04-30 08:20:13.550000 |
| 7fab0a90-b393-4bb1-acab-b70ed11bb487 |      9535 |    119736 |               4 |              0.0445265 | recomart_svd_recommender | v1              | v1                |               20260430081645 | 2026-04-30 08:20:13.550000 |
| 7fab0a90-b393-4bb1-acab-b70ed11bb487 |      9535 |    248455 |               5 |              0.0324901 | recomart_svd_recommender | v1              | v1                |               20260430081645 | 2026-04-30 08:20:13.550000 |
| 7fab0a90-b393-4bb1-acab-b70ed11bb487 |      9535 |    384302 |               6 |              0.0319402 | recomart_svd_recommender | v1              | v1                |               20260430081645 | 2026-04-30 08:20:13.550000 |
| 7fab0a90-b393-4bb1-acab-b70ed11bb487 |      9535 |    420960 |               7 |              0.0303763 | recomart_svd_recommender | v1              | v1                |               20260430081645 | 2026-04-30 08:20:13.550000 |
| 7fab0a90-b393-4bb1-acab-b70ed11bb487 |      9535 |    342530 |               8 |              0.0280658 | recomart_svd_recommender | v1              | v1                |               20260430081645 | 2026-04-30 08:20:13.550000 |
| 7fab0a90-b393-4bb1-acab-b70ed11bb487 |      9535 |    310944 |               9 |              0.0262225 | recomart_svd_recommender | v1              | v1                |               20260430081645 | 2026-04-30 08:20:13.550000 |
| 7fab0a90-b393-4bb1-acab-b70ed11bb487 |      9535 |     48030 |              10 |              0.0249945 | recomart_svd_recommender | v1              | v1                |               20260430081645 | 2026-04-30 08:20:13.550000 |
| 7fab0a90-b393-4bb1-acab-b70ed11bb487 |     12579 |    445351 |               1 |              0.741511  | recomart_svd_recommender | v1              | v1                |               20260430081645 | 2026-04-30 08:20:13.550000 |
| 7fab0a90-b393-4bb1-acab-b70ed11bb487 |     12579 |    355994 |               2 |              0.555628  | recomart_svd_recommender | v1              | v1                |               20260430081645 | 2026-04-30 08:20:13.550000 |
| 7fab0a90-b393-4bb1-acab-b70ed11bb487 |     12579 |    441852 |               3 |              0.432198  | recomart_svd_recommender | v1              | v1                |               20260430081645 | 2026-04-30 08:20:13.550000 |
| 7fab0a90-b393-4bb1-acab-b70ed11bb487 |     12579 |     37029 |               4 |              0.350456  | recomart_svd_recommender | v1              | v1                |               20260430081645 | 2026-04-30 08:20:13.550000 |
| 7fab0a90-b393-4bb1-acab-b70ed11bb487 |     12579 |    465522 |               5 |              0.347304  | recomart_svd_recommender | v1              | v1                |               20260430081645 | 2026-04-30 08:20:13.550000 |
| 7fab0a90-b393-4bb1-acab-b70ed11bb487 |     12579 |     11279 |               6 |              0.347129  | recomart_svd_recommender | v1              | v1                |               20260430081645 | 2026-04-30 08:20:13.550000 |
| 7fab0a90-b393-4bb1-acab-b70ed11bb487 |     12579 |    409804 |               7 |              0.345199  | recomart_svd_recommender | v1              | v1                |               20260430081645 | 2026-04-30 08:20:13.550000 |
| 7fab0a90-b393-4bb1-acab-b70ed11bb487 |     12579 |    439963 |               8 |              0.320016  | recomart_svd_recommender | v1              | v1                |               20260430081645 | 2026-04-30 08:20:13.550000 |
| 7fab0a90-b393-4bb1-acab-b70ed11bb487 |     12579 |    109583 |               9 |              0.307678  | recomart_svd_recommender | v1              | v1                |               20260430081645 | 2026-04-30 08:20:13.550000 |
| 7fab0a90-b393-4bb1-acab-b70ed11bb487 |     12579 |    268883 |              10 |              0.296682  | recomart_svd_recommender | v1              | v1                |               20260430081645 | 2026-04-30 08:20:13.550000 |

---
