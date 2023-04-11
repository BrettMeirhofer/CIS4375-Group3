-- Owner: Perminder Singh
-- Top Product That Have Been Used In Promos
-- Rule: Most Promotions Used
-- Description: This report shows the top products that have been redeemed by customers.
-- Product Name, Promo Count, Promos Used
-- left, left, left
SELECT p.id, p.product_name, SUM(cpp.quantity) as total_redeemed
FROM Product p
JOIN CustomerProductPromo cpp ON p.id = cpp.product_id
JOIN CustomerPromo cp ON cp.id = cpp.customer_promo_id
JOIN Promo promo ON promo.id = cp.promo_id
WHERE cp.created_date BETWEEN '{}' AND '{}'
GROUP BY p.id, p.product_name
ORDER BY total_redeemed DESC;