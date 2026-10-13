SELECT
    order_id,
    customer_id,
    restaurant_id,
    order_date,
    DATE(order_date) AS order_day,
    order_status,
    payment_method,
    delivery_time_minutes,
    CASE
        WHEN order_status = 'Delivered' THEN TRUE
        ELSE FALSE
    END AS is_delivered
FROM {{ source('raw', 'orders') }}