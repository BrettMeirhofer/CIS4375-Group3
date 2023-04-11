-- Owner: Perminder Singh
-- Top Product Promo
-- Rule: Most Promotions Used
-- Description: This report shows the top products with the most promotions used, along with the promotion names.
-- Product Name, Promo Count, Promos Used
-- left, right, left
SELECT 
  p.product_name, 
  COUNT(*) AS promo_count,
  STRING_AGG(pr.promo_name, ', ') AS promos_used
FROM 
  Product p
  JOIN ProductPromo pp ON pp.product_id = p.id
  JOIN Promo pr ON pr.id = pp.promo_id
WHERE pr.created_date BETWEEN '{}' AND '{}'
GROUP BY 
  p.product_name
ORDER BY 
  promo_count DESC;