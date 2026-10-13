SELECT
    order_day,
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(DISTINCT CASE
        WHEN is_delivered THEN order_id
    END) AS delivered_orders,
    SUM(order_value) AS total_revenue,
    AVG(order_value) AS average_order_value,
    AVG(delivery_time_minutes) AS average_delivery_time
FROM {{ ref('fct_orders') }}
GROUP BY order_day
ORDER BY order_day