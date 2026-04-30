USE ROLE ACCOUNTADMIN;
USE DATABASE RECOMART_DB;

-- ============================================================
-- Overall DQ summary by validation batch
-- ============================================================

SELECT
    BATCH_ID AS VALIDATION_BATCH_ID,
    STATUS,
    COUNT(*) AS RULE_COUNT,
    MIN(EXECUTED_TS) AS FIRST_RULE_EXECUTED_TS,
    MAX(EXECUTED_TS) AS LAST_RULE_EXECUTED_TS
FROM OPS.DATA_QUALITY_RESULTS
GROUP BY BATCH_ID, STATUS
ORDER BY FIRST_RULE_EXECUTED_TS DESC;


-- ============================================================
-- Detailed DQ results
-- ============================================================

SELECT
    BATCH_ID AS VALIDATION_BATCH_ID,
    RULE_ID,
    TARGET_TABLE,
    TOTAL_RECORDS,
    FAILED_RECORDS,
    PASSED_RECORDS,
    FAILURE_PERCENTAGE,
    STATUS,
    MESSAGE,
    EXECUTED_TS
FROM OPS.DATA_QUALITY_RESULTS
ORDER BY EXECUTED_TS DESC, RULE_ID;


-- ============================================================
-- Valid vs invalid events by validation batch
-- ============================================================

SELECT
    VALIDATION_BATCH_ID,
    VALIDATION_RUN_TS,
    IS_VALID,
    VALIDATION_MESSAGE,
    COUNT(*) AS RECORD_COUNT
FROM VALIDATED.RECOMART_EVENTS
GROUP BY
    VALIDATION_BATCH_ID,
    VALIDATION_RUN_TS,
    IS_VALID,
    VALIDATION_MESSAGE
ORDER BY VALIDATION_RUN_TS DESC, RECORD_COUNT DESC;


-- ============================================================
-- Valid vs invalid item properties by validation batch
-- ============================================================

SELECT
    VALIDATION_BATCH_ID,
    VALIDATION_RUN_TS,
    IS_VALID,
    VALIDATION_MESSAGE,
    COUNT(*) AS RECORD_COUNT
FROM VALIDATED.RECOMART_ITEM_PROPERTIES
GROUP BY
    VALIDATION_BATCH_ID,
    VALIDATION_RUN_TS,
    IS_VALID,
    VALIDATION_MESSAGE
ORDER BY VALIDATION_RUN_TS DESC, RECORD_COUNT DESC;


-- ============================================================
-- Valid vs invalid category tree by validation batch
-- ============================================================

SELECT
    VALIDATION_BATCH_ID,
    VALIDATION_RUN_TS,
    IS_VALID,
    VALIDATION_MESSAGE,
    COUNT(*) AS RECORD_COUNT
FROM VALIDATED.RECOMART_CATEGORY_TREE
GROUP BY
    VALIDATION_BATCH_ID,
    VALIDATION_RUN_TS,
    IS_VALID,
    VALIDATION_MESSAGE
ORDER BY VALIDATION_RUN_TS DESC, RECORD_COUNT DESC;


-- ============================================================
-- Event distribution after validation
-- ============================================================

SELECT
    VALIDATION_BATCH_ID,
    EVENT_TYPE,
    COUNT(*) AS TOTAL_RECORDS,
    COUNT_IF(IS_VALID = TRUE) AS VALID_RECORDS,
    COUNT_IF(IS_VALID = FALSE) AS INVALID_RECORDS
FROM VALIDATED.RECOMART_EVENTS
GROUP BY VALIDATION_BATCH_ID, EVENT_TYPE
ORDER BY TOTAL_RECORDS DESC;