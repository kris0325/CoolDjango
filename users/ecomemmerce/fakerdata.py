import mysql.connector
from faker import Faker
import random
from datetime import datetime, timedelta

# 创建 MySQL 数据库连接
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password='',
    database="ecommerce"
)

cursor = conn.cursor()

# 初始化Faker库
fake = Faker()


# 生成10000条客户数据
def generate_customers(n):
    for _ in range(n):
        customer_name = fake.name()
        email = fake.email()
        phone = fake.numerify(text='###-###-####')
        address = fake.address()
        city = fake.city()
        region = fake.state()
        postal_code = fake.postcode()
        cursor.execute("""
            INSERT INTO customers (customer_name, email, phone, address, city, region, postal_code) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (customer_name, email, phone, address, city, region, postal_code))
    conn.commit()


# 生成10000条送货数据
def generate_deliveries(n):
    for _ in range(n):
        courier_id = random.randint(1, 100)
        delivery_date = fake.date_between(start_date='-2y', end_date='today')
        delivery_address = fake.address()
        delivery_cost = round(random.uniform(5, 100), 2)
        expected_delivery_time = datetime.strptime(str(delivery_date), "%Y-%m-%d") + timedelta(
            days=random.randint(1, 5))
        delivery_time = expected_delivery_time + timedelta(hours=random.randint(-5, 5))
        distance_traveled = round(random.uniform(1, 100), 2)
        delivery_status = random.choice(['delivered', 'in transit', 'returned'])
        cursor.execute("""
            INSERT INTO deliveries (courier_id, delivery_date, delivery_address, delivery_cost, 
                                    expected_delivery_time, delivery_time, distance_traveled, delivery_status) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (courier_id, delivery_date, delivery_address, delivery_cost, expected_delivery_time, delivery_time,
              distance_traveled, delivery_status))
    conn.commit()


# 生成10000条订单数据
def generate_orders(n):
    for _ in range(n):
        customer_id = random.randint(1, 10000)
        order_date = fake.date_between(start_date='-2y', end_date='today')
        total_amount = round(random.uniform(50, 500), 2)
        delivery_id = random.randint(1, 10000)
        cursor.execute("""
            INSERT INTO orders (customer_id, order_date, total_amount, delivery_id)
            VALUES (%s, %s, %s, %s)
        """, (customer_id, order_date, total_amount, delivery_id))
    conn.commit()


# 生成1000条退货数据
def generate_returns(n):
    for _ in range(n):
        delivery_id = random.randint(1, 10000)
        return_date = fake.date_between(start_date='-1y', end_date='today')
        return_reason = fake.text(max_nb_chars=200)
        cursor.execute("""
            INSERT INTO returns (delivery_id, return_date, return_reason)
            VALUES (%s, %s, %s)
        """, (delivery_id, return_date, return_reason))
    conn.commit()


# 生成10000条送货反馈数据
def generate_delivery_feedback(n):
    for _ in range(n):
        delivery_id = random.randint(1, 10000)
        customer_id = random.randint(1, 10000)
        feedback_rating = random.randint(1, 5)
        feedback_comments = fake.text(max_nb_chars=200)
        feedback_date = fake.date_between(start_date='-1y', end_date='today')
        cursor.execute("""
            INSERT INTO delivery_feedback (delivery_id, customer_id, feedback_rating, feedback_comments, feedback_date)
            VALUES (%s, %s, %s, %s, %s)
        """, (delivery_id, customer_id, feedback_rating, feedback_comments, feedback_date))
    conn.commit()


# 生成数据
generate_customers(10000)
generate_deliveries(10000)
generate_orders(10000)
generate_returns(1000)
generate_delivery_feedback(10000)

# 关闭连接
cursor.close()
conn.close()
