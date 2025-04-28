import pymysql
import time
from decimal import Decimal

# Connect to the database
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='1234',
    database='shoppingdb',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)


with connection.cursor() as cursor:
    # Example query
    sql = "SELECT VERSION()"
    cursor.execute(sql)
    result = cursor.fetchone()
    print("Database version:", result)

try:
    with connection.cursor() as cursor:
        # Insert a new record into the users table
        sql = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
        cursor.execute(sql, ('new_user5', 'new_user@example.com', 'securepassword'))
        connection.commit()
        print("New user inserted successfully.")
except Exception as e:
    print("Error inserting new user:", e)


users = []

with connection.cursor() as cursor:
    # Read data from the users table
    sql = "SELECT * FROM users"
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        users.append(row)
        print(row)

# for i in range(len(users)):
#     with connection.cursor() as cursor:
#         # Insert a new record into the users table
#         sql = "INSERT INTO orders (user_id, total_price, order_time) VALUES (%s, %s, %s)"

#         price = Decimal('16.66')# 使用 Decimal 类型

#         cursor.execute(sql, (int(users[i]['id']), price,time.strftime('%Y-%m-%d %H:%M:%S')))
#         connection.commit()
#         print("New user inserted successfully.")


with connection.cursor() as cursor:
    # Read data from the users table
    sql = "SELECT * FROM orders"
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        print(row)

connection.close()