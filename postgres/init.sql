CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS marts;
CREATE SCHEMA IF NOT EXISTS ai;

CREATE TABLE IF NOT EXISTS raw.customers (
    customer_id INTEGER PRIMARY KEY,
    customer_name VARCHAR(100),
    email VARCHAR(150),
    city VARCHAR(100),
    age INTEGER
);

CREATE TABLE IF NOT EXISTS raw.restaurants (
    restaurant_id INTEGER PRIMARY KEY,
    restaurant_name VARCHAR(150),
    city VARCHAR(100),
    rating NUMERIC(3,1),
    delivery_time_minutes INTEGER
);

CREATE TABLE IF NOT EXISTS raw.food_items (
    food_id INTEGER PRIMARY KEY,
    food_name VARCHAR(150),
    category VARCHAR(100),
    price NUMERIC(10,2)
);

CREATE TABLE IF NOT EXISTS raw.orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    restaurant_id INTEGER,
    order_date TIMESTAMP,
    order_status VARCHAR(50),
    payment_method VARCHAR(50),
    delivery_time_minutes INTEGER
);

CREATE TABLE IF NOT EXISTS raw.order_items (
    order_item_id INTEGER PRIMARY KEY,
    order_id INTEGER,
    food_id INTEGER,
    quantity INTEGER,
    unit_price NUMERIC(10,2),
    total_price NUMERIC(10,2)
);

CREATE TABLE IF NOT EXISTS raw.reviews (
    review_id INTEGER PRIMARY KEY,
    order_id INTEGER,
    rating INTEGER,
    review_text TEXT
);