## Update Order Pay Amount ##

	## 开始
	begin;

	## 设置变量
	set @orderId = 订单ID;  
	set @itemPrice = 商品单价;  
	set @itemTotal = 商品总价;  
	set @shippingCost = 运费;  
	set @totalAmount = 订单总价;  
	set @shippingAmount = 运费;  
	set @transactionNumber = 交易号;  
	set @paymentGateWay = 交易网关;  
	set @companyAcount = 支付网关公司账号;  
	set @userName = 支付用户名;  

	## 更新语句
	update 
		sales_order so, 
		order_item oi,
		order_shipment os,
		order_shipment_item osi,
		trade t
	set 
		## 更新订单总价
		so.total_amount = @totalAmount,
		## 更新订单支付总价
		so.paid_amount = @totalAmount,
		## 更新订单运费
		so.shipping_cost = @shippingCost,
		## 更新订单商品总价
		so.item_subtoal = @itemTotal,
		## 更新商品单价
		oi.sku_price = @itemPrice,
		## 更新商品优惠后的单价
		oi.sku_discount_price = @itemPrice,
		## 更新商品的运费
		oi.shipping_amount = @shippingAmount,
		## 更新商品的支付分摊价
		oi.payment_price_share = @itemPrice,
		## 更新商品的支付分摊价的总价
		oi.payment_price_share_total = @itemTotal,
		## 更新商品的运费
		os.shipping_cost = @shippingCost,
		## 更新商品优惠后的运费
		os.shipping_discount_amount = @shippingCost,
		## 更新商品的支付总价
		os.item_payment_subtotal = @itemTotal,
		## 更新商品单价
		osi.sku_price = @itemPrice,
		## 更新商品优惠后的单价
		osi.sku_discount_price = @itemPrice,
		## 更新商品需要支付的总价
		t.amount = @totalAmount
	where 1 = 1
	and so.id = @orderId
	and oi.order_id = so.id
	and os.ordeR_id = so.id
	and osi.order_shipment_id = os.id
	and t.order_id = so.id;

	## 拼接支付链接
	select concat(
		'http://192.168.24.94:6090/soa/ordertradeservice/updateTrade.gm?tradeId=', 
		t.id, 
		'&payAmount=', 
		so.total_amount, 
		'&paymentGateWay=',
		@paymentGateWay,
		'&companyAcount=',
		@companyAcount,
		'&transactionNumber=', 
		@transactionNumber, 
		'&success=1&userName=',
		@userName
		)
	from trade t, sales_order so
	where 1 = 1
	and t.order_id = so.id
	and so.id = @orderId;
	
	## 提交
	commit;