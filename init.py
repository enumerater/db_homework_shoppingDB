import pymysql

# 连接
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='1234',
    charset='utf8mb4',
)

with connection.cursor() as cursor:
    # 创建数据库
    cursor.execute("create database if not exists shopping_db")
    cursor.execute("use shopping_db")
    # 创建表
    #用户表
    cursor.execute("""
        create table if not exists users
        (
            user_name varchar(10) not null,
            password varchar(10) not null,
            user_phone varchar(11),
            address varchar(50),
            primary key (user_name)
        )
    """)

    #商家表
    cursor.execute("""
        create table if not exists merchants
        (
            merchant_name varchar(10) not null,
            permission_num int,
            primary key (merchant_name)
        )
    """)

    #商品表
    cursor.execute("""
        create table if not exists goods
        (
            goods_id int auto_increment,
            goods_name varchar(10) not null,
            purchase_price float,
            price float,
            primary key (goods_id)
        )
    """)

    #订单表
    cursor.execute("""
        create table if not exists orders
        (
            order_id int auto_increment,
            user_name varchar(10) not null,
            order_time datetime,
            order_money float,
            primary key (order_id),
            foreign key (user_name) references users(user_name)
        )
    """)

    #购物车表
    cursor.execute("""
        create table if not exists cart
        (
            user_name varchar(10),
            goods_id int,
            goods_num int,
            primary key (user_name, goods_id,goods_num),
            foreign key (user_name) references users(user_name),
            foreign key (goods_id) references goods(goods_id)
        )
    """)

    #购买表
    cursor.execute("""
        create table if not exists user_goods
        (
            user_name varchar(10),
            goods_id int,
            primary key (user_name, goods_id),
            foreign key (user_name) references users(user_name),
            foreign key (goods_id) references goods(goods_id)
        )
    """)

    #上架表
    cursor.execute("""
        create table if not exists goods_merchants
        (
            goods_id int,
            merchant_name varchar(10),
            primary key (goods_id, merchant_name),
            foreign key (merchant_name) references merchants(merchant_name),
            foreign key (goods_id) references goods(goods_id)
        )
    """)




