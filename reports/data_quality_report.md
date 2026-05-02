# Data Quality Report

**Generated At:** 2026-05-02 10:16:38 UTC

**Project:** RecoMart Recommendation Data Pipeline

---
## Data Quality Summary

**CSV Export:** `reports/exports/dq_summary.csv`

|   VALIDATION_BATCH_ID | STATUS   |   RULE_COUNT | FIRST_RULE_EXECUTED_TS     | LAST_RULE_EXECUTED_TS      |
|----------------------:|:---------|-------------:|:---------------------------|:---------------------------|
|        20260502031153 | FAILED   |            1 | 2026-05-02 03:15:07.452000 | 2026-05-02 03:15:07.452000 |
|        20260502031153 | PASSED   |            7 | 2026-05-02 03:15:06.139000 | 2026-05-02 03:15:10.496000 |
|        20260502024231 | FAILED   |            1 | 2026-05-02 02:45:15.669000 | 2026-05-02 02:45:15.669000 |
|        20260502024231 | PASSED   |            7 | 2026-05-02 02:45:14.200000 | 2026-05-02 02:45:18.292000 |
|        20260430081645 | FAILED   |            1 | 2026-04-30 08:18:36.675000 | 2026-04-30 08:18:36.675000 |
|        20260430081645 | PASSED   |            7 | 2026-04-30 08:18:35.387000 | 2026-04-30 08:18:38.685000 |
|        20260430075931 | FAILED   |            1 | 2026-04-30 08:01:49.356000 | 2026-04-30 08:01:49.356000 |
|        20260430075931 | PASSED   |            7 | 2026-04-30 08:01:40.772000 | 2026-04-30 08:01:55.415000 |
|        20260430030321 | FAILED   |            3 | 2026-04-30 03:48:10.701000 | 2026-04-30 07:37:42.053000 |
|        20260430030321 | PASSED   |           21 | 2026-04-30 03:48:09.678000 | 2026-04-30 07:37:56.582000 |
|        20260430033303 | PASSED   |            1 | 2026-04-30 03:33:03.354000 | 2026-04-30 03:33:03.354000 |
|        20260430033301 | PASSED   |            2 | 2026-04-30 03:33:01.104000 | 2026-04-30 03:33:01.734000 |
|        20260430033300 | PASSED   |            1 | 2026-04-30 03:33:00.731000 | 2026-04-30 03:33:00.731000 |
|        20260430033300 | FAILED   |            1 | 2026-04-30 03:33:00.257000 | 2026-04-30 03:33:00.257000 |
|        20260430033257 | PASSED   |            1 | 2026-04-30 03:32:57.062000 | 2026-04-30 03:32:57.062000 |
|        20260430033255 | PASSED   |            2 | 2026-04-30 03:32:55.424000 | 2026-04-30 03:32:55.767000 |

---
## Detailed Data Quality Results

**CSV Export:** `reports/exports/dq_details.csv`

|   VALIDATION_BATCH_ID | RULE_ID   | TARGET_TABLE                     |   TOTAL_RECORDS |   FAILED_RECORDS |   PASSED_RECORDS |   FAILURE_PERCENTAGE | STATUS   | MESSAGE                                              | EXECUTED_TS                |
|----------------------:|:----------|:---------------------------------|----------------:|-----------------:|-----------------:|---------------------:|:---------|:-----------------------------------------------------|:---------------------------|
|        20260502031153 | DQ008     | RAW.RAW_EXTERNAL_PRODUCTS        |            1400 |                0 |                1 |                 0    | PASSED   | External API should return at least one product      | 2026-05-02 03:15:10.496000 |
|        20260502031153 | DQ007     | RAW.RAW_RECOMART_CATEGORY_TREE   |           23366 |                0 |            23366 |                 0    | PASSED   | Category ID should not be null                       | 2026-05-02 03:15:10.164000 |
|        20260502031153 | DQ006     | RAW.RAW_RECOMART_ITEM_PROPERTIES |       283862628 |                0 |        283862628 |                 0    | PASSED   | Item property fields should not be null              | 2026-05-02 03:15:09.696000 |
|        20260502031153 | DQ005     | RAW.RAW_RECOMART_EVENTS          |        38585414 |                0 |         38585414 |                 0    | PASSED   | Transaction events should have transaction_id        | 2026-05-02 03:15:09.065000 |
|        20260502031153 | DQ004     | RAW.RAW_RECOMART_EVENTS          |        38585414 |         35829773 |          2755641 |                92.86 | FAILED   | Duplicate event records should not exist             | 2026-05-02 03:15:07.452000 |
|        20260502031153 | DQ003     | RAW.RAW_RECOMART_EVENTS          |        38585414 |                0 |         38585414 |                 0    | PASSED   | Event type should be view, addtocart, or transaction | 2026-05-02 03:15:06.995000 |
|        20260502031153 | DQ002     | RAW.RAW_RECOMART_EVENTS          |        38585414 |                0 |         38585414 |                 0    | PASSED   | Item ID should not be null                           | 2026-05-02 03:15:06.594000 |
|        20260502031153 | DQ001     | RAW.RAW_RECOMART_EVENTS          |        38585414 |                0 |         38585414 |                 0    | PASSED   | Visitor ID should not be null                        | 2026-05-02 03:15:06.139000 |
|        20260502024231 | DQ008     | RAW.RAW_EXTERNAL_PRODUCTS        |            1000 |                0 |                1 |                 0    | PASSED   | External API should return at least one product      | 2026-05-02 02:45:18.292000 |
|        20260502024231 | DQ007     | RAW.RAW_RECOMART_CATEGORY_TREE   |           16690 |                0 |            16690 |                 0    | PASSED   | Category ID should not be null                       | 2026-05-02 02:45:17.964000 |
|        20260502024231 | DQ006     | RAW.RAW_RECOMART_ITEM_PROPERTIES |       202759020 |                0 |        202759020 |                 0    | PASSED   | Item property fields should not be null              | 2026-05-02 02:45:17.569000 |
|        20260502024231 | DQ005     | RAW.RAW_RECOMART_EVENTS          |        27561010 |                0 |         27561010 |                 0    | PASSED   | Transaction events should have transaction_id        | 2026-05-02 02:45:17.051000 |
|        20260502024231 | DQ004     | RAW.RAW_RECOMART_EVENTS          |        27561010 |         24805369 |          2755641 |                90    | FAILED   | Duplicate event records should not exist             | 2026-05-02 02:45:15.669000 |
|        20260502024231 | DQ003     | RAW.RAW_RECOMART_EVENTS          |        27561010 |                0 |         27561010 |                 0    | PASSED   | Event type should be view, addtocart, or transaction | 2026-05-02 02:45:15.250000 |
|        20260502024231 | DQ002     | RAW.RAW_RECOMART_EVENTS          |        27561010 |                0 |         27561010 |                 0    | PASSED   | Item ID should not be null                           | 2026-05-02 02:45:14.803000 |
|        20260502024231 | DQ001     | RAW.RAW_RECOMART_EVENTS          |        27561010 |                0 |         27561010 |                 0    | PASSED   | Visitor ID should not be null                        | 2026-05-02 02:45:14.200000 |
|        20260430081645 | DQ008     | RAW.RAW_EXTERNAL_PRODUCTS        |             400 |                0 |                1 |                 0    | PASSED   | External API should return at least one product      | 2026-04-30 08:18:38.685000 |
|        20260430081645 | DQ007     | RAW.RAW_RECOMART_CATEGORY_TREE   |            6676 |                0 |             6676 |                 0    | PASSED   | Category ID should not be null                       | 2026-04-30 08:18:38.299000 |
|        20260430081645 | DQ006     | RAW.RAW_RECOMART_ITEM_PROPERTIES |        81103608 |                0 |         81103608 |                 0    | PASSED   | Item property fields should not be null              | 2026-04-30 08:18:37.872000 |
|        20260430081645 | DQ005     | RAW.RAW_RECOMART_EVENTS          |        11024404 |                0 |         11024404 |                 0    | PASSED   | Transaction events should have transaction_id        | 2026-04-30 08:18:37.496000 |
|        20260430081645 | DQ004     | RAW.RAW_RECOMART_EVENTS          |        11024404 |          8268763 |          2755641 |                75    | FAILED   | Duplicate event records should not exist             | 2026-04-30 08:18:36.675000 |
|        20260430081645 | DQ003     | RAW.RAW_RECOMART_EVENTS          |        11024404 |                0 |         11024404 |                 0    | PASSED   | Event type should be view, addtocart, or transaction | 2026-04-30 08:18:36.272000 |
|        20260430081645 | DQ002     | RAW.RAW_RECOMART_EVENTS          |        11024404 |                0 |         11024404 |                 0    | PASSED   | Item ID should not be null                           | 2026-04-30 08:18:35.861000 |
|        20260430081645 | DQ001     | RAW.RAW_RECOMART_EVENTS          |        11024404 |                0 |         11024404 |                 0    | PASSED   | Visitor ID should not be null                        | 2026-04-30 08:18:35.387000 |
|        20260430075931 | DQ008     | RAW.RAW_EXTERNAL_PRODUCTS        |             200 |                0 |                1 |                 0    | PASSED   | External API should return at least one product      | 2026-04-30 08:01:55.415000 |
|        20260430075931 | DQ007     | RAW.RAW_RECOMART_CATEGORY_TREE   |            3338 |                0 |             3338 |                 0    | PASSED   | Category ID should not be null                       | 2026-04-30 08:01:54.459000 |
|        20260430075931 | DQ006     | RAW.RAW_RECOMART_ITEM_PROPERTIES |        40551804 |                0 |         40551804 |                 0    | PASSED   | Item property fields should not be null              | 2026-04-30 08:01:54.064000 |
|        20260430075931 | DQ005     | RAW.RAW_RECOMART_EVENTS          |         5512202 |                0 |          5512202 |                 0    | PASSED   | Transaction events should have transaction_id        | 2026-04-30 08:01:50.703000 |
|        20260430075931 | DQ004     | RAW.RAW_RECOMART_EVENTS          |         5512202 |          2756561 |          2755641 |                50.01 | FAILED   | Duplicate event records should not exist             | 2026-04-30 08:01:49.356000 |
|        20260430075931 | DQ003     | RAW.RAW_RECOMART_EVENTS          |         5512202 |                0 |          5512202 |                 0    | PASSED   | Event type should be view, addtocart, or transaction | 2026-04-30 08:01:44.966000 |
|        20260430075931 | DQ002     | RAW.RAW_RECOMART_EVENTS          |         5512202 |                0 |          5512202 |                 0    | PASSED   | Item ID should not be null                           | 2026-04-30 08:01:44.592000 |
|        20260430075931 | DQ001     | RAW.RAW_RECOMART_EVENTS          |         5512202 |                0 |          5512202 |                 0    | PASSED   | Visitor ID should not be null                        | 2026-04-30 08:01:40.772000 |
|        20260430030321 | DQ008     | RAW.RAW_EXTERNAL_PRODUCTS        |             100 |                0 |                1 |                 0    | PASSED   | External API should return at least one product      | 2026-04-30 07:37:56.582000 |
|        20260430030321 | DQ007     | RAW.RAW_RECOMART_CATEGORY_TREE   |            1669 |                0 |             1669 |                 0    | PASSED   | Category ID should not be null                       | 2026-04-30 07:37:52.224000 |
|        20260430030321 | DQ006     | RAW.RAW_RECOMART_ITEM_PROPERTIES |        20275902 |                0 |         20275902 |                 0    | PASSED   | Item property fields should not be null              | 2026-04-30 07:37:46.212000 |
|        20260430030321 | DQ005     | RAW.RAW_RECOMART_EVENTS          |         2756101 |                0 |          2756101 |                 0    | PASSED   | Transaction events should have transaction_id        | 2026-04-30 07:37:45.851000 |
|        20260430030321 | DQ004     | RAW.RAW_RECOMART_EVENTS          |         2756101 |              460 |          2755641 |                 0.02 | FAILED   | Duplicate event records should not exist             | 2026-04-30 07:37:42.053000 |
|        20260430030321 | DQ003     | RAW.RAW_RECOMART_EVENTS          |         2756101 |                0 |          2756101 |                 0    | PASSED   | Event type should be view, addtocart, or transaction | 2026-04-30 07:37:41.602000 |
|        20260430030321 | DQ002     | RAW.RAW_RECOMART_EVENTS          |         2756101 |                0 |          2756101 |                 0    | PASSED   | Item ID should not be null                           | 2026-04-30 07:37:35.235000 |
|        20260430030321 | DQ001     | RAW.RAW_RECOMART_EVENTS          |         2756101 |                0 |          2756101 |                 0    | PASSED   | Visitor ID should not be null                        | 2026-04-30 07:37:34.796000 |
|        20260430030321 | DQ008     | RAW.RAW_EXTERNAL_PRODUCTS        |             100 |                0 |                1 |                 0    | PASSED   | External API should return at least one product      | 2026-04-30 05:05:35.613000 |
|        20260430030321 | DQ007     | RAW.RAW_RECOMART_CATEGORY_TREE   |            1669 |                0 |             1669 |                 0    | PASSED   | Category ID should not be null                       | 2026-04-30 05:05:31.956000 |
|        20260430030321 | DQ006     | RAW.RAW_RECOMART_ITEM_PROPERTIES |        20275902 |                0 |         20275902 |                 0    | PASSED   | Item property fields should not be null              | 2026-04-30 05:05:31.193000 |
|        20260430030321 | DQ005     | RAW.RAW_RECOMART_EVENTS          |         2756101 |                0 |          2756101 |                 0    | PASSED   | Transaction events should have transaction_id        | 2026-04-30 05:05:30.498000 |
|        20260430030321 | DQ004     | RAW.RAW_RECOMART_EVENTS          |         2756101 |              460 |          2755641 |                 0.02 | FAILED   | Duplicate event records should not exist             | 2026-04-30 05:05:29.991000 |
|        20260430030321 | DQ003     | RAW.RAW_RECOMART_EVENTS          |         2756101 |                0 |          2756101 |                 0    | PASSED   | Event type should be view, addtocart, or transaction | 2026-04-30 05:05:29.599000 |
|        20260430030321 | DQ002     | RAW.RAW_RECOMART_EVENTS          |         2756101 |                0 |          2756101 |                 0    | PASSED   | Item ID should not be null                           | 2026-04-30 05:05:28.173000 |
|        20260430030321 | DQ001     | RAW.RAW_RECOMART_EVENTS          |         2756101 |                0 |          2756101 |                 0    | PASSED   | Visitor ID should not be null                        | 2026-04-30 05:05:27.769000 |
|        20260430030321 | DQ008     | RAW.RAW_EXTERNAL_PRODUCTS        |             100 |                0 |                1 |                 0    | PASSED   | External API should return at least one product      | 2026-04-30 03:48:16.969000 |
|        20260430030321 | DQ007     | RAW.RAW_RECOMART_CATEGORY_TREE   |            1669 |                0 |             1669 |                 0    | PASSED   | Category ID should not be null                       | 2026-04-30 03:48:14.981000 |
|        20260430030321 | DQ006     | RAW.RAW_RECOMART_ITEM_PROPERTIES |        20275902 |                0 |         20275902 |                 0    | PASSED   | Item property fields should not be null              | 2026-04-30 03:48:14.348000 |
|        20260430030321 | DQ005     | RAW.RAW_RECOMART_EVENTS          |         2756101 |                0 |          2756101 |                 0    | PASSED   | Transaction events should have transaction_id        | 2026-04-30 03:48:13.980000 |
|        20260430030321 | DQ004     | RAW.RAW_RECOMART_EVENTS          |         2756101 |              460 |          2755641 |                 0.02 | FAILED   | Duplicate event records should not exist             | 2026-04-30 03:48:10.701000 |
|        20260430030321 | DQ003     | RAW.RAW_RECOMART_EVENTS          |         2756101 |                0 |          2756101 |                 0    | PASSED   | Event type should be view, addtocart, or transaction | 2026-04-30 03:48:10.322000 |
|        20260430030321 | DQ002     | RAW.RAW_RECOMART_EVENTS          |         2756101 |                0 |          2756101 |                 0    | PASSED   | Item ID should not be null                           | 2026-04-30 03:48:09.980000 |
|        20260430030321 | DQ001     | RAW.RAW_RECOMART_EVENTS          |         2756101 |                0 |          2756101 |                 0    | PASSED   | Visitor ID should not be null                        | 2026-04-30 03:48:09.678000 |
|        20260430033303 | DQ008     | RAW.RAW_EXTERNAL_PRODUCTS        |             100 |                0 |                1 |                 0    | PASSED   | External API should return at least one product      | 2026-04-30 03:33:03.354000 |
|        20260430033301 | DQ007     | RAW.RAW_RECOMART_CATEGORY_TREE   |            1669 |                0 |             1669 |                 0    | PASSED   | Category ID should not be null                       | 2026-04-30 03:33:01.734000 |
|        20260430033301 | DQ006     | RAW.RAW_RECOMART_ITEM_PROPERTIES |        20275902 |                0 |         20275902 |                 0    | PASSED   | Item property fields should not be null              | 2026-04-30 03:33:01.104000 |
|        20260430033300 | DQ005     | RAW.RAW_RECOMART_EVENTS          |         2756101 |                0 |          2756101 |                 0    | PASSED   | Transaction events should have transaction_id        | 2026-04-30 03:33:00.731000 |
|        20260430033300 | DQ004     | RAW.RAW_RECOMART_EVENTS          |         2756101 |              460 |          2755641 |                 0.02 | FAILED   | Duplicate event records should not exist             | 2026-04-30 03:33:00.257000 |
|        20260430033257 | DQ003     | RAW.RAW_RECOMART_EVENTS          |         2756101 |                0 |          2756101 |                 0    | PASSED   | Event type should be view, addtocart, or transaction | 2026-04-30 03:32:57.062000 |
|        20260430033255 | DQ002     | RAW.RAW_RECOMART_EVENTS          |         2756101 |                0 |          2756101 |                 0    | PASSED   | Item ID should not be null                           | 2026-04-30 03:32:55.767000 |
|        20260430033255 | DQ001     | RAW.RAW_RECOMART_EVENTS          |         2756101 |                0 |          2756101 |                 0    | PASSED   | Visitor ID should not be null                        | 2026-04-30 03:32:55.424000 |

---
## Validated Event Quality

**CSV Export:** `reports/exports/validated_event_quality.csv`

|   VALIDATION_BATCH_ID | VALIDATION_RUN_TS          | IS_VALID   | VALIDATION_MESSAGE     |   RECORD_COUNT |
|----------------------:|:---------------------------|:-----------|:-----------------------|---------------:|
|        20260502031153 | 2026-05-02 03:12:36.485000 | False      | Duplicate event record |       35829773 |
|        20260502031153 | 2026-05-02 03:12:36.485000 | True       | Valid record           |        2755641 |

---
