--Brett Meirhofer
--Top Customers by Promo Engagement
--The client can use this report as one metric to access cashier performance. Cashiers with high customer spending may have skills that could be transferred to lower performing Cashiers increasing the overall revenue of the business.
--Displays all the active cashiers and the total amount of customer spending with them acting as the cashier.
--Row,Customer ID, Full Name, Email Address, Total Income, Total Discount, Num Products Purchased, Num Promos Redeemed
--,left,left,left,money,money,left,left

SELECT
 ROW_NUMBER() OVER(ORDER BY (SELECT NULL)),
    Customer.id AS customer_id,
    Customer.first_name + ' ' + Customer.last_name AS customer_name,
    Customer.email,
    SUM(CustomerProductPromo.line_total) AS total_income,
    SUM(CustomerProductPromo.line_discount) AS total_discount,
    SUM(CustomerProductPromo.quantity) AS num_products_purchased,
    COUNT(CustomerPromo.id) AS num_promo_redeemed
FROM
    Customer
INNER JOIN CustomerPromo ON Customer.id = CustomerPromo.customer_id
INNER JOIN CustomerProductPromo ON CustomerPromo.id = CustomerProductPromo.customer_promo_id
WHERE CustomerPromo.created_date BETWEEN '{}' AND '{}'
GROUP BY
    Customer.id,
    Customer.first_name,
    Customer.last_name,
    Customer.email
ORDER BY
    num_promo_redeemed DESC;

