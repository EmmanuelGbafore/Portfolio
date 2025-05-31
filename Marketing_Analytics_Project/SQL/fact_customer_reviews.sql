SELECT
*
FROM dbo.customer_reviews;

-- 

SELECT
 ReviewID,                 -- Selects the ReviewID
 CustomerID,               -- Selects the CustomerID
 ProductID,                -- Selects the ProductID
 ReviewDate,               -- Selects the Date
 Rating,                   -- Selects the Rating
 REPLACE(ReviewText,'  ',' ') AS ReviewText          -- Replaces double spaces in the review text with single spaces

 FROM dbo.customer_reviews;
