-- 触发器1：在删除商品时，自动删除相关的订单项
create trigger trg_goods_delete_cascade
after delete on goods
for each row
begin
    delete from orders where goods_id = OLD.goods_id;
end;

