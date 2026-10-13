
{{ config(materialized='table') }}

WITH review_summary AS (
    SELECT
        restaurant_id,
        COUNT(*) AS total_reviews,
        COUNT(*) FILTER (WHERE sentiment = 'positive') AS positive_reviews,
        COUNT(*) FILTER (WHERE sentiment = 'neutral') AS neutral_reviews,
        COUNT(*) FILTER (WHERE sentiment = 'negative') AS negative_reviews,
        AVG(rating) AS average_review_rating
    FROM {{ source('raw', 'reviews') }} AS r
    LEFT JOIN {{ source('ai', 'review_sentiment') }} AS s
        ON r.review_id = s.review_id
    GROUP BY restaurant_id
)

SELECT
    restaurant.restaurant_id,
    restaurant.restaurant_name,
    restaurant.city,
    restaurant.rating AS restaurant_rating,
    COALESCE(summary.total_reviews, 0) AS total_reviews,
    COALESCE(summary.positive_reviews, 0) AS positive_reviews,
    COALESCE(summary.neutral_reviews, 0) AS neutral_reviews,
    COALESCE(summary.negative_reviews, 0) AS negative_reviews,
    COALESCE(
        summary.negative_reviews::NUMERIC
        / NULLIF(summary.total_reviews, 0),
        0
    ) AS negative_review_rate,
    summary.average_review_rating
FROM {{ ref('dim_restaurants') }} AS restaurant
LEFT JOIN review_summary AS summary
    ON restaurant.restaurant_id = summary.restaurant_id
