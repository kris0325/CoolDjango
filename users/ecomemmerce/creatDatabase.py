import psycopg2
from psycopg2 import sql
from psycopg2.extras import register_uuid, execute_values
from faker import Faker
import random
import uuid
import concurrent.futures

# 数据库连接配置信息
db_config = {
    'host': 'localhost',
    'database': 'ecommerce',
    'user': 'kris',  # 替换为您的用户名
    'password': '',  # 替换为您的密码
}

# 创建数据库连接
def create_connection():
    conn = psycopg2.connect(**db_config)
    register_uuid()
    return conn

# 创建所有表
def create_tables(connection):
    try:
        with connection.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS customers (
                    customer_id UUID PRIMARY KEY,
                    name VARCHAR(255),
                    email VARCHAR(255),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    product_id UUID PRIMARY KEY,
                    name VARCHAR(255),
                    price DECIMAL(10, 2),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS orders (
                    order_id UUID PRIMARY KEY,
                    customer_id UUID REFERENCES customers(customer_id),
                    product_id UUID REFERENCES products(product_id),
                    quantity INT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS fulfillment (
                    fulfillment_id UUID PRIMARY KEY,
                    order_id UUID REFERENCES orders(order_id),
                    status VARCHAR(255),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS marketing (
                    marketing_id UUID PRIMARY KEY,
                    customer_id UUID REFERENCES customers(customer_id),
                    campaign_name VARCHAR(255),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            connection.commit()
            print("所有表创建完成。")
    except Exception as e:
        print(f"创建表时出错: {e}")

# 插入客户数据
def insert_customers(connection, total_records):
    fake = Faker()
    try:
        with connection.cursor() as cur:
            data = [(uuid.uuid4(), fake.name(), fake.email()) for _ in range(total_records)]
            execute_values(cur, "INSERT INTO customers (customer_id, name, email) VALUES %s", data)
            connection.commit()
            print(f"插入 {total_records} 条客户数据完成。")
    except Exception as e:
        print(f"插入客户数据时出错: {e}")

# 插入产品数据
def insert_products(connection, total_records):
    fake = Faker()
    try:
        with connection.cursor() as cur:
            data = [(uuid.uuid4(), fake.word(), round(random.uniform(10.0, 100.0), 2)) for _ in range(total_records)]
            execute_values(cur, "INSERT INTO products (product_id, name, price) VALUES %s", data)
            connection.commit()
            print(f"插入 {total_records} 条产品数据完成。")
    except Exception as e:
        print(f"插入产品数据时出错: {e}")

# 获取实际的客户和产品 ID
def get_ids(connection, table, id_column):
    with connection.cursor() as cur:
        cur.execute(f"SELECT {id_column} FROM {table}")
        return [row[0] for row in cur.fetchall()]

# 插入订单数据
def insert_orders(connection, total_records):
    try:
        with connection.cursor() as cur:
            customer_ids = get_ids(connection, 'customers', 'customer_id')
            product_ids = get_ids(connection, 'products', 'product_id')
            data = [
                (uuid.uuid4(), random.choice(customer_ids), random.choice(product_ids), random.randint(1, 10))
                for _ in range(total_records)
            ]
            execute_values(cur, "INSERT INTO orders (order_id, customer_id, product_id, quantity) VALUES %s", data)
            connection.commit()
            print(f"插入 {total_records} 条订单数据完成。")
    except Exception as e:
        print(f"插入订单数据时出错: {e}")

# 插入履约数据
def insert_fulfillment(connection, total_records):
    try:
        with connection.cursor() as cur:
            order_ids = get_ids(connection, 'orders', 'order_id')
            data = [
                (uuid.uuid4(), random.choice(order_ids), random.choice(['Shipped', 'Pending', 'Delivered']))
                for _ in range(total_records)
            ]
            execute_values(cur, "INSERT INTO fulfillment (fulfillment_id, order_id, status) VALUES %s", data)
            connection.commit()
            print(f"插入 {total_records} 条履约数据完成。")
    except Exception as e:
        print(f"插入履约数据时出错: {e}")

# 插入营销数据
def insert_marketing(connection, total_records):
    fake = Faker()
    try:
        with connection.cursor() as cur:
            customer_ids = get_ids(connection, 'customers', 'customer_id')
            data = [
                (uuid.uuid4(), random.choice(customer_ids), fake.catch_phrase())
                for _ in range(total_records)
            ]
            execute_values(cur, "INSERT INTO marketing (marketing_id, customer_id, campaign_name) VALUES %s", data)
            connection.commit()
            print(f"插入 {total_records} 条营销数据完成。")
    except Exception as e:
        print(f"插入营销数据时出错: {e}")

# 主函数
def main():
    total_records = 10000  # 每张表插入的记录数
    connection = create_connection()
    create_tables(connection)

    # 插入数据
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(insert_customers, connection, total_records),
            executor.submit(insert_products, connection, total_records),
        ]
        for future in concurrent.futures.as_completed(futures):
            future.result()  # 确保没有异常

        # 插入订单、履约和营销数据
        executor.submit(insert_orders, connection, total_records).result()
        executor.submit(insert_fulfillment, connection, total_records).result()
        executor.submit(insert_marketing, connection, total_records).result()

    connection.close()

if __name__ == "__main__":
    main()