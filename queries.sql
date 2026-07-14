-- Example analytical queries to run against warehouse.db
-- Usage: sqlite3 warehouse.db < queries.sql
-- Or open sqlite3 warehouse.db interactively and paste these one at a time.

-- 1. Top 10 products by total revenue
SELECT
    Description,
    ROUND(SUM(TotalPrice), 2) AS total_revenue,
    SUM(Quantity) AS total_units_sold
FROM orders
GROUP BY Description
ORDER BY total_revenue DESC
LIMIT 10;

-- 2. Monthly revenue trend
SELECT
    strftime('%Y-%m', InvoiceDate) AS month,
    ROUND(SUM(TotalPrice), 2) AS monthly_revenue,
    COUNT(DISTINCT InvoiceNo) AS num_orders
FROM orders
GROUP BY month
ORDER BY month;

-- 3. Revenue by country
SELECT
    Country,
    ROUND(SUM(TotalPrice), 2) AS total_revenue,
    COUNT(DISTINCT CustomerID) AS num_customers
FROM orders
GROUP BY Country
ORDER BY total_revenue DESC
LIMIT 15;

-- 4. Top customers by lifetime spend
SELECT
    CustomerID,
    Country,
    ROUND(SUM(TotalPrice), 2) AS lifetime_spend,
    COUNT(DISTINCT InvoiceNo) AS num_orders
FROM orders
GROUP BY CustomerID
ORDER BY lifetime_spend DESC
LIMIT 10;

-- 5. Average order value over time (a metric that matters to any business)
SELECT
    strftime('%Y-%m', InvoiceDate) AS month,
    ROUND(SUM(TotalPrice) / COUNT(DISTINCT InvoiceNo), 2) AS avg_order_value
FROM orders
GROUP BY month
ORDER BY month;
