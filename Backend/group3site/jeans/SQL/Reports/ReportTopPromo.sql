-- Brett Meirhofer
-- Promos by Number of Redeems
-- The client can use this report as one metric to access cashier performance. Cashiers with high customer spending may have skills that could be transferred to lower performing Cashiers increasing the overall revenue of the business.
-- Displays all the active cashiers and the total amount of customer spending with them acting as the cashier.
-- Report ID, Promo Name, Promo Code, Redeems, Total Income, Total Discount, Total Products Purchased, Number of Promos Redeemed
-- left, left, left, left, money, money, left, left
SELECT
    promo.id AS report_id,
    promo.promo_name AS promo_name,
    promo.promo_code AS promo_code,
    COUNT(DISTINCT CustomerPromo.customer_id) AS redeems,
    SUM(CustomerProductPromo.line_total) AS total_income,
    SUM(CustomerProductPromo.line_discount) AS total_discount,
    SUM(CustomerProductPromo.quantity) AS total_products_purchased,
    COUNT(CustomerPromo.id) AS num_promo_redeemed
FROM
    Promo promo
INNER JOIN CustomerPromo ON promo.id = CustomerPromo.promo_id
INNER JOIN CustomerProductPromo ON CustomerPromo.id = CustomerProductPromo.customer_promo_id
WHERE CustomerPromo.created_date BETWEEN '{}' AND '{}'
GROUP BY
    promo.id,
    promo.promo_name,
    promo.promo_code
ORDER BY
    redeems DESC;
