SELECT TOP 5
CONCAT(first_name, ' ', last_name) AS "labels",
COUNT(*) AS "data"
FROM CustomerPromo
INNER JOIN Customer ON Customer.id = CustomerPromo.customer_id
GROUP BY CONCAT(first_name, ' ', last_name)
ORDER BY COUNT(*) DESC