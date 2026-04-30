USE ROLE ACCOUNTADMIN;
USE DATABASE RECOMART_DB;

-- ============================================================
-- DQ001: visitor_id should not be null
-- ============================================================

INSERT INTO OPS.DATA_QUALITY_RESULTS (
    RESULT_ID,
    BATCH_ID,
    RULE_ID,
    TARGET_TABLE,
    TOTAL_RECORDS,
    FAILED_RECORDS,
    PASSED_RECORDS,
    FAILURE_PERCENTAGE,
    STATUS,
    MESSAGE
)
SELECT
    UUID_STRING(),
    $VALIDATION_BATCH_ID,
    'DQ001',
    'RAW.RAW_RECOMART_EVENTS',
    COUNT(*),
    COUNT_IF(VISITOR_ID IS NULL),
    COUNT(*) - COUNT_IF(VISITOR_ID IS NULL),
    ROUND(COUNT_IF(VISITOR_ID IS NULL) * 100.0 / NULLIF(COUNT(*), 0), 2),
    CASE WHEN COUNT_IF(VISITOR_ID IS NULL) = 0 THEN 'PASSED' ELSE 'FAILED' END,
    'Visitor ID should not be null'
FROM RAW.RAW_RECOMART_EVENTS;


-- ============================================================
-- DQ002: item_id should not be null
-- ============================================================

INSERT INTO OPS.DATA_QUALITY_RESULTS (
    RESULT_ID,
    BATCH_ID,
    RULE_ID,
    TARGET_TABLE,
    TOTAL_RECORDS,
    FAILED_RECORDS,
    PASSED_RECORDS,
    FAILURE_PERCENTAGE,
    STATUS,
    MESSAGE
)
SELECT
    UUID_STRING(),
    $VALIDATION_BATCH_ID,
    'DQ002',
    'RAW.RAW_RECOMART_EVENTS',
    COUNT(*),
    COUNT_IF(ITEM_ID IS NULL),
    COUNT(*) - COUNT_IF(ITEM_ID IS NULL),
    ROUND(COUNT_IF(ITEM_ID IS NULL) * 100.0 / NULLIF(COUNT(*), 0), 2),
    CASE WHEN COUNT_IF(ITEM_ID IS NULL) = 0 THEN 'PASSED' ELSE 'FAILED' END,
    'Item ID should not be null'
FROM RAW.RAW_RECOMART_EVENTS;


-- ============================================================
-- DQ003: event_type should be valid
-- ============================================================

INSERT INTO OPS.DATA_QUALITY_RESULTS (
    RESULT_ID,
    BATCH_ID,
    RULE_ID,
    TARGET_TABLE,
    TOTAL_RECORDS,
    FAILED_RECORDS,
    PASSED_RECORDS,
    FAILURE_PERCENTAGE,
    STATUS,
    MESSAGE
)
SELECT
    UUID_STRING(),
    $VALIDATION_BATCH_ID,
    'DQ003',
    'RAW.RAW_RECOMART_EVENTS',
    COUNT(*),
    COUNT_IF(EVENT_TYPE NOT IN ('view', 'addtocart', 'transaction') OR EVENT_TYPE IS NULL),
    COUNT(*) - COUNT_IF(EVENT_TYPE NOT IN ('view', 'addtocart', 'transaction') OR EVENT_TYPE IS NULL),
    ROUND(
        COUNT_IF(EVENT_TYPE NOT IN ('view', 'addtocart', 'transaction') OR EVENT_TYPE IS NULL) * 100.0 / NULLIF(COUNT(*), 0),
        2
    ),
    CASE
        WHEN COUNT_IF(EVENT_TYPE NOT IN ('view', 'addtocart', 'transaction') OR EVENT_TYPE IS NULL) = 0 THEN 'PASSED'
        ELSE 'FAILED'
    END,
    'Event type should be view, addtocart, or transaction'
FROM RAW.RAW_RECOMART_EVENTS;


-- ============================================================
-- DQ004: duplicate event records
-- ============================================================

INSERT INTO OPS.DATA_QUALITY_RESULTS (
    RESULT_ID,
    BATCH_ID,
    RULE_ID,
    TARGET_TABLE,
    TOTAL_RECORDS,
    FAILED_RECORDS,
    PASSED_RECORDS,
    FAILURE_PERCENTAGE,
    STATUS,
    MESSAGE
)
WITH duplicate_events AS (
    SELECT
        EVENT_TIMESTAMP_MS,
        VISITOR_ID,
        EVENT_TYPE,
        ITEM_ID,
        TRANSACTION_ID,
        COUNT(*) AS DUPLICATE_COUNT
    FROM RAW.RAW_RECOMART_EVENTS
    GROUP BY
        EVENT_TIMESTAMP_MS,
        VISITOR_ID,
        EVENT_TYPE,
        ITEM_ID,
        TRANSACTION_ID
    HAVING COUNT(*) > 1
),
summary AS (
    SELECT
        (SELECT COUNT(*) FROM RAW.RAW_RECOMART_EVENTS) AS TOTAL_RECORDS,
        COALESCE(SUM(DUPLICATE_COUNT - 1), 0) AS FAILED_RECORDS
    FROM duplicate_events
)
SELECT
    UUID_STRING(),
    $VALIDATION_BATCH_ID,
    'DQ004',
    'RAW.RAW_RECOMART_EVENTS',
    TOTAL_RECORDS,
    FAILED_RECORDS,
    TOTAL_RECORDS - FAILED_RECORDS,
    ROUND(FAILED_RECORDS * 100.0 / NULLIF(TOTAL_RECORDS, 0), 2),
    CASE WHEN FAILED_RECORDS = 0 THEN 'PASSED' ELSE 'FAILED' END,
    'Duplicate event records should not exist'
FROM summary;


-- ============================================================
-- DQ005: transaction events should have transaction_id
-- ============================================================

INSERT INTO OPS.DATA_QUALITY_RESULTS (
    RESULT_ID,
    BATCH_ID,
    RULE_ID,
    TARGET_TABLE,
    TOTAL_RECORDS,
    FAILED_RECORDS,
    PASSED_RECORDS,
    FAILURE_PERCENTAGE,
    STATUS,
    MESSAGE
)
SELECT
    UUID_STRING(),
    $VALIDATION_BATCH_ID,
    'DQ005',
    'RAW.RAW_RECOMART_EVENTS',
    COUNT(*),
    COUNT_IF(EVENT_TYPE = 'transaction' AND TRANSACTION_ID IS NULL),
    COUNT(*) - COUNT_IF(EVENT_TYPE = 'transaction' AND TRANSACTION_ID IS NULL),
    ROUND(
        COUNT_IF(EVENT_TYPE = 'transaction' AND TRANSACTION_ID IS NULL) * 100.0 / NULLIF(COUNT(*), 0),
        2
    ),
    CASE
        WHEN COUNT_IF(EVENT_TYPE = 'transaction' AND TRANSACTION_ID IS NULL) = 0 THEN 'PASSED'
        ELSE 'FAILED'
    END,
    'Transaction events should have transaction_id'
FROM RAW.RAW_RECOMART_EVENTS;


-- ============================================================
-- DQ006: item property mandatory fields
-- ============================================================

INSERT INTO OPS.DATA_QUALITY_RESULTS (
    RESULT_ID,
    BATCH_ID,
    RULE_ID,
    TARGET_TABLE,
    TOTAL_RECORDS,
    FAILED_RECORDS,
    PASSED_RECORDS,
    FAILURE_PERCENTAGE,
    STATUS,
    MESSAGE
)
SELECT
    UUID_STRING(),
    $VALIDATION_BATCH_ID,
    'DQ006',
    'RAW.RAW_RECOMART_ITEM_PROPERTIES',
    COUNT(*),
    COUNT_IF(ITEM_ID IS NULL OR PROPERTY_NAME IS NULL OR PROPERTY_VALUE IS NULL),
    COUNT(*) - COUNT_IF(ITEM_ID IS NULL OR PROPERTY_NAME IS NULL OR PROPERTY_VALUE IS NULL),
    ROUND(
        COUNT_IF(ITEM_ID IS NULL OR PROPERTY_NAME IS NULL OR PROPERTY_VALUE IS NULL) * 100.0 / NULLIF(COUNT(*), 0),
        2
    ),
    CASE
        WHEN COUNT_IF(ITEM_ID IS NULL OR PROPERTY_NAME IS NULL OR PROPERTY_VALUE IS NULL) = 0 THEN 'PASSED'
        ELSE 'FAILED'
    END,
    'Item property fields should not be null'
FROM RAW.RAW_RECOMART_ITEM_PROPERTIES;


-- ============================================================
-- DQ007: category_id should not be null
-- ============================================================

INSERT INTO OPS.DATA_QUALITY_RESULTS (
    RESULT_ID,
    BATCH_ID,
    RULE_ID,
    TARGET_TABLE,
    TOTAL_RECORDS,
    FAILED_RECORDS,
    PASSED_RECORDS,
    FAILURE_PERCENTAGE,
    STATUS,
    MESSAGE
)
SELECT
    UUID_STRING(),
    $VALIDATION_BATCH_ID,
    'DQ007',
    'RAW.RAW_RECOMART_CATEGORY_TREE',
    COUNT(*),
    COUNT_IF(CATEGORY_ID IS NULL),
    COUNT(*) - COUNT_IF(CATEGORY_ID IS NULL),
    ROUND(COUNT_IF(CATEGORY_ID IS NULL) * 100.0 / NULLIF(COUNT(*), 0), 2),
    CASE WHEN COUNT_IF(CATEGORY_ID IS NULL) = 0 THEN 'PASSED' ELSE 'FAILED' END,
    'Category ID should not be null'
FROM RAW.RAW_RECOMART_CATEGORY_TREE;


-- ============================================================
-- DQ008: external API should return product records
-- ============================================================

INSERT INTO OPS.DATA_QUALITY_RESULTS (
    RESULT_ID,
    BATCH_ID,
    RULE_ID,
    TARGET_TABLE,
    TOTAL_RECORDS,
    FAILED_RECORDS,
    PASSED_RECORDS,
    FAILURE_PERCENTAGE,
    STATUS,
    MESSAGE
)
WITH external_product_summary AS (
    SELECT
        COUNT(product.value:id) AS PRODUCT_COUNT
    FROM RAW.RAW_EXTERNAL_PRODUCTS,
    LATERAL FLATTEN(INPUT => PRODUCT_JSON:products) product
)
SELECT
    UUID_STRING(),
    $VALIDATION_BATCH_ID,
    'DQ008',
    'RAW.RAW_EXTERNAL_PRODUCTS',
    PRODUCT_COUNT,
    CASE WHEN PRODUCT_COUNT = 0 THEN 1 ELSE 0 END,
    CASE WHEN PRODUCT_COUNT > 0 THEN 1 ELSE 0 END,
    CASE WHEN PRODUCT_COUNT = 0 THEN 100 ELSE 0 END,
    CASE WHEN PRODUCT_COUNT > 0 THEN 'PASSED' ELSE 'FAILED' END,
    'External API should return at least one product'
FROM external_product_summary;