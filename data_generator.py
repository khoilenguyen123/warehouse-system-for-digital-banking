import pandas as pd
from sqlalchemy import create_engine
from faker import Faker
import random
from datetime import datetime, timedelta

# 1. Cấu hình kết nối (Nhớ thay mật khẩu của Khôi)
conn_string = 'postgresql://postgres:123@localhost:5432/postgres'
engine = create_engine(conn_string)
fake = Faker()


def generate_large_data():
    print("⏳ Bắt đầu tạo dữ liệu. Quá trình này mất khoảng 1-2 phút...")

    # --- TẠO KHÁCH HÀNG (5,000 người) ---
    print("1. Đang tạo 5000 Khách hàng...")
    customers = []
    for _ in range(5000):
        customers.append({
            'full_name': fake.name(),
            'dob': fake.date_of_birth(minimum_age=18, maximum_age=70),
            'id_card': fake.ssn(),
            'address': fake.address().replace('\n', ', '),
            'income_level': round(random.uniform(5000000, 100000000), 2)
        })
    pd.DataFrame(customers).to_sql('customers', engine, schema='staging', if_exists='append', index=False)

    # --- TẠO TÀI KHOẢN ---
    print("2. Đang tạo Tài khoản...")
    # Lấy danh sách ID khách hàng vừa tạo từ DB
    df_cust_ids = pd.read_sql("SELECT customer_id FROM staging.customers", engine)
    cust_ids = df_cust_ids['customer_id'].tolist()

    accounts = []
    for cid in cust_ids:
        # Mỗi khách hàng có 1 đến 2 tài khoản
        num_accounts = random.randint(1, 2)
        for _ in range(num_accounts):
            accounts.append({
                'customer_id': cid,
                'account_number': fake.unique.bban(),
                'account_type': random.choice(['Current', 'Saving']),
                'balance': round(random.uniform(100000, 500000000), 2),  # Số dư từ 100k đến 500 triệu
                'status': random.choice(['Active', 'Active', 'Active', 'Closed'])  # Đa số là Active
            })
    pd.DataFrame(accounts).to_sql('accounts', engine, schema='staging', if_exists='append', index=False)

    # --- TẠO GIAO DỊCH (Khoảng 50,000 giao dịch) ---
    print("3. Đang tạo Giao dịch (Transactions)...")
    df_acc_ids = pd.read_sql("SELECT account_id FROM staging.accounts WHERE status = 'Active'", engine)
    acc_ids = df_acc_ids['account_id'].tolist()

    transactions = []
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)  # Giao dịch trong 1 năm qua

    for _ in range(50000):
        # Tạo ngẫu nhiên giao dịch
        acc_id = random.choice(acc_ids)
        t_type = random.choice(['Transfer', 'Withdraw', 'Deposit'])

        # Cố tình tạo một vài giao dịch siêu lớn (Anomaly) để sau này phân tích Fraud
        if random.random() < 0.05:  # 5% xác suất
            amount = round(random.uniform(500000000, 2000000000), 2)  # 500 củ - 2 tỷ
        else:
            amount = round(random.uniform(50000, 20000000), 2)

        transactions.append({
            'account_id': acc_id,
            'transaction_date': fake.date_time_between(start_date=start_date, end_date=end_date),
            'amount': amount,
            'transaction_type': t_type,
            'ip_address': fake.ipv4()
        })

    # Ghi vào DB theo từng lô (chunk) để không bị treo máy
    pd.DataFrame(transactions).to_sql('transactions', engine, schema='staging', if_exists='append', index=False,
                                      chunksize=10000)

    print("✅ HOÀN TẤT! Ngân hàng của bạn đã có dữ liệu để phân tích.")


# Chạy chương trình
if __name__ == "__main__":
    generate_large_data()
