SELECT
*
FROM dbo.engagement_data;

--

SELECT
EngagementID,
ContentID,
ContentType,
UPPER(REPLACE(ContentType, 'Socialmedia','SOCIALMEDIA')) AS ContentType,                             -- Change the case of Socialmedia to SocialMedia
Likes,
LEFT(ViewsClicksCombined,CHARINDEX('-', ViewsClicksCombined)-1) AS Views,                            -- Extracts the views from the combined clicks and views data
RIGHT(ViewsClicksCombined,LEN(ViewsClicksCombined)-CHARINDEX('-',ViewsClicksCombined)) AS Clicks,    -- Extracts the clicks from the combined clicks and views data
CampaignID,
ProductID,
FORMAT(CONVERT(DATE,EngagementDate),'dd.MM.yy') AS EngagementDate           -- Format the date as month-date-year

FROM dbo.engagement_data

WHERE ContentType != 'newsletter';              -- Filters out parts where ContentType is newsletter




