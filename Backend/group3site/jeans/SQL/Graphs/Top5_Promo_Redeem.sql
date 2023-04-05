SELECT TOP 5
promo_code AS "labels",
COUNT(*) AS "data"
FROM Promo
INNER JOIN CustomerPromo ON CustomerPromo.promo_id = Promo.id
GROUP BY promo_code
ORDER BY COUNT(*) DESC