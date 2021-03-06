#存放各种常用的SQL#

##Snowball相关##

###查询商品属性及值的类型###
	
	SELECT att.attribute_id,
		att.attr_type,
		att.attribute_name,
		atv.attr_value_type,
		atv.option_name
	FROM pra_product_attribute pra,
		att_attribute att,
		atv_attribute_value atv
	WHERE
		1 = 1
	AND pra.product_base_id = :productBaseId
	AND pra.attribute_id = att.attribute_id
	AND pra.attribute_value_id = atv.attribute_value_id;

###处理数据库存在相同自定义属性值不同ID的数据###

查询相同属性名的自定义属性>1

	SELECT cta.category_id,
		att.attribute_name,
		max(att.attribute_id) maxAttId,
		count(0) attNum
	FROM cta_category_attribute cta,
		att_attribute att
	WHERE 1 = 1
	AND cta.attribute_id = att.attribute_id
	AND att.attr_type = 'C'
	and cta.category_id = :leafCatId
	GROUP BY cta.category_id,
		att.attribute_name
	HAVING count(0) > 1;

查询相同属性名的自定义属性>1的需要替换并删除的属性

	SELECT cta.category_id,
		att.attribute_name,
		att.attribute_id
	FROM cta_category_attribute cta,
		att_attribute att
	WHERE 1 = 1
	AND cta.attribute_id = att.attribute_id
	AND att.attr_type = 'C'
	and cta.category_id = :leafCatId
	and att.attribute_name = :attributeName
	and att.attribute_id <> :maxAttId;
	
将需要替换删除的自定义属性的值的attId替换掉
	
	update atv_attribute_value
	set attribute_id = :maxAttId
	where attribute_id = :attributeId;

将商品的属性update为唯一的ID

	update pra_product_attribute 
	set attribute_id = :maxAttId
	where attribute_id = :attributeId;

删除多余的自定义属性

	delete from mfa_manufacture_attribute
	where 1 = 1
	and attribute_id in (attIdList);

	delete from att_attribute
	where 1 = 1
	and attribute_id in (attIdList);

查询相同分类下的相同自定义属性及属性值>1的

	SELECT cta.category_id leafCatId,
		att.attribute_id,
		att.attribute_name,
		atv.attr_value_type,
		atv.option_name,
		max(atv.attribute_value_id) maxAtvId,
		count(0) atvNum
	FROM cta_category_attribute cta,
		att_attribute att,
		atv_attribute_value atv
	WHERE 1 = 1
	AND cta.attribute_id = att.attribute_id
	AND att.attribute_id = atv.attribute_id
	AND atv.attr_value_type = 'C'
	AND cta.category_id = :leafCatId
	GROUP BY cta.category_id,
		att.attribute_id,
		att.attribute_name,
		atv.attr_value_type,
		atv.option_name
	HAVING count(0) > 1;

查询相同分类下的相同自定义属性及属性值>1的需要替换并删除的属性

	SELECT cta.category_id,
		att.attribute_id,
		att.attribute_name,
		atv.attr_value_type,
		atv.option_name,
		atv.attribute_value_id
	FROM cta_category_attribute cta,
		att_attribute att,
		atv_attribute_value atv
	WHERE 1 = 1
	AND cta.attribute_id = att.attribute_id
	AND att.attribute_id = atv.attribute_id
	AND atv.attr_value_type = 'C'
	AND cta.category_id = :leafCatId
	and att.attribute_id = :attribute_id
	and att.attribute_name = :attributeName
	and atv.attr_value_type = :attrValueType
	and atv.option_name = :optionName
	and atv.attribute_value_id <> :maxAtvId;

查询更新相同分类下的相同自定义属性值为同一个ID

	SELECT *
	FROM pra_product_attribute pra,
		pca_product_category pca
	WHERE 1 = 1
	AND pra.product_base_id = pca.product_base_id
	AND pra.attribute_id = :attributeId
	AND pra.attribute_value_id in (:atvIdList)
	AND pca.category_id = :leafCatId;

	update pra_product_attribute pra, pca_product_category pca
	set pra.attribute_value_id = :maxAtvId,
		pra.last_update_by = -1,
		pra.last_update_time = now()
	where 1 = 1
	and pra.product_base_id = pca.product_base_id
	and pra.attribute_id = :attributeId
	and pra.attribute_value_id in (:atvIdList)
	and pca.category_id = :leafCatId;

删除多余的自定义属性值

	delete from atv_attribute_value
	where 1 = 1
	and attribute_value_id in (:atvIdList);







##获取需要修改的id##


	SELECT cta.category_id,
			att.attribute_id,
			att.attribute_name,
			atv.attr_value_type,
			atv.option_name,
			atv.attribute_value_id,
			temp.maxAtvId
		FROM cta_category_attribute cta,
			att_attribute att,
			atv_attribute_value atv,
	(SELECT cta.category_id leafCatId,
			att.attribute_id,
			att.attribute_name,
			atv.attr_value_type,
			atv.option_name,
			max(atv.attribute_value_id) maxAtvId,
			count(0) atvNum
		FROM cta_category_attribute cta,
			att_attribute att,
			atv_attribute_value atv
		WHERE 1 = 1
		AND cta.attribute_id = att.attribute_id
		AND att.attribute_id = atv.attribute_id
		AND atv.attr_value_type = 'C'
		AND cta.category_id = 831
		GROUP BY cta.category_id,
			att.attribute_id,
			att.attribute_name,
			atv.attr_value_type,
			atv.option_name
		HAVING count(0) > 1 ) temp
	WHERE 1 = 1
		AND cta.attribute_id = att.attribute_id
		AND att.attribute_id = atv.attribute_id
		AND atv.attr_value_type = 'C'
		AND cta.category_id = 831
		and att.attribute_id = temp.attribute_id
		and att.attribute_name = temp.attribute_name
		and atv.option_name = temp.option_name
		and atv.attribute_value_id <> temp.maxAtvId;
		

asdas


		update pra_product_attribute pra, pca_product_category pca, 

		#select pra.attribute_value_id, pra.attribute_id, aa.*
		#from pra_product_attribute pra, pca_product_category pca, 
		(
		SELECT cta.category_id,
				att.attribute_id,
				att.attribute_name,
				atv.attr_value_type,
				atv.option_name,
				atv.attribute_value_id,
				temp.maxAtvId
			FROM cta_category_attribute cta,
				att_attribute att,
				atv_attribute_value atv,
		(SELECT cta.category_id leafCatId,
				att.attribute_id,
				att.attribute_name,
				atv.attr_value_type,
				atv.option_name,
				max(atv.attribute_value_id) maxAtvId,
				count(0) atvNum
			FROM cta_category_attribute cta,
				att_attribute att,
				atv_attribute_value atv
			WHERE 1 = 1
			AND cta.attribute_id = att.attribute_id
			AND att.attribute_id = atv.attribute_id
			AND atv.attr_value_type = 'C'
			AND cta.category_id = 830
			GROUP BY cta.category_id,
				att.attribute_id,
				att.attribute_name,
				atv.attr_value_type,
				atv.option_name
			HAVING count(0) > 1 ) temp
		WHERE 1 = 1
			AND cta.attribute_id = att.attribute_id
			AND att.attribute_id = atv.attribute_id
			AND atv.attr_value_type = 'C'
			AND cta.category_id = 830
			and att.attribute_id = temp.attribute_id
			and att.attribute_name = temp.attribute_name
			and atv.option_name = temp.option_name
			and atv.attribute_value_id <> temp.maxAtvId
		) aa
		set pra.attribute_value_id = aa.maxAtvId,
				pra.last_update_by = -1,
				pra.last_update_time = now()
		where 1 = 1
			and pra.product_base_id = pca.product_base_id
			and pra.attribute_id = aa.attribute_id
			and pra.attribute_value_id = aa.attribute_value_id
			and pca.category_id = 830;




## 直接update更新atv[重复属性] ##
	update atv_attribute_value atv, 
	(
	SELECT temp.maxAttId, att.attribute_id
		FROM cta_category_attribute cta,
			att_attribute att,
			(SELECT cta.category_id,
			att.attribute_name,
			max(att.attribute_id) maxAttId,
			count(0) attNum
		FROM cta_category_attribute cta,
			att_attribute att
		WHERE 1 = 1
		AND cta.attribute_id = att.attribute_id
		AND att.attr_type = 'C'
		and cta.category_id = 830
		GROUP BY cta.category_id,
			att.attribute_name
		HAVING count(0) > 1) temp
		WHERE 1 = 1
		AND cta.attribute_id = att.attribute_id
		AND att.attr_type = 'C'
		and cta.category_id = temp.category_id
		and att.attribute_name = temp.attribute_name
		and att.attribute_id <> temp.maxAttId) pp
	set atv.attribute_id = pp.maxAttId
	where 1 =1 
	and atv.attribute_id = pp.attribute_id;

## 直接update更新Pra[重复属性] ##

	update pra_product_attribute pra,
	(
	SELECT temp.maxAttId, att.attribute_id
		FROM cta_category_attribute cta,
			att_attribute att,
			(SELECT cta.category_id,
			att.attribute_name,
			max(att.attribute_id) maxAttId,
			count(0) attNum
		FROM cta_category_attribute cta,
			att_attribute att
		WHERE 1 = 1
		AND cta.attribute_id = att.attribute_id
		AND att.attr_type = 'C'
		and cta.category_id = 830
		GROUP BY cta.category_id,
			att.attribute_name
		HAVING count(0) > 1) temp
		WHERE 1 = 1
		AND cta.attribute_id = att.attribute_id
		AND att.attr_type = 'C'
		and cta.category_id = temp.category_id
		and att.attribute_name = temp.attribute_name
		and att.attribute_id <> temp.maxAttId) pp
	set pra.attribute_id = pp.maxAttId
		where pra.attribute_id = pp.attribute_id;

## 直接删除mfa[重复属性] ##

	delete from mfa_manufacture_attribute
		where 1 = 1
		and attribute_id in (
	SELECT att.attribute_id
		FROM cta_category_attribute cta,
			att_attribute att,
			(SELECT cta.category_id,
			att.attribute_name,
			max(att.attribute_id) maxAttId,
			count(0) attNum
		FROM cta_category_attribute cta,
			att_attribute att
		WHERE 1 = 1
		AND cta.attribute_id = att.attribute_id
		AND att.attr_type = 'C'
		and cta.category_id = 830
		GROUP BY cta.category_id,
			att.attribute_name
		HAVING count(0) > 1) temp
		WHERE 1 = 1
		AND cta.attribute_id = att.attribute_id
		AND att.attr_type = 'C'
		and cta.category_id = temp.category_id
		and att.attribute_name = temp.attribute_name
		and att.attribute_id <> temp.maxAttId
	);

## 删除重复属性att[重复属性] ##

	delete from att_attribute
	where 1 = 1
	and attribute_id in (

	);
	
	
## 查找需要修复的分类 ##
	select temp.category_id, count(0) from (
	SELECT cta.category_id,
			att.attribute_name,
			max(att.attribute_id) maxAttId,
			count(0) attNum
		FROM cta_category_attribute cta,
			att_attribute att
		WHERE 1 = 1
		AND cta.attribute_id = att.attribute_id
		AND att.attr_type = 'C'
		GROUP BY cta.category_id,
			att.attribute_name
		HAVING count(0) > 1) temp
	where 1 = 1
	group by temp.category_id;