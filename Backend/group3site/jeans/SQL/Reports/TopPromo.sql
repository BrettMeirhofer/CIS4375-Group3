SELECT
    promo.id,
    promo.promo_name,
    promo.promo_code,
    promo.promo_desc,
    COUNT(DISTINCT CustomerPromo.customer_id) AS customer_count
FROM
    Promo promo
INNER JOIN CustomerPromo ON promo.id = CustomerPromo.promo_id
GROUP BY
    promo.id,
    promo.promo_name,
    promo.promo_code,
    promo.promo_desc
ORDER BY
    customer_count DESC;