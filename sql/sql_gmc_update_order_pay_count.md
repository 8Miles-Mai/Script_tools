
## 更新订单金额 ##
#### 更新订单 ####
update sales_order
set total_amount = **, paid_amount = **, shipping_cost = **
where id = **;
#### 更新订单货品 ####
update order_item
set sku_price = **, sku_discount_price = **, shipping_amount = **, payment_price_share = **, payment_price_share_total = **
where order_id = **;
#### 更新订单运输信息 ####
update order_shipment
set shipping_cost = **, shipping_discount_amount = **, item_payment_subtotal = **
where order_id = **;
#### 取得订单运输信息ID ####
select id from order_shipment where order_id = **;
#### 更新订单运输货品信息 ####
update order_shipment_item
set sku_price = **, sku_discount_price = **
where order_shipment_id = **;
#### 拼接付款链接 ####
http://192.168.24.94:6090/soa/ordertradeservice/updateTrade.gm?tradeId=6113&payAmount=48.0000&paymentGateWay=ALIPAY&companyAcount=ALIPAY.globalmarket.com&transactionNumber=1267658044&success=1&userName=ALIPAY

