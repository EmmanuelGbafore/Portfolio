SELECT
*
FROM dbo.customers

SELECT
*
FROM dbo.geography

SELECT
CustomerID,
CustomerName,
Email,
Gender,
GeographyID,
Age,
CASE
WHEN Age < 30 THEN 'Young'
WHEN Age BETWEEN 30 AND 54 THEN 'Middle_Age'
ELSE 'Senior'
END AS AgeGroup


FROM dbo.customers

SELECT
*
FROM dbo.customer_journey

SELECT
*
FROM dbo.customers

