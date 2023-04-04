--Brett Meirhofer
--Promos by number of redeems
--The client can use this report as one metric to access cashier performance. Cashiers with high customer spending may have skills that could be transferred to lower performing Cashiers increasing the overall revenue of the business.
--Displays all the active cashiers and the total amount of customer spending with them acting as the cashier.
--Row Number, Promo Name, Promo Code, Redeems
--,,,,right,right,right

SELECT
    promo.id,
    promo.promo_name,
    promo.promo_code,
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