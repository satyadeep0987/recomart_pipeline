USE ROLE ACCOUNTADMIN;
USE DATABASE RECOMART_DB;

-- ============================================================
-- 1. Overall clean event summary
-- ============================================================

SELECT
    COUNT(*) AS TOTAL_EVENTS,
    COUNT(DISTINCT USER_ID) AS UNIQUE_USERS,
    COUNT(DISTINCT ITEM_ID) AS UNIQUE_ITEMS,
    MIN(EVENT_TS) AS FIRST_EVENT_TS,
    MAX(EVENT_TS) AS LAST_EVENT_TS
FROM CURATED.CLEAN_RECOMART_EVENTS;


-- ============================================================
-- 2. Event type distribution
-- ============================================================

SELECT
    EVENT_TYPE,
    COUNT(*) AS EVENT_COUNT,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS EVENT_PERCENTAGE
FROM CURATED.CLEAN_RECOMART_EVENTS
GROUP BY EVENT_TYPE
ORDER BY EVENT_COUNT DESC;


-- ============================================================
-- 3. Daily event trend
-- ============================================================

SELECT
    EVENT_DATE,
    EVENT_TYPE,
    COUNT(*) AS EVENT_COUNT
FROM CURATED.CLEAN_RECOMART_EVENTS
GROUP BY EVENT_DATE, EVENT_TYPE
ORDER BY EVENT_DATE, EVENT_TYPE;


-- ============================================================
-- 4. Top 20 popular products
-- ============================================================

SELECT
    ITEM_ID,
    TOTAL_VIEWS,
    TOTAL_ADD_TO_CARTS,
    TOTAL_TRANSACTIONS,
    ITEM_POPULARITY_SCORE,
    CONVERSION_RATE
FROM CURATED.ITEM_FEATURES
ORDER BY ITEM_POPULARITY_SCORE DESC
LIMIT 20;


-- ============================================================
-- 5. User activity distribution
-- ============================================================

SELECT
    USER_ACTIVITY_LEVEL,
    COUNT(*) AS USER_COUNT
FROM CURATED.USER_FEATURES
GROUP BY USER_ACTIVITY_LEVEL
ORDER BY USER_COUNT DESC;


-- ============================================================
-- 6. Item activity distribution
-- ============================================================

SELECT
    ITEM_ACTIVITY_LEVEL,
    COUNT(*) AS ITEM_COUNT
FROM CURATED.ITEM_FEATURES
GROUP BY ITEM_ACTIVITY_LEVEL
ORDER BY ITEM_COUNT DESC;


-- ============================================================
-- 7. User-item matrix sparsity
-- ============================================================

WITH counts AS (
    SELECT
        COUNT(DISTINCT USER_ID) AS USER_COUNT,
        COUNT(DISTINCT ITEM_ID) AS ITEM_COUNT,
        COUNT(*) AS OBSERVED_INTERACTIONS
    FROM CURATED.USER_ITEM_INTERACTIONS
)
SELECT
    USER_COUNT,
    ITEM_COUNT,
    OBSERVED_INTERACTIONS,
    USER_COUNT * ITEM_COUNT AS POSSIBLE_INTERACTIONS,
    ROUND(
        1 - OBSERVED_INTERACTIONS / NULLIF(USER_COUNT * ITEM_COUNT, 0),
        6
    ) AS SPARSITY_RATIO
FROM counts;


-- ============================================================
-- 8. Interaction score distribution
-- ============================================================

SELECT
    CASE
        WHEN IMPLICIT_SCORE = 1 THEN '1'
        WHEN IMPLICIT_SCORE BETWEEN 2 AND 5 THEN '2-5'
        WHEN IMPLICIT_SCORE BETWEEN 6 AND 10 THEN '6-10'
        WHEN IMPLICIT_SCORE BETWEEN 11 AND 20 THEN '11-20'
        ELSE '20+'
    END AS SCORE_BUCKET,
    COUNT(*) AS INTERACTION_COUNT
FROM CURATED.USER_ITEM_INTERACTIONS
GROUP BY SCORE_BUCKET
ORDER BY SCORE_BUCKET;