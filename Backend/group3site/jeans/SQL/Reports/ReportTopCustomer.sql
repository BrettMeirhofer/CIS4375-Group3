--Brett Meirhofer
--Top Customers by Promo Engagement
--The client can use this report as one metric to access cashier performance. Cashiers with high customer spending may have skills that could be transferred to lower performing Cashiers increasing the overall revenue of the business.
--Displays all the active cashiers and the total amount of customer spending with them acting as the cashier.
--Row Number, Customer ID, Full Name, Email Address, Promos Redeemed
--,,,,

SELECT
    ROW_NUMBER() OVER(ORDER BY (SELECT NULL)),
    Customer.id AS customer_id,
    Customer.first_name + ' ' + Customer.last_name,
    Customer.email,
    COUNT(CustomerPromo.promo_id) AS promo_count
FROM
    Customer
INNER JOIN CustomerPromo ON Customer.id = CustomerPromo.customer_id
WHERE CustomerPromo.created_date BETWEEN '{}' AND '{}'
GROUP BY
    Customer.id,
    Customer.first_name,
    Customer.last_name,
	Customer.email
ORDER BY
    promo_count DESC;
