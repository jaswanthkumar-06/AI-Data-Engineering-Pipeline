SELECT
    o.order_id,
    o.order_date,
    o.order_day,
    o.customer_id,
    o.restaurant_id,
    o.order_status,
    o.payment_method,
    o.delivery_time_minutes,
    o.is_delivered,
    COALESCE(SUM(oi.total_price), 0) AS order_value
FROM {{ ref('stg_orders') }} o
LEFT JOIN {{ ref('stg_order_items') }} oi
    ON o.order_id = oi.order_id
GROUP BY
    o.order_id,
    o.order_date,
    o.order_day,
    o.customer_id,
    o.restaurant_id,
    o.order_status,
    o.payment_method,
    o.delivery_time_minutes,
    o.is_delivered