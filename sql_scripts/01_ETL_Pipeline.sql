-- Tạo bảng khách hàng
CREATE TABLE staging.customers (
    customer_id SERIAL PRIMARY KEY,
    full_name VARCHAR(100),
    dob DATE,
    id_card VARCHAR(20),
    address TEXT,
    income_level DECIMAL(15, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tạo bảng tài khoản
CREATE TABLE staging.accounts (
    account_id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES staging.customers(customer_id),
    account_number VARCHAR(20) UNIQUE,
    account_type VARCHAR(20),
    balance DECIMAL(15, 2),
    status VARCHAR(10)
);

-- Tạo bảng giao dịch
CREATE TABLE staging.transactions (
    transaction_id SERIAL PRIMARY KEY,
    account_id INT REFERENCES staging.accounts(account_id),
    transaction_date TIMESTAMP,
    amount DECIMAL(15, 2),
    transaction_type VARCHAR(20),
    ip_address VARCHAR(45)
);
