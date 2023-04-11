-- Owner: Peminder Singh
-- Top Months by Unique Customers Redeeming Promotions
-- Rule: Most Recent Months
-- Description: The client can use this report to track the months with the most unique customers redeeming promotions ordered by the most recent date. This information can be useful in planning and executing marketing campaigns.
-- Row,Year,Month,Unique Customers
-- ,left,left,left
SELECT
 ROW_NUMBER() OVER(ORDER BY (SELECT NULL)),
  YEAR(cp.created_date) as year, 
  MONTH(cp.created_date) as month, 
  COUNT(DISTINCT cp.customer_id) as unique_customers 
FROM 
  CustomerPromo cp 
WHERE cp.created_date BETWEEN '{}' AND '{}'
GROUP BY 
  YEAR(cp.created_date), MONTH(cp.created_date)
ORDER BY 
  MAX(cp.created_date) DESC;
