import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3 
import numpy as np

books = []

for page in range(1, 6): 
    url = f"https://books.toscrape.com/catalogue/page-{page}.html"
    response = requests.get(url)
    response.encoding = "utf-8"   # ✅ force UTF-8 decoding
    soup = BeautifulSoup(response.text, "html.parser")

    for book in soup.select(".product_pod"):
        title = book.h3.a["title"]
        price = book.select_one(".price_color").text
        star_rating = book.p["class"][1]   # e.g. "Three"
        availability = book.select_one(".availability").text.strip()
        category = "All products"

        books.append([title, price, star_rating, availability, category])

df = pd.DataFrame(books,columns=["title", "price", "star_rating", "availability", "category"])
print(df.head())



# Example scraped data
books = [
    {"title": "Book A", "price_raw": "£51.77", "rating_raw": "Three", "availability_raw": "In stock (22 available)", "category": "Travel"},
    {"title": "Book B", "price_raw": "£53.74", "rating_raw": "Five", "availability_raw": "Out of stock", "category": "Fiction"},
    {"title": "Book C", "price_raw": "£50.10", "rating_raw": "One", "availability_raw": "In stock (10 available)", "category": "History"},
]

df = pd.DataFrame(books)

# Strip currency symbol and convert to float
df["price_gbp"] = df["price_raw"].str.replace("£", "").astype(float)

# Map star rating text to integer
rating_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
df["rating"] = df["rating_raw"].map(rating_map)

# Parse availability text into boolean
df["in_stock"] = df["availability_raw"].str.contains("In stock")

# Handle parsing errors: median imputation for numeric fields
df["rating"] = df["rating"].fillna(df["rating"].median())
df["price_gbp"] = df["price_gbp"].fillna(df["price_gbp"].median())

# Drop rows if non-numeric fields fail
df = df.dropna(subset=["title", "category"])

# Convert GBP to INR using fixed rate
df["price_inr"] = df["price_gbp"] * 105.50

print(df)


# Example DataFrame with price_gbp
data = {
    "title": ["Book A", "Book B", "Book C"],
    "price_gbp": [51.77, 53.74, 50.10]
}

df = pd.DataFrame(data)

# Fixed baseline conversion rate
CONVERSION_RATE = 105.50

# Convert GBP to INR
df["price_inr"] = df["price_gbp"] * CONVERSION_RATE

print(df)


# Connect to SQLite database (creates file if not exists)
conn = sqlite3.connect("books.db")
cursor = conn.cursor()

# Create categories table
cursor.execute("""
CREATE TABLE IF NOT EXISTS categories (
    category_id INTEGER PRIMARY KEY,
    category_name TEXT UNIQUE
);
""")

# Create books table with FK reference to categories
cursor.execute("""
CREATE TABLE IF NOT EXISTS books (
    book_id INTEGER PRIMARY KEY,
    title TEXT,
    price_gbp REAL,
    price_inr REAL,
    rating INTEGER,
    in_stock INTEGER,
    category_id INTEGER,
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
);
""")

conn.commit()
conn.close()



books_data = [
    {"title": "Book A", "price_gbp": 51.77, "price_inr": 5451.385, "rating": 3, "in_stock": 1, "category": "Travel"},
    {"title": "Book B", "price_gbp": 53.74, "price_inr": 5665.67, "rating": 5, "in_stock": 0, "category": "Fiction"},
    {"title": "Book C", "price_gbp": 50.10, "price_inr": 5285.55, "rating": 1, "in_stock": 1, "category": "History"},
]

conn = sqlite3.connect("books.db")
cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS categories (
    category_id INTEGER PRIMARY KEY,
    category_name TEXT UNIQUE
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS books (
    book_id INTEGER PRIMARY KEY,
    title TEXT,
    price_gbp REAL,
    price_inr REAL,
    rating INTEGER,
    in_stock INTEGER,
    category_id INTEGER,
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
);
""")


categories = {b["category"] for b in books_data}
for cat in categories:
    cursor.execute("INSERT OR IGNORE INTO categories (category_name) VALUES (?)", (cat,))


for b in books_data:
    cursor.execute("SELECT category_id FROM categories WHERE category_name=?", (b["category"],))
    cat_id = cursor.fetchone()[0]
    cursor.execute("""
    INSERT INTO books (title, price_gbp, price_inr, rating, in_stock, category_id)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (b["title"], b["price_gbp"], b["price_inr"], b["rating"], b["in_stock"], cat_id))

conn.commit()


q1 = "SELECT title, price_gbp FROM books WHERE rating >= 3;"
print(pd.read_sql(q1, conn))

q2 = "SELECT title, rating FROM books ORDER BY rating DESC;"
print(pd.read_sql(q2, conn))

q3 = "SELECT title, price_inr FROM books ORDER BY price_inr DESC LIMIT 2;"
print(pd.read_sql(q3, conn))


q4 = "SELECT DISTINCT category_id FROM books;"
print(pd.read_sql(q4, conn))


q5 = "SELECT title, price_gbp FROM books WHERE price_gbp BETWEEN 50 AND 52;"
print(pd.read_sql(q5, conn))


q6 = """
SELECT c.category_name, b.title, b.rating
FROM books b
JOIN categories c ON b.category_id = c.category_id
ORDER BY c.category_name, b.rating DESC
LIMIT 10;
"""
print(pd.read_sql(q6, conn))

conn.close()

import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect("books.db")

# Read back two query results into DataFrames
q1 = "SELECT title, price_gbp FROM books WHERE rating >= 3;"
df_q1 = pd.read_sql(q1, conn)
print("Query 1 result:\n", df_q1)

q2 = "SELECT title, rating FROM books ORDER BY rating DESC;"
df_q2 = pd.read_sql(q2, conn)
print("Query 2 result:\n", df_q2)

# Reproduce the join query using pd.merge on in-memory DataFrames
books_df = pd.read_sql("SELECT * FROM books;", conn)
categories_df = pd.read_sql("SELECT * FROM categories;", conn)

merged = pd.merge(books_df, categories_df, on="category_id", how="inner")
join_result = merged[["category_name", "title", "rating"]].sort_values(
    by=["category_name", "rating"], ascending=[True, False]
).head(10)

print("Join result via merge:\n", join_result)

conn.close()

