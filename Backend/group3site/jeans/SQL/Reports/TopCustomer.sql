SELECT
    Customer.id AS customer_id,
    Customer.first_name,
    Customer.last_name,
    COUNT(CustomerPromo.promo_id) AS promo_count
FROM
    Customer
INNER JOIN CustomerPromo ON Customer.id = CustomerPromo.customer_id
GROUP BY
    Customer.id,
    Customer.first_name,
    Customer.last_name
ORDER BY
    promo_count DESC;