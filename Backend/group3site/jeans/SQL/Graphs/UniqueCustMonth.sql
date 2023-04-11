SELECT MONTH(created_date) AS "labels",
COUNT(DISTINCT customer_id) AS "data"
FROM CustomerPromo
WHERE DATEDIFF(MONTH, created_date, GETDATE()) <= 12
GROUP BY MONTH(created_date)