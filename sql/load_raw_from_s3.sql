USE ROLE ACCOUNTADMIN;
USE WAREHOUSE COMPUTE_WH;
USE DATABASE RECOMART_DB;
USE SCHEMA RAW;

-- ============================================================
-- RecoMart Automated S3 to Snowflake RAW Load
-- This batch ID is used for all RAW tables in one pipeline run.
-- ============================================================

SET LOAD_BATCH_ID = TO_VARCHAR(CURRENT_TIMESTAMP(), 'YYYYMMDDHH24MISS');

SELECT
    $LOAD_BATCH_ID AS CURRENT_LOAD_BATCH_ID;


-- ============================================================
-- 1. Load RecoMart Events
-- Source:
-- s3://recomartdatalake/raw/recomart/events/
-- Target:
-- RECOMART_DB.RAW.RAW_RECOMART_EVENTS
-- ============================================================

COPY INTO RAW.RAW_RECOMART_EVENTS (
    EVENT_TIMESTAMP_MS,
    VISITOR_ID,
    EVENT_TYPE,
    ITEM_ID,
    TRANSACTION_ID,
    SOURCE_FILE_NAME,
    INGESTION_DATE,
    BATCH_ID
)
FROM (
    SELECT
        TRY_TO_NUMBER($1) AS EVENT_TIMESTAMP_MS,
        TRY_TO_NUMBER($2) AS VISITOR_ID,
        $3::VARCHAR AS EVENT_TYPE,
        TRY_TO_NUMBER($4) AS ITEM_ID,
        TRY_TO_NUMBER($5) AS TRANSACTION_ID,
        METADATA$FILENAME AS SOURCE_FILE_NAME,
        TRY_TO_DATE(
            REGEXP_SUBSTR(
                METADATA$FILENAME,
                'ingestion_date=([0-9]{4}-[0-9]{2}-[0-9]{2})',
                1,
                1,
                'e',
                1
            )
        ) AS INGESTION_DATE,
        $LOAD_BATCH_ID AS BATCH_ID
    FROM @RAW.RECOMART_S3_STAGE/raw/recomart/events/
)
FILE_FORMAT = RAW.CSV_FILE_FORMAT
PATTERN = '.*events.*[.]csv'
ON_ERROR = 'CONTINUE'
FORCE = TRUE;


-- ============================================================
-- 2. Load RecoMart Item Properties
-- Source:
-- s3://recomartdatalake/raw/recomart/item_properties/
-- Target:
-- RECOMART_DB.RAW.RAW_RECOMART_ITEM_PROPERTIES
-- ============================================================

COPY INTO RAW.RAW_RECOMART_ITEM_PROPERTIES (
    PROPERTY_TIMESTAMP_MS,
    ITEM_ID,
    PROPERTY_NAME,
    PROPERTY_VALUE,
    SOURCE_FILE_NAME,
    INGESTION_DATE,
    BATCH_ID
)
FROM (
    SELECT
        TRY_TO_NUMBER($1) AS PROPERTY_TIMESTAMP_MS,
        TRY_TO_NUMBER($2) AS ITEM_ID,
        $3::VARCHAR AS PROPERTY_NAME,
        $4::VARCHAR AS PROPERTY_VALUE,
        METADATA$FILENAME AS SOURCE_FILE_NAME,
        TRY_TO_DATE(
            REGEXP_SUBSTR(
                METADATA$FILENAME,
                'ingestion_date=([0-9]{4}-[0-9]{2}-[0-9]{2})',
                1,
                1,
                'e',
                1
            )
        ) AS INGESTION_DATE,
        $LOAD_BATCH_ID AS BATCH_ID
    FROM @RAW.RECOMART_S3_STAGE/raw/recomart/item_properties/
)
FILE_FORMAT = RAW.CSV_FILE_FORMAT
PATTERN = '.*item_properties.*[.]csv'
ON_ERROR = 'CONTINUE'
FORCE = TRUE;


-- ============================================================
-- 3. Load RecoMart Category Tree
-- Source:
-- s3://recomartdatalake/raw/recomart/category_tree/
-- Target:
-- RECOMART_DB.RAW.RAW_RECOMART_CATEGORY_TREE
-- ============================================================

COPY INTO RAW.RAW_RECOMART_CATEGORY_TREE (
    CATEGORY_ID,
    PARENT_CATEGORY_ID,
    SOURCE_FILE_NAME,
    INGESTION_DATE,
    BATCH_ID
)
FROM (
    SELECT
        TRY_TO_NUMBER($1) AS CATEGORY_ID,
        TRY_TO_NUMBER($2) AS PARENT_CATEGORY_ID,
        METADATA$FILENAME AS SOURCE_FILE_NAME,
        TRY_TO_DATE(
            REGEXP_SUBSTR(
                METADATA$FILENAME,
                'ingestion_date=([0-9]{4}-[0-9]{2}-[0-9]{2})',
                1,
                1,
                'e',
                1
            )
        ) AS INGESTION_DATE,
        $LOAD_BATCH_ID AS BATCH_ID
    FROM @RAW.RECOMART_S3_STAGE/raw/recomart/category_tree/
)
FILE_FORMAT = RAW.CSV_FILE_FORMAT
PATTERN = '.*category_tree.*[.]csv'
ON_ERROR = 'CONTINUE'
FORCE = TRUE;


-- ============================================================
-- 4. Load External Product API JSON
-- Source:
-- s3://recomartdatalake/raw/external_api/dummyjson_products/
-- Target:
-- RECOMART_DB.RAW.RAW_EXTERNAL_PRODUCTS
-- ============================================================

COPY INTO RAW.RAW_EXTERNAL_PRODUCTS (
    PRODUCT_JSON,
    SOURCE_FILE_NAME,
    INGESTION_DATE,
    BATCH_ID
)
FROM (
    SELECT
        $1 AS PRODUCT_JSON,
        METADATA$FILENAME AS SOURCE_FILE_NAME,
        TRY_TO_DATE(
            REGEXP_SUBSTR(
                METADATA$FILENAME,
                'ingestion_date=([0-9]{4}-[0-9]{2}-[0-9]{2})',
                1,
                1,
                'e',
                1
            )
        ) AS INGESTION_DATE,
        $LOAD_BATCH_ID AS BATCH_ID
    FROM @RAW.RECOMART_S3_STAGE/raw/external_api/dummyjson_products/
)
FILE_FORMAT = RAW.JSON_FILE_FORMAT
PATTERN = '.*products.*[.]json'
ON_ERROR = 'CONTINUE'
FORCE = TRUE;


-- ============================================================
-- 5. Insert Load Audit Logs
-- ============================================================

INSERT INTO OPS.INGESTION_AUDIT_LOG (
    BATCH_ID,
    SOURCE_SYSTEM,
    SOURCE_NAME,
    SOURCE_PATH,
    TARGET_TABLE,
    FILE_NAME,
    ROWS_LOADED,
    ROWS_FAILED,
    INGESTION_STATUS,
    ERROR_MESSAGE,
    START_TS,
    END_TS
)
SELECT
    $LOAD_BATCH_ID,
    'RECOMART',
    'events',
    's3://recomartdatalake/raw/recomart/events/',
    'RAW.RAW_RECOMART_EVENTS',
    'events.csv',
    COUNT(*),
    0,
    'SUCCESS',
    NULL,
    CURRENT_TIMESTAMP(),
    CURRENT_TIMESTAMP()
FROM RAW.RAW_RECOMART_EVENTS
WHERE BATCH_ID = $LOAD_BATCH_ID;


INSERT INTO OPS.INGESTION_AUDIT_LOG (
    BATCH_ID,
    SOURCE_SYSTEM,
    SOURCE_NAME,
    SOURCE_PATH,
    TARGET_TABLE,
    FILE_NAME,
    ROWS_LOADED,
    ROWS_FAILED,
    INGESTION_STATUS,
    ERROR_MESSAGE,
    START_TS,
    END_TS
)
SELECT
    $LOAD_BATCH_ID,
    'RECOMART',
    'item_properties',
    's3://recomartdatalake/raw/recomart/item_properties/',
    'RAW.RAW_RECOMART_ITEM_PROPERTIES',
    'item_properties_part1.csv,item_properties_part2.csv',
    COUNT(*),
    0,
    'SUCCESS',
    NULL,
    CURRENT_TIMESTAMP(),
    CURRENT_TIMESTAMP()
FROM RAW.RAW_RECOMART_ITEM_PROPERTIES
WHERE BATCH_ID = $LOAD_BATCH_ID;


INSERT INTO OPS.INGESTION_AUDIT_LOG (
    BATCH_ID,
    SOURCE_SYSTEM,
    SOURCE_NAME,
    SOURCE_PATH,
    TARGET_TABLE,
    FILE_NAME,
    ROWS_LOADED,
    ROWS_FAILED,
    INGESTION_STATUS,
    ERROR_MESSAGE,
    START_TS,
    END_TS
)
SELECT
    $LOAD_BATCH_ID,
    'RECOMART',
    'category_tree',
    's3://recomartdatalake/raw/recomart/category_tree/',
    'RAW.RAW_RECOMART_CATEGORY_TREE',
    'category_tree.csv',
    COUNT(*),
    0,
    'SUCCESS',
    NULL,
    CURRENT_TIMESTAMP(),
    CURRENT_TIMESTAMP()
FROM RAW.RAW_RECOMART_CATEGORY_TREE
WHERE BATCH_ID = $LOAD_BATCH_ID;


INSERT INTO OPS.INGESTION_AUDIT_LOG (
    BATCH_ID,
    SOURCE_SYSTEM,
    SOURCE_NAME,
    SOURCE_PATH,
    TARGET_TABLE,
    FILE_NAME,
    ROWS_LOADED,
    ROWS_FAILED,
    INGESTION_STATUS,
    ERROR_MESSAGE,
    START_TS,
    END_TS
)
SELECT
    $LOAD_BATCH_ID,
    'DUMMYJSON_API',
    'external_products',
    's3://recomartdatalake/raw/external_api/dummyjson_products/',
    'RAW.RAW_EXTERNAL_PRODUCTS',
    'products.json',
    COUNT(*),
    0,
    'SUCCESS',
    NULL,
    CURRENT_TIMESTAMP(),
    CURRENT_TIMESTAMP()
FROM RAW.RAW_EXTERNAL_PRODUCTS
WHERE BATCH_ID = $LOAD_BATCH_ID;


-- ============================================================
-- 6. Load Verification Summary
-- ============================================================

SELECT
    'RAW_RECOMART_EVENTS' AS TABLE_NAME,
    $LOAD_BATCH_ID AS BATCH_ID,
    COUNT(*) AS ROW_COUNT
FROM RAW.RAW_RECOMART_EVENTS
WHERE BATCH_ID = $LOAD_BATCH_ID

UNION ALL

SELECT
    'RAW_RECOMART_ITEM_PROPERTIES' AS TABLE_NAME,
    $LOAD_BATCH_ID AS BATCH_ID,
    COUNT(*) AS ROW_COUNT
FROM RAW.RAW_RECOMART_ITEM_PROPERTIES
WHERE BATCH_ID = $LOAD_BATCH_ID

UNION ALL

SELECT
    'RAW_RECOMART_CATEGORY_TREE' AS TABLE_NAME,
    $LOAD_BATCH_ID AS BATCH_ID,
    COUNT(*) AS ROW_COUNT
FROM RAW.RAW_RECOMART_CATEGORY_TREE
WHERE BATCH_ID = $LOAD_BATCH_ID

UNION ALL

SELECT
    'RAW_EXTERNAL_PRODUCTS' AS TABLE_NAME,
    $LOAD_BATCH_ID AS BATCH_ID,
    COUNT(*) AS ROW_COUNT
FROM RAW.RAW_EXTERNAL_PRODUCTS
WHERE BATCH_ID = $LOAD_BATCH_ID;