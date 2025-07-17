-- Return rate per category
SELECT category, COUNT(*) AS total_returns
FROM orders o
JOIN returns r ON o.order_id = r.order_id
JOIN products p ON o.product_id = p.product_id
GROUP BY category
ORDER BY total_returns DESC;
