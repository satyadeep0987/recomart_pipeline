USE ROLE ACCOUNTADMIN;
USE DATABASE RECOMART_DB;

-- ============================================================
-- Profile raw events
-- ============================================================

SELECT
    COUNT(*) AS TOTAL_RECORDS,
    COUNT(DISTINCT VISITOR_ID) AS UNIQUE_USERS,
    COUNT(DISTINCT ITEM_ID) AS UNIQUE_ITEMS,
    MIN(EVENT_TIMESTAMP_MS) AS MIN_EVENT_TIMESTAMP_MS,
    MAX(EVENT_TIMESTAMP_MS) AS MAX_EVENT_TIMESTAMP_MS,
    COUNT_IF(VISITOR_ID IS NULL) AS NULL_VISITOR_ID_COUNT,
    COUNT_IF(ITEM_ID IS NULL) AS NULL_ITEM_ID_COUNT,
    COUNT_IF(EVENT_TYPE IS NULL) AS NULL_EVENT_TYPE_COUNT,
    COUNT_IF(EVENT_TIMESTAMP_MS IS NULL) AS NULL_TIMESTAMP_COUNT
FROM RAW.RAW_RECOMART_EVENTS;


-- ============================================================
-- Event type distribution
-- ============================================================

SELECT
    EVENT_TYPE,
    COUNT(*) AS EVENT_COUNT,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS PERCENTAGE
FROM RAW.RAW_RECOMART_EVENTS
GROUP BY EVENT_TYPE
ORDER BY EVENT_COUNT DESC;


-- ============================================================
-- Duplicate event check
-- ============================================================

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
ORDER BY DUPLICATE_COUNT DESC
LIMIT 50;


-- ============================================================
-- Profile item properties
-- ============================================================

SELECT
    COUNT(*) AS TOTAL_RECORDS,
    COUNT(DISTINCT ITEM_ID) AS UNIQUE_ITEMS,
    COUNT(DISTINCT PROPERTY_NAME) AS UNIQUE_PROPERTIES,
    COUNT_IF(ITEM_ID IS NULL) AS NULL_ITEM_ID_COUNT,
    COUNT_IF(PROPERTY_NAME IS NULL) AS NULL_PROPERTY_NAME_COUNT,
    COUNT_IF(PROPERTY_VALUE IS NULL) AS NULL_PROPERTY_VALUE_COUNT,
    MIN(PROPERTY_TIMESTAMP_MS) AS MIN_PROPERTY_TIMESTAMP_MS,
    MAX(PROPERTY_TIMESTAMP_MS) AS MAX_PROPERTY_TIMESTAMP_MS
FROM RAW.RAW_RECOMART_ITEM_PROPERTIES;


-- ============================================================
-- Profile category tree
-- ============================================================

SELECT
    COUNT(*) AS TOTAL_CATEGORIES,
    COUNT(DISTINCT CATEGORY_ID) AS UNIQUE_CATEGORIES,
    COUNT_IF(CATEGORY_ID IS NULL) AS NULL_CATEGORY_ID_COUNT,
    COUNT_IF(PARENT_CATEGORY_ID IS NULL) AS ROOT_CATEGORY_COUNT
FROM RAW.RAW_RECOMART_CATEGORY_TREE;


-- ============================================================
-- Profile external API JSON
-- ============================================================

SELECT
    COUNT(*) AS RAW_JSON_FILES,
    COUNT(product.value:id) AS TOTAL_PRODUCTS
FROM RAW.RAW_EXTERNAL_PRODUCTS,
LATERAL FLATTEN(INPUT => PRODUCT_JSON:products) product;