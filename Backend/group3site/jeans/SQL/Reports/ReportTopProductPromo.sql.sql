-- Owner: Perminder Singh
-- Top Product That Have Been Used In Promos
-- Rule: Most Promotions Used
-- Description: This report shows the top products that have been redeemed by customers.
-- Row,Product ID,Product Name,Total Quantity Redeemed,Total Income,Total Discount,Number of Promotions Used,Number of Customers Who Purchased
-- ,left,left,left,money,money,left,left

SELECT
     ROW_NUMBER() OVER(ORDER BY (SELECT NULL)),
    p.id,
    p.product_name,
    SUM(cpp.quantity) as total_redeemed,
    SUM(cpp.line_total) as total_income,
    SUM(cpp.line_discount) as total_discount,
    COUNT(DISTINCT cp.id) as num_promo_redeemed,
    COUNT(DISTINCT cpp.customer_promo_id) as num_customers_purchased
FROM
    Product p
JOIN CustomerProductPromo cpp ON p.id = cpp.product_id
JOIN CustomerPromo cp ON cp.id = cpp.customer_promo_id
JOIN Promo promo ON promo.id = cp.promo_id
WHERE cp.created_date BETWEEN '{}' AND '{}'
GROUP BY p.id, p.product_name
ORDER BY total_redeemed DESC;