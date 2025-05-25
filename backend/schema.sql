-- schema.sql: Star Schema DDL

-- Dimension table: customers
CREATE TABLE IF NOT EXISTS dim_customer (
    customer_key SERIAL PRIMARY KEY,
    customer_id INT NOT NULL UNIQUE,
    country TEXT
);

-- Dimension table: products
CREATE TABLE IF NOT EXISTS dim_product (
    product_key SERIAL PRIMARY KEY,
    stock_code TEXT NOT NULL UNIQUE,
    description TEXT
);

-- Fact table: sales
CREATE TABLE IF NOT EXISTS fact_sales (
    invoice_no TEXT NOT NULL,
    stock_code_ref TEXT NOT NULL,
    customer_id_ref INT NOT NULL,
    invoice_date TIMESTAMPTZ NOT NULL,
    quantity INT NOT NULL,
    unit_price NUMERIC(10,2) NOT NULL,
    gross_line_value NUMERIC(12,2),
    is_cancelled BOOLEAN,
    customer_key INT NOT NULL,
    product_key INT NOT NULL,
    PRIMARY KEY (invoice_no, stock_code_ref),
    FOREIGN KEY (customer_key) REFERENCES dim_customer(customer_key),
    FOREIGN KEY (product_key) REFERENCES dim_product(product_key)
);
