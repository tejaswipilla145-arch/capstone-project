I installed the Python libraries I needed (requests, beautifulsoup4, pandas).

I scraped data from the website using requests to get the page and BeautifulSoup to pull out book titles, prices, ratings, and availability.

I cleaned the data:

Took out the £ sign and made prices into numbers.

Changed rating words into numbers (1–5).

Made availability into True/False.

Added INR prices using the fixed rate (1 GBP = 105.50 INR).

Filled missing numeric values with the median or dropped bad rows.

I made a SQLite database with two tables: one for categories and one for books. The books table links to categories with a foreign key.

I inserted the cleaned data into the database.

I ran SQL queries to practice: SELECT with WHERE, ORDER BY, LIMIT, DISTINCT, BETWEEN, and a JOIN between books and categories.

I read some query results back into pandas DataFrames with pd.read\_sql.

I also used pd.merge on my DataFrames to reproduce the join query and checked that both SQL and pandas gave the same result.

