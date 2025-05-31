SELECT
*
FROM dbo.customer_journey;

--

SELECT
JourneyID,
CustomerID,
ProductID,
--VisitDate,
FORMAT(CONVERT(DATE,VisitDate),'dd.MM.yy') AS VisitDate,
Stage,
Action,
Duration,
-- Use Row Number to assign a unique number to each record within the partition defined below
ROW_NUMBER() OVER(
-- Partition by groups the rows based on the specified column that should be unique

 PARTITION BY CustomerID, ProductID,VisitDate, Stage, Action
-- Order by defines how to order the rows within each partition (usually by a unique identifier like JourneyID)
ORDER BY JourneyID
) AS row_num   -- this creates a new column called row_num that numbers each row within its partition.

FROM dbo.customer_journey

SELECT *
FROM (
    SELECT
        JourneyID,
        CustomerID,
        ProductID,
        VisitDate,
        Stage,
        Action,
        Duration,
        ROW_NUMBER() OVER (
            PARTITION BY CustomerID, ProductID, VisitDate, Stage, Action
            ORDER BY JourneyID
        ) AS row_num
    FROM dbo.customer_journey
) AS subquery
WHERE row_num > 1
ORDER BY JourneyID;

-- 1. Remove rows where Duration is NULL
DELETE FROM customer_journey
WHERE Duration IS NULL;

-- 2. Remove duplicates using ROW_NUMBER() (if supported)
WITH CTE AS (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY JourneyID, CustomerID, ProductID, Stage, Action, Duration ORDER BY JourneyID) AS rn
    FROM customer_journey
)
DELETE FROM customer_journey
WHERE JourneyID IN (
    SELECT JourneyID FROM CTE WHERE rn > 1
);



SELECT
    FORMAT(VisitDate, 'MM.dd.yy') AS VisitDate
FROM dbo.customer_journey;

UPDATE dbo.customer_journey
SET VisitDate = FORMAT(CAST(VisitDate AS datetime), 'MM.dd.yy')
WHERE VisitDate IS NOT NULL;

SELECT
JourneyID,
CustomerID,
ProductID,
--VisitDate,
FORMAT(CONVERT(DATE,VisitDate),'dd.MM.yy') AS VisitDate,
Stage,
Action,
Duration

FROM dbo.customer_journey














