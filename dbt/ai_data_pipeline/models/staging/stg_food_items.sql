SELECT
    food_id,
    TRIM(food_name) AS food_name,
    TRIM(category) AS category,
    price
FROM {{ source('raw', 'food_items') }}