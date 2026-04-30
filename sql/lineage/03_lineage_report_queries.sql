USE ROLE ACCOUNTADMIN;
USE DATABASE RECOMART_DB;

-- ============================================================
-- Dataset version registry
-- ============================================================

SELECT
    DATASET_NAME,
    SOURCE_TYPE,
    LOCAL_PATH,
    S3_RAW_PATH,
    TARGET_TABLE,
    FILE_SIZE_BYTES,
    ROW_COUNT,
    SHA256_HASH,
    VERSIONING_TOOL,
    VERSION_STATUS,
    MANIFEST_CREATED_TS,
    REGISTERED_TS
FROM OPS.DATASET_VERSION_REGISTRY
ORDER BY REGISTERED_TS DESC;


-- ============================================================
-- Pipeline lineage flow
-- ============================================================

SELECT
    BATCH_ID,
    SOURCE_LAYER,
    SOURCE_OBJECT,
    TARGET_LAYER,
    TARGET_OBJECT,
    TRANSFORMATION_NAME,
    TRANSFORMATION_TYPE,
    TRANSFORMATION_LOGIC,
    STATUS,
    CREATED_TS
FROM OPS.DATA_LINEAGE
ORDER BY CREATED_TS;


-- ============================================================
-- End-to-end batch trace
-- ============================================================

SELECT
    l.BATCH_ID,
    l.TRANSFORMATION_NAME,
    l.SOURCE_OBJECT,
    l.TARGET_OBJECT,
    l.TRANSFORMATION_TYPE,
    l.STATUS,
    l.CREATED_TS
FROM OPS.DATA_LINEAGE l
WHERE l.BATCH_ID = (
    SELECT BATCH_ID
    FROM OPS.DATA_LINEAGE
    WHERE BATCH_ID IS NOT NULL
    ORDER BY CREATED_TS DESC
    LIMIT 1
)
ORDER BY l.CREATED_TS;


-- ============================================================
-- Feature store version lineage
-- ============================================================

SELECT
    FEATURE_VERSION,
    SOURCE_VALIDATION_BATCH_ID,
    COUNT(*) AS FEATURE_ROW_COUNT,
    MIN(FEATURE_PUBLISHED_TS) AS FIRST_PUBLISHED_TS,
    MAX(FEATURE_PUBLISHED_TS) AS LAST_PUBLISHED_TS
FROM FEATURE_STORE.OFFLINE_RECOMMENDATION_FEATURES
GROUP BY FEATURE_VERSION, SOURCE_VALIDATION_BATCH_ID
ORDER BY LAST_PUBLISHED_TS DESC;