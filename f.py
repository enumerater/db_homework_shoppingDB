import aiomysql
import fastapi
import datetime
import uvicorn

app = fastapi.FastAPI()

# 异步获取连接池
async def get_pool():
    return await aiomysql.create_pool(
        host='localhost',
        user='root',
        password='1234',
        db='shopping_db',
        charset='utf8mb4',
        autocommit=True
    )

@app.get("/")
async def read_root():
    return {"Hello": "World"}

# 查询用户
@app.get("/user")
async def get_user(user_name: str):
    pool = await get_pool()
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            await cursor.execute("select * from users where user_name = %s", (user_name,))
            result = await cursor.fetchone()
    pool.close()
    await pool.wait_closed()
    return result

# 查询商家
@app.get("/merchant")
async def get_merchant(merchant_name: str):
    pool = await get_pool()
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            await cursor.execute("select * from merchants where merchant_name = %s", (merchant_name,))
            result = await cursor.fetchone()
    pool.close()
    await pool.wait_closed()
    return result

# 查询商品
@app.get("/goods")
async def get_goods(goods_id: int):
    pool = await get_pool()
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            await cursor.execute("select * from goods where goods_id = %s", (goods_id,))
            result = await cursor.fetchone()
    pool.close()
    await pool.wait_closed()
    return result

# 查询订单
@app.get("/order")
async def get_order(order_id: int):
    pool = await get_pool()
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            await cursor.execute("select * from orders where order_id = %s", (order_id,))
            result = await cursor.fetchone()
    pool.close()
    await pool.wait_closed()
    return result

# 增加用户
@app.post("/user")
async def create_user(user_name: str, user_password: str):
    pool = await get_pool()
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("insert into users (user_name, password) values (%s, %s)", (user_name, user_password))
            await conn.commit()
    pool.close()
    await pool.wait_closed()
    return {"message": "User created successfully"}

# 增加商家
@app.post("/merchant")
async def create_merchant(merchant_name: str,permission_num:str):
    pool = await get_pool()
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("insert into merchants (merchant_name, permission_num) values (%s, %s)", (merchant_name, permission_num))
            await conn.commit()
    pool.close()
    await pool.wait_closed()
    return {"message": "Merchant created successfully"}

#增加商品
@app.post("/goods")
async def create_goods(goods_name: str, purchase_price: float, price: float):
    pool = await get_pool()
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("insert into goods (goods_name, purchase_price, price) values (%s, %s, %s)", (goods_name, purchase_price, price))
            await conn.commit()
    pool.close()
    await pool.wait_closed()
    return {"message": "Goods created successfully"}

# 修改用户
@app.post("/user/update")
async def update_user(
    old_user_name: str,
    password: str,
    user_phone: str,
    address: str,
    new_user_name: str
):
    pool = await get_pool()
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(
                "update users set user_name = %s, password = %s, user_phone = %s, address = %s where user_name = %s",
                (new_user_name, password, user_phone, address, old_user_name)
            )
            await conn.commit()
    pool.close()
    await pool.wait_closed()
    return {"message": "User updated successfully"}

# 加入购物车
@app.post("/cart")
async def add_to_cart(
    user_name: str,
    goods_id: int,
    goods_num: int
):
    pool = await get_pool()
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            # 检查商品是否存在
            await cursor.execute("select * from goods where goods_id = %s", (goods_id,))
            goods = await cursor.fetchone()
            if not goods:
                raise fastapi.HTTPException(status_code=404, detail="商品不存在")

            # 检查用户是否存在
            await cursor.execute("select * from users where user_name = %s", (user_name,))
            user = await cursor.fetchone()
            if not user:
                raise fastapi.HTTPException(status_code=404, detail="用户不存在")

            # 插入购物车
            await cursor.execute(
                "insert into cart (user_name, goods_id, goods_num) values (%s, %s, %s)",
                (user_name, goods_id, goods_num)
            )
            await conn.commit()
    pool.close()
    await pool.wait_closed()
    return {"message": "Added to cart successfully"}

# 提交订单
@app.post("/order")
async def create_order(
    user_name: str,
):
    pool = await get_pool()
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            # 查询用户购物车
            await cursor.execute("select * from cart where user_name = %s", (user_name,))
            cart_items = await cursor.fetchall()
            if not cart_items:
                raise fastapi.HTTPException(status_code=400, detail="购物车为空，无法提交订单")

            # 统计购物车总金额
            total_amount = 0
            for item in cart_items:
                await cursor.execute("select price from goods where goods_id = %s", (item[1],))
                goods = await cursor.fetchone()
                if goods:
                    total_amount += item[1] * item[2]   

            # 插入订单
            await cursor.execute(
                "insert into orders (user_name, order_time, order_money) values (%s, %s, %s)",
                (user_name, datetime.datetime.now(), total_amount)
            )

            # 清空购物车
            await cursor.execute("DELETE FROM cart WHERE user_name = %s", (user_name,))
            await conn.commit()
    pool.close()
    await pool.wait_closed()
    return {"message": "Order created successfully"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
