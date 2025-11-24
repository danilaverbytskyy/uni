CREATE TABLE Products (
    product_id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity >= 0)
);

CREATE TABLE Orders (
    order_id SERIAL PRIMARY KEY,
    total_price DECIMAL(10, 2) NOT NULL CHECK (total_price >= 0),
    date DATE NOT NULL,
    date_of_recording TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Orders_Products (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES Orders(order_id) ON DELETE CASCADE,
    product_id INTEGER NOT NULL REFERENCES Products(product_id) ON DELETE RESTRICT,
    price DECIMAL(10, 2) NOT NULL CHECK (price >= 0),
    quantity INTEGER NOT NULL CHECK (quantity > 0),

    UNIQUE(order_id, product_id)
);