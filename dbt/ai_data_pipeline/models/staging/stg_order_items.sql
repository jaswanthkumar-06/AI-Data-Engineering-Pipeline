SELECT
    order_item_id,
    order_id,
    food_id,
    quantity,
    unit_price,
    total_price
FROM {{ source('raw', 'order_items') }}