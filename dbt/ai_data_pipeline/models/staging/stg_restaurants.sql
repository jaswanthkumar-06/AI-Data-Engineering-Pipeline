SELECT
    restaurant_id,
    TRIM(restaurant_name) AS restaurant_name,
    TRIM(city) AS city,
    rating,
    delivery_time_minutes
FROM {{ source('raw', 'restaurants') }}