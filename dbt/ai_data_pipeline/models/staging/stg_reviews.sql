SELECT
    review_id,
    order_id,
    rating,
    TRIM(review_text) AS review_text,
    LENGTH(TRIM(review_text)) AS review_length
FROM {{ source('raw', 'reviews') }}