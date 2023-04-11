-- Owner: Perminder Singh
-- Top Months by Returning Customers Redeeming Promotions
-- Rule: Most Recent Months
-- Description: This query counts the number of returning customers per month who have redeemed promotions more than once. It joins the CustomerPromo table with a subquery that counts the number of unique promo IDs for each customer and month, then groups the result by year and month. The query is ordered by year and month.
-- Row,Year,Month,Returning Customers
-- ,left,left,left
SELECT
  ROW_NUMBER() OVER(ORDER BY (SELECT NULL)),
  YEAR(cp.created_date) as year, 
  MONTH(cp.created_date) as month, 
  COUNT(DISTINCT cp.customer_id) as returning_customers 
FROM 
  CustomerPromo cp 
  JOIN (
    SELECT 
      cp2.customer_id, 
      YEAR(cp2.created_date) as year, 
      MONTH(cp2.created_date) as month, 
      COUNT(DISTINCT cp2.promo_id) as promo_count 
    FROM 
      CustomerPromo cp2
    GROUP BY 
      cp2.customer_id, YEAR(cp2.created_date), MONTH(cp2.created_date)
  ) as customer_promo_counts ON cp.customer_id = customer_promo_counts.customer_id AND YEAR(cp.created_date) = customer_promo_counts.year AND MONTH(cp.created_date) = customer_promo_counts.month AND customer_promo_counts.promo_count > 1
WHERE cp.created_date BETWEEN '{}' AND '{}'
GROUP BY 
  YEAR(cp.created_date), MONTH(cp.created_date)
ORDER BY 
  year, month;