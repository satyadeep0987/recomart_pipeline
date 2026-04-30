USE ROLE ACCOUNTADMIN;
USE DATABASE RECOMART_DB;

-- ============================================================
-- Load RecoMart events
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
        $1::NUMBER,
        $2::NUMBER,
        $3::VARCHAR,
        $4::NUMBER,
        TRY_TO_NUMBER($5),
        METADATA$FILENAME,
        CURRENT_DATE(),
        TO_VARCHAR(CURRENT_TIMESTAMP(), 'YYYYMMDDHH24MISS')
    FROM @RAW.RECOMART_S3_STAGE/raw/recomart/events/
)
FILE_FORMAT = RAW.CSV_FILE_FORMAT
PATTERN = '.*events.*[.]csv'
ON_ERROR = 'CONTINUE';


-- ============================================================
-- Load RecoMart item properties
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
        $1::NUMBER,
        $2::NUMBER,
        $3::VARCHAR,
        $4::VARCHAR,
        METADATA$FILENAME,
        CURRENT_DATE(),
        TO_VARCHAR(CURRENT_TIMESTAMP(), 'YYYYMMDDHH24MISS')
    FROM @RAW.RECOMART_S3_STAGE/raw/recomart/item_properties/
)
FILE_FORMAT = RAW.CSV_FILE_FORMAT
PATTERN = '.*item_properties.*[.]csv'
ON_ERROR = 'CONTINUE';


-- ============================================================
-- Load RecoMart category tree
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
        $1::NUMBER,
        TRY_TO_NUMBER($2),
        METADATA$FILENAME,
        CURRENT_DATE(),
        TO_VARCHAR(CURRENT_TIMESTAMP(), 'YYYYMMDDHH24MISS')
    FROM @RAW.RECOMART_S3_STAGE/raw/recomart/category_tree/
)
FILE_FORMAT = RAW.CSV_FILE_FORMAT
PATTERN = '.*category_tree.*[.]csv'
ON_ERROR = 'CONTINUE';


-- ============================================================
-- Load external product JSON
-- ============================================================

COPY INTO RAW.RAW_EXTERNAL_PRODUCTS (
    PRODUCT_JSON,
    SOURCE_FILE_NAME,
    INGESTION_DATE,
    BATCH_ID
)
FROM (
    SELECT
        $1,
        METADATA$FILENAME,
        CURRENT_DATE(),
        TO_VARCHAR(CURRENT_TIMESTAMP(), 'YYYYMMDDHH24MISS')
    FROM @RAW.RECOMART_S3_STAGE/raw/external_api/dummyjson_products/
)
FILE_FORMAT = RAW.JSON_FILE_FORMAT
PATTERN = '.*products.*[.]json'
ON_ERROR = 'CONTINUE';