# Data Preparation and EDA Report

**Generated At:** 2026-04-30 15:20:19 UTC

**Project:** RecoMart Recommendation Data Pipeline

---
## Clean Event Summary

**CSV Export:** `reports/exports/eda_clean_event_summary.csv`

|   TOTAL_EVENTS |   UNIQUE_USERS |   UNIQUE_ITEMS | FIRST_EVENT_TS             | LAST_EVENT_TS              |
|---------------:|---------------:|---------------:|:---------------------------|:---------------------------|
|        8266923 |        1407580 |         235061 | 2015-05-03 03:00:04.384000 | 2015-09-18 02:59:47.788000 |

---
## Event Type Distribution

**CSV Export:** `reports/exports/eda_event_distribution.csv`

| EVENT_TYPE   |   EVENT_COUNT |   EVENT_PERCENTAGE |
|:-------------|--------------:|-------------------:|
| view         |       7992654 |              96.68 |
| addtocart    |        206898 |               2.5  |
| transaction  |         67371 |               0.81 |

---
## Top 20 Popular Products

**CSV Export:** `reports/exports/eda_top_products.csv`

|   ITEM_ID |   TOTAL_VIEWS |   TOTAL_ADD_TO_CARTS |   TOTAL_TRANSACTIONS |   ITEM_POPULARITY_SCORE |   CONVERSION_RATE |
|----------:|--------------:|---------------------:|---------------------:|------------------------:|------------------:|
|    461686 |          2538 |                  304 |                  133 |                    4115 |          0.052403 |
|    461686 |          2538 |                  304 |                  133 |                    4115 |          0.052403 |
|    461686 |          2538 |                  304 |                  133 |                    4115 |          0.052403 |
|    187946 |          3410 |                    2 |                    0 |                    3416 |          0        |
|    187946 |          3410 |                    2 |                    0 |                    3416 |          0        |
|    187946 |          3410 |                    2 |                    0 |                    3416 |          0        |
|      5411 |          2325 |                    9 |                    0 |                    2352 |          0        |
|      5411 |          2325 |                    9 |                    0 |                    2352 |          0        |
|      5411 |          2325 |                    9 |                    0 |                    2352 |          0        |
|    219512 |          1740 |                   48 |                   12 |                    1944 |          0.006897 |
|    219512 |          1740 |                   48 |                   12 |                    1944 |          0.006897 |
|    219512 |          1740 |                   48 |                   12 |                    1944 |          0.006897 |
|    257040 |          1531 |                   89 |                   27 |                    1933 |          0.017636 |
|    257040 |          1531 |                   89 |                   27 |                    1933 |          0.017636 |
|    257040 |          1531 |                   89 |                   27 |                    1933 |          0.017636 |
|    320130 |          1333 |                  141 |                   33 |                    1921 |          0.024756 |
|    320130 |          1333 |                  141 |                   33 |                    1921 |          0.024756 |
|    320130 |          1333 |                  141 |                   33 |                    1921 |          0.024756 |
|      7943 |          1346 |                   97 |                   46 |                    1867 |          0.034175 |
|      7943 |          1346 |                   97 |                   46 |                    1867 |          0.034175 |

---
## User-Item Matrix Sparsity

**CSV Export:** `reports/exports/eda_user_item_sparsity.csv`

|   USER_COUNT |   ITEM_COUNT |   OBSERVED_INTERACTIONS |   POSSIBLE_INTERACTIONS |   SPARSITY_RATIO |
|-------------:|-------------:|------------------------:|------------------------:|-----------------:|
|      1407580 |       235061 |                 6435537 |            330867162380 |         0.999981 |

---
