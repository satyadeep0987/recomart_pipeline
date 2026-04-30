USE ROLE ACCOUNTADMIN;
USE DATABASE RECOMART_DB;

CREATE SCHEMA IF NOT EXISTS FEATURE_STORE;

-- ============================================================
-- Feature metadata registry
-- ============================================================

CREATE TABLE IF NOT EXISTS FEATURE_STORE.FEATURE_REGISTRY (
    FEATURE_ID              VARCHAR,
    FEATURE_NAME            VARCHAR,
    FEATURE_GROUP           VARCHAR,
    ENTITY_TYPE             VARCHAR,
    ENTITY_KEY              VARCHAR,
    SOURCE_TABLE            VARCHAR,
    SOURCE_COLUMN           VARCHAR,
    TRANSFORMATION_LOGIC     VARCHAR,
    DATA_TYPE               VARCHAR,
    FEATURE_VERSION         VARCHAR,
    SOURCE_VALIDATION_BATCH_ID VARCHAR,
    IS_ACTIVE               BOOLEAN DEFAULT TRUE,
    CREATED_BY              VARCHAR DEFAULT CURRENT_USER(),
    CREATED_TS              TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    UPDATED_TS              TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- ============================================================
-- Offline feature table for model training
-- ============================================================

CREATE TABLE IF NOT EXISTS FEATURE_STORE.OFFLINE_RECOMMENDATION_FEATURES (
    USER_ID                         NUMBER(38,0),
    ITEM_ID                         NUMBER(38,0),

    USER_TOTAL_VIEWS                NUMBER(38,0),
    USER_TOTAL_ADD_TO_CARTS         NUMBER(38,0),
    USER_TOTAL_TRANSACTIONS         NUMBER(38,0),
    USER_ACTIVITY_LEVEL             VARCHAR,
    USER_AVG_IMPLICIT_SCORE         FLOAT,

    ITEM_TOTAL_VIEWS                NUMBER(38,0),
    ITEM_TOTAL_ADD_TO_CARTS         NUMBER(38,0),
    ITEM_TOTAL_TRANSACTIONS         NUMBER(38,0),
    ITEM_POPULARITY_SCORE           FLOAT,
    ITEM_CONVERSION_RATE            FLOAT,
    ITEM_ACTIVITY_LEVEL             VARCHAR,

    VIEW_COUNT                      NUMBER(38,0),
    ADD_TO_CART_COUNT               NUMBER(38,0),
    TRANSACTION_COUNT               NUMBER(38,0),
    USER_ITEM_IMPLICIT_SCORE        FLOAT,

    TARGET_LABEL                    FLOAT,

    FEATURE_VERSION                 VARCHAR,
    SOURCE_VALIDATION_BATCH_ID      VARCHAR,
    FEATURE_RUN_TS                  TIMESTAMP_NTZ,
    FEATURE_PUBLISHED_TS            TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- ============================================================
-- Online feature table for inference
-- ============================================================

CREATE TABLE IF NOT EXISTS FEATURE_STORE.ONLINE_RECOMMENDATION_FEATURES (
    USER_ID                         NUMBER(38,0),
    ITEM_ID                         NUMBER(38,0),

    USER_ACTIVITY_LEVEL             VARCHAR,
    USER_AVG_IMPLICIT_SCORE         FLOAT,

    ITEM_POPULARITY_SCORE           FLOAT,
    ITEM_CONVERSION_RATE            FLOAT,
    ITEM_ACTIVITY_LEVEL             VARCHAR,

    USER_ITEM_IMPLICIT_SCORE        FLOAT,
    RECOMMENDATION_CANDIDATE_SCORE  FLOAT,

    FEATURE_VERSION                 VARCHAR,
    SOURCE_VALIDATION_BATCH_ID      VARCHAR,
    LAST_UPDATED_TS                 TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- ============================================================
-- Retrieval audit log
-- ============================================================

CREATE TABLE IF NOT EXISTS FEATURE_STORE.FEATURE_RETRIEVAL_LOG (
    REQUEST_ID              VARCHAR,
    USER_ID                 NUMBER(38,0),
    ITEM_ID                 NUMBER(38,0),
    FEATURE_VERSION         VARCHAR,
    SOURCE_VALIDATION_BATCH_ID VARCHAR,
    REQUEST_TYPE            VARCHAR,
    REQUEST_TS              TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    STATUS                  VARCHAR,
    MESSAGE                 VARCHAR
);