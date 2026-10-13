SELECT
    restaurant_id,
    restaurant_name,
    city,
    rating,
    delivery_time_minutes
FROM {{ ref('stg_restaurants') }}