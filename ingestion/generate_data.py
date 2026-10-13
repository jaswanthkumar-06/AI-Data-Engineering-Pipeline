import os
import random
from datetime import datetime, timedelta

import pandas as pd
import numpy as np


# -----------------------------
# Configuration
# -----------------------------

OUTPUT_DIR = "data/raw"

NUM_RESTAURANTS = 100
NUM_CUSTOMERS = 1000
NUM_FOOD_ITEMS = 300
NUM_ORDERS = 10000
NUM_REVIEWS = 3000

random.seed(42)
np.random.seed(42)


# -----------------------------
# Create output directory
# -----------------------------

os.makedirs(OUTPUT_DIR, exist_ok=True)


# -----------------------------
# Restaurants
# -----------------------------

cities = [
    "Visakhapatnam",
    "Hyderabad",
    "Bengaluru",
    "Chennai",
    "Vijayawada",
]

restaurant_names = [
    "Spice Hub",
    "Food Factory",
    "Urban Tadka",
    "Biryani House",
    "Taste Point",
    "Food Junction",
    "The Kitchen",
    "Royal Meals",
    "Andhra Flavours",
    "Street Bites",
]

restaurants = []

for i in range(1, NUM_RESTAURANTS + 1):
    restaurants.append(
        {
            "restaurant_id": i,
            "restaurant_name": f"{random.choice(restaurant_names)} {i}",
            "city": random.choice(cities),
            "rating": round(random.uniform(3.0, 5.0), 1),
            "delivery_time_minutes": random.randint(20, 60),
        }
    )

restaurants_df = pd.DataFrame(restaurants)


# -----------------------------
# Customers
# -----------------------------

customers = []

for i in range(1, NUM_CUSTOMERS + 1):
    customers.append(
        {
            "customer_id": i,
            "customer_name": f"Customer_{i}",
            "email": f"customer{i}@example.com",
            "city": random.choice(cities),
            "age": random.randint(18, 60),
        }
    )

customers_df = pd.DataFrame(customers)


# -----------------------------
# Food Items
# -----------------------------

food_names = [
    "Chicken Biryani",
    "Veg Biryani",
    "Paneer Butter Masala",
    "Chicken Fried Rice",
    "Veg Fried Rice",
    "Masala Dosa",
    "Idli",
    "Vada",
    "Pizza",
    "Burger",
    "Noodles",
    "Mandi",
    "Chicken 65",
    "Paneer Tikka",
    "Gulab Jamun",
]

categories = [
    "Biryani",
    "Indian",
    "Chinese",
    "Fast Food",
    "Dessert",
]

food_items = []

for i in range(1, NUM_FOOD_ITEMS + 1):
    food_items.append(
        {
            "food_id": i,
            "food_name": f"{random.choice(food_names)} {i}",
            "category": random.choice(categories),
            "price": round(random.uniform(80, 600), 2),
        }
    )

food_df = pd.DataFrame(food_items)


# -----------------------------
# Orders
# -----------------------------

order_statuses = [
    "Delivered",
    "Delivered",
    "Delivered",
    "Cancelled",
]

payment_methods = [
    "UPI",
    "Credit Card",
    "Debit Card",
    "Cash",
]

start_date = datetime(2026, 1, 1)

orders = []

for i in range(1, NUM_ORDERS + 1):

    order_date = start_date + timedelta(
        days=random.randint(0, 270),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59),
    )

    orders.append(
        {
            "order_id": i,
            "customer_id": random.randint(1, NUM_CUSTOMERS),
            "restaurant_id": random.randint(1, NUM_RESTAURANTS),
            "order_date": order_date,
            "order_status": random.choice(order_statuses),
            "payment_method": random.choice(payment_methods),
            "delivery_time_minutes": random.randint(20, 70),
        }
    )

orders_df = pd.DataFrame(orders)


# -----------------------------
# Order Items
# -----------------------------

order_items = []

item_id = 1

for order_id in range(1, NUM_ORDERS + 1):

    number_of_items = random.randint(1, 4)

    for _ in range(number_of_items):

        food_id = random.randint(1, NUM_FOOD_ITEMS)
        quantity = random.randint(1, 3)

        food_price = food_df.loc[
            food_df["food_id"] == food_id, "price"
        ].iloc[0]

        order_items.append(
            {
                "order_item_id": item_id,
                "order_id": order_id,
                "food_id": food_id,
                "quantity": quantity,
                "unit_price": food_price,
                "total_price": round(food_price * quantity, 2),
            }
        )

        item_id += 1

order_items_df = pd.DataFrame(order_items)


# -----------------------------
# Reviews
# -----------------------------

positive_reviews = [
    "Food was excellent and delivery was fast",
    "Amazing taste and good quality",
    "Really enjoyed the food",
    "Great service and delicious food",
    "The food arrived hot and fresh",
]

negative_reviews = [
    "Food was cold when it arrived",
    "Very late delivery",
    "Food quality was poor",
    "Not satisfied with the order",
    "The food was not fresh",
]

neutral_reviews = [
    "Food was okay",
    "Average experience",
    "Nothing special",
    "It was fine",
    "Decent food and service",
]

reviews = []

for i in range(1, NUM_REVIEWS + 1):

    review_type = random.choice(
        ["positive", "positive", "negative", "neutral"]
    )

    if review_type == "positive":
        review_text = random.choice(positive_reviews)

    elif review_type == "negative":
        review_text = random.choice(negative_reviews)

    else:
        review_text = random.choice(neutral_reviews)

    reviews.append(
        {
            "review_id": i,
            "order_id": random.randint(1, NUM_ORDERS),
            "rating": random.randint(1, 5),
            "review_text": review_text,
        }
    )

reviews_df = pd.DataFrame(reviews)


# -----------------------------
# Save CSV files
# -----------------------------

datasets = {
    "restaurants.csv": restaurants_df,
    "customers.csv": customers_df,
    "food_items.csv": food_df,
    "orders.csv": orders_df,
    "order_items.csv": order_items_df,
    "reviews.csv": reviews_df,
}

for filename, dataframe in datasets.items():

    path = os.path.join(OUTPUT_DIR, filename)

    dataframe.to_csv(path, index=False)

    print(f"Created: {path} ({len(dataframe):,} rows)")


print("\nDataset generation completed successfully.")