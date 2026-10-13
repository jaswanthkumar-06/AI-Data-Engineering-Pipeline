SELECT
    customer_id,
    customer_name,
    email,
    city,
    age,
    age_group
FROM {{ ref('stg_customers') }}