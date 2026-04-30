USE ROLE ACCOUNTADMIN;
USE DATABASE RECOMART_DB;

SET VALIDATION_BATCH_ID = (
    SELECT BATCH_ID
    FROM RAW.RAW_RECOMART_EVENTS
    WHERE BATCH_ID IS NOT NULL
    ORDER BY LOAD_TS DESC
    LIMIT 1
);

SET VALIDATION_RUN_TS = CURRENT_TIMESTAMP();

SELECT
    $VALIDATION_BATCH_ID AS VALIDATION_BATCH_ID,
    $VALIDATION_RUN_TS AS VALIDATION_RUN_TS;

-- ============================================================
-- Clear previous validated data
-- ============================================================

TRUNCATE TABLE VALIDATED.RECOMART_EVENTS;
TRUNCATE TABLE VALIDATED.RECOMART_ITEM_PROPERTIES;
TRUNCATE TABLE VALIDATED.RECOMART_CATEGORY_TREE;
TRUNCATE TABLE VALIDATED.EXTERNAL_PRODUCTS;


-- ============================================================
-- Validate RecoMart events
-- ============================================================

INSERT INTO VALIDATED.RECOMART_EVENTS (
    EVENT_ID,
    EVENT_TIMESTAMP_MS,
    EVENT_TS,
    VISITOR_ID,
    EVENT_TYPE,
    ITEM_ID,
    TRANSACTION_ID,
    IS_VALID,
    VALIDATION_MESSAGE,
    SOURCE_FILE_NAME,
    INGESTION_DATE,
    LOAD_TS,
    VALIDATION_BATCH_ID,
    VALIDATION_RUN_TS,
    VALIDATED_BY
)
WITH event_base AS (
    SELECT
        SHA2(
            CONCAT_WS(
                '|',
                COALESCE(TO_VARCHAR(EVENT_TIMESTAMP_MS), ''),
                COALESCE(TO_VARCHAR(VISITOR_ID), ''),
                COALESCE(EVENT_TYPE, ''),
                COALESCE(TO_VARCHAR(ITEM_ID), ''),
                COALESCE(TO_VARCHAR(TRANSACTION_ID), '')
            ),
            256
        ) AS EVENT_ID,

        EVENT_TIMESTAMP_MS,
        TO_TIMESTAMP_NTZ(EVENT_TIMESTAMP_MS / 1000) AS EVENT_TS,
        VISITOR_ID,
        EVENT_TYPE,
        ITEM_ID,
        TRANSACTION_ID,
        SOURCE_FILE_NAME,
        INGESTION_DATE,
        LOAD_TS,

        ROW_NUMBER() OVER (
            PARTITION BY
                EVENT_TIMESTAMP_MS,
                VISITOR_ID,
                EVENT_TYPE,
                ITEM_ID,
                TRANSACTION_ID
            ORDER BY LOAD_TS
        ) AS DUPLICATE_RANK
    FROM RAW.RAW_RECOMART_EVENTS
)
SELECT
    EVENT_ID,
    EVENT_TIMESTAMP_MS,
    EVENT_TS,
    VISITOR_ID,
    EVENT_TYPE,
    ITEM_ID,
    TRANSACTION_ID,

    CASE
        WHEN EVENT_TIMESTAMP_MS IS NULL THEN FALSE
        WHEN VISITOR_ID IS NULL THEN FALSE
        WHEN ITEM_ID IS NULL THEN FALSE
        WHEN EVENT_TYPE IS NULL THEN FALSE
        WHEN EVENT_TYPE NOT IN ('view', 'addtocart', 'transaction') THEN FALSE
        WHEN EVENT_TYPE = 'transaction' AND TRANSACTION_ID IS NULL THEN FALSE
        WHEN DUPLICATE_RANK > 1 THEN FALSE
        ELSE TRUE
    END AS IS_VALID,

    CASE
        WHEN EVENT_TIMESTAMP_MS IS NULL THEN 'Missing event timestamp'
        WHEN VISITOR_ID IS NULL THEN 'Missing visitor_id'
        WHEN ITEM_ID IS NULL THEN 'Missing item_id'
        WHEN EVENT_TYPE IS NULL THEN 'Missing event_type'
        WHEN EVENT_TYPE NOT IN ('view', 'addtocart', 'transaction') THEN 'Invalid event_type'
        WHEN EVENT_TYPE = 'transaction' AND TRANSACTION_ID IS NULL THEN 'Transaction event missing transaction_id'
        WHEN DUPLICATE_RANK > 1 THEN 'Duplicate event record'
        ELSE 'Valid record'
    END AS VALIDATION_MESSAGE,

    SOURCE_FILE_NAME,
    INGESTION_DATE,
    LOAD_TS,
    $VALIDATION_BATCH_ID AS VALIDATION_BATCH_ID,
    $VALIDATION_RUN_TS AS VALIDATION_RUN_TS,
    CURRENT_USER() AS VALIDATED_BY
FROM event_base;


-- ============================================================
-- Validate RecoMart item properties
-- ============================================================

INSERT INTO VALIDATED.RECOMART_ITEM_PROPERTIES (
    ITEM_PROPERTY_ID,
    PROPERTY_TIMESTAMP_MS,
    PROPERTY_TS,
    ITEM_ID,
    PROPERTY_NAME,
    PROPERTY_VALUE,
    IS_VALID,
    VALIDATION_MESSAGE,
    SOURCE_FILE_NAME,
    INGESTION_DATE,
    LOAD_TS,
    VALIDATION_BATCH_ID,
    VALIDATION_RUN_TS,
    VALIDATED_BY
)
WITH property_base AS (
    SELECT
        SHA2(
            CONCAT_WS(
                '|',
                COALESCE(TO_VARCHAR(PROPERTY_TIMESTAMP_MS), ''),
                COALESCE(TO_VARCHAR(ITEM_ID), ''),
                COALESCE(PROPERTY_NAME, ''),
                COALESCE(PROPERTY_VALUE, '')
            ),
            256
        ) AS ITEM_PROPERTY_ID,

        PROPERTY_TIMESTAMP_MS,
        TO_TIMESTAMP_NTZ(PROPERTY_TIMESTAMP_MS / 1000) AS PROPERTY_TS,
        ITEM_ID,
        PROPERTY_NAME,
        PROPERTY_VALUE,
        SOURCE_FILE_NAME,
        INGESTION_DATE,
        LOAD_TS,

        ROW_NUMBER() OVER (
            PARTITION BY
                PROPERTY_TIMESTAMP_MS,
                ITEM_ID,
                PROPERTY_NAME,
                PROPERTY_VALUE
            ORDER BY LOAD_TS
        ) AS DUPLICATE_RANK
    FROM RAW.RAW_RECOMART_ITEM_PROPERTIES
)
SELECT
    ITEM_PROPERTY_ID,
    PROPERTY_TIMESTAMP_MS,
    PROPERTY_TS,
    ITEM_ID,
    PROPERTY_NAME,
    PROPERTY_VALUE,

    CASE
        WHEN PROPERTY_TIMESTAMP_MS IS NULL THEN FALSE
        WHEN ITEM_ID IS NULL THEN FALSE
        WHEN PROPERTY_NAME IS NULL THEN FALSE
        WHEN PROPERTY_VALUE IS NULL THEN FALSE
        WHEN DUPLICATE_RANK > 1 THEN FALSE
        ELSE TRUE
    END AS IS_VALID,

    CASE
        WHEN PROPERTY_TIMESTAMP_MS IS NULL THEN 'Missing property timestamp'
        WHEN ITEM_ID IS NULL THEN 'Missing item_id'
        WHEN PROPERTY_NAME IS NULL THEN 'Missing property_name'
        WHEN PROPERTY_VALUE IS NULL THEN 'Missing property_value'
        WHEN DUPLICATE_RANK > 1 THEN 'Duplicate item property record'
        ELSE 'Valid record'
    END AS VALIDATION_MESSAGE,

    SOURCE_FILE_NAME,
    INGESTION_DATE,
    LOAD_TS,
    $VALIDATION_BATCH_ID AS VALIDATION_BATCH_ID,
    $VALIDATION_RUN_TS AS VALIDATION_RUN_TS,
    CURRENT_USER() AS VALIDATED_BY
FROM property_base;


-- ============================================================
-- Validate RecoMart category tree
-- ============================================================

INSERT INTO VALIDATED.RECOMART_CATEGORY_TREE (
    CATEGORY_ID,
    PARENT_CATEGORY_ID,
    IS_VALID,
    VALIDATION_MESSAGE,
    SOURCE_FILE_NAME,
    INGESTION_DATE,
    LOAD_TS,
    VALIDATION_BATCH_ID,
    VALIDATION_RUN_TS,
    VALIDATED_BY
)
WITH category_base AS (
    SELECT
        CATEGORY_ID,
        PARENT_CATEGORY_ID,
        SOURCE_FILE_NAME,
        INGESTION_DATE,
        LOAD_TS,

        ROW_NUMBER() OVER (
            PARTITION BY CATEGORY_ID, PARENT_CATEGORY_ID
            ORDER BY LOAD_TS
        ) AS DUPLICATE_RANK
    FROM RAW.RAW_RECOMART_CATEGORY_TREE
)
SELECT
    CATEGORY_ID,
    PARENT_CATEGORY_ID,

    CASE
        WHEN CATEGORY_ID IS NULL THEN FALSE
        WHEN DUPLICATE_RANK > 1 THEN FALSE
        ELSE TRUE
    END AS IS_VALID,

    CASE
        WHEN CATEGORY_ID IS NULL THEN 'Missing category_id'
        WHEN DUPLICATE_RANK > 1 THEN 'Duplicate category record'
        ELSE 'Valid record'
    END AS VALIDATION_MESSAGE,

    SOURCE_FILE_NAME,
    INGESTION_DATE,
    LOAD_TS,
    $VALIDATION_BATCH_ID AS VALIDATION_BATCH_ID,
    $VALIDATION_RUN_TS AS VALIDATION_RUN_TS,
    CURRENT_USER() AS VALIDATED_BY
FROM category_base;


-- ============================================================
-- Validate external product API data
-- ============================================================

INSERT INTO VALIDATED.EXTERNAL_PRODUCTS (
    PRODUCT_ID,
    PRODUCT_TITLE,
    PRODUCT_DESCRIPTION,
    CATEGORY,
    PRICE,
    RATING,
    STOCK,
    BRAND,
    PRODUCT_JSON,
    SOURCE_SYSTEM,
    SOURCE_FILE_NAME,
    INGESTION_DATE,
    LOAD_TS,
    VALIDATION_BATCH_ID,
    VALIDATION_RUN_TS,
    VALIDATED_BY
)
SELECT
    product.value:id::NUMBER AS PRODUCT_ID,
    product.value:title::VARCHAR AS PRODUCT_TITLE,
    product.value:description::VARCHAR AS PRODUCT_DESCRIPTION,
    product.value:category::VARCHAR AS CATEGORY,
    product.value:price::FLOAT AS PRICE,
    product.value:rating::FLOAT AS RATING,
    product.value:stock::NUMBER AS STOCK,
    product.value:brand::VARCHAR AS BRAND,
    product.value AS PRODUCT_JSON,
    SOURCE_SYSTEM,
    SOURCE_FILE_NAME,
    INGESTION_DATE,
    LOAD_TS,
    $VALIDATION_BATCH_ID AS VALIDATION_BATCH_ID,
    $VALIDATION_RUN_TS AS VALIDATION_RUN_TS,
    CURRENT_USER() AS VALIDATED_BY
FROM RAW.RAW_EXTERNAL_PRODUCTS,
LATERAL FLATTEN(INPUT => PRODUCT_JSON:products) product
WHERE product.value:id IS NOT NULL;