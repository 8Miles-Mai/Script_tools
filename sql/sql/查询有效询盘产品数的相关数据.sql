
--一、统计接收过有效询盘的产品数
SELECT COUNT(DISTINCT(iip.product_id))
  FROM im$inq_product iip
 WHERE 1 = 1
   AND iip.inq_recipient_id IN
       (SELECT iir.inq_recipient_id
          FROM im$inq_recipient iir
         WHERE 1 = 1
           AND EXISTS
         (SELECT NULL
                  FROM im$inquiry ii
                 WHERE ii.status = 7
                   AND ii.inquiry_id = iir.inquiry_id
                   AND ii.create_time >= to_date('2013-01-01', 'YYYY-mm-DD')
                   --AND ii.create_time < to_date('2014-01-01', 'YYYY-mm-DD')
                   ));
                   
--2013-01-01 到 2013-12-31 统计结果为： 654033
--2013-01-01 至今 统计结果为： 721585
--全部统计结果为： 958311
                   
--二、统计系统中的产品数【只统计删除、下线、在线 的产品】
select count(0)
  from seller$product sp
 where sp.status in (-3, 13, 7)
   --AND sp.create_time < to_date('2014-01-01', 'YYYY-mm-DD')
   --AND sp.create_time >= to_date('2013-01-01', 'YYYY-mm-DD');
   
--2013-01-01 到 2013-12-31 统计结果为： 2682861
--2013-01-01 至今 统计结果为： 2955249
--全部统计结果为： 4049057

--三、有效询盘产品的厂家数
select count(distinct(sp.comp_id))
  from seller$product sp
 where sp.product_id in
       (SELECT DISTINCT (iip.product_id)
          FROM im$inq_product iip
         WHERE 1 = 1
           AND iip.inq_recipient_id IN
               (SELECT iir.inq_recipient_id
                  FROM im$inq_recipient iir
                 WHERE 1 = 1
                   AND EXISTS
                 (SELECT NULL
                          FROM im$inquiry ii
                         WHERE ii.status = 7
                           AND ii.inquiry_id = iir.inquiry_id
                           --AND ii.create_time >= to_date('2013-01-01', 'YYYY-mm-DD')
                           --AND ii.create_time < to_date('2014-01-01', 'YYYY-mm-DD')
                           )));
                               
--2013-01-01 到 2013-12-31 统计结果为： 20583
--2013-01-01 至今 统计结果为： 21843
--全部统计结果为： 23091

--四、统计厂家总数
select count(0) 
  from seller$company sc
 where 1 = 1
   and ((sc.status = 7 and sc.create_time < to_date('2014-01-01', 'YYYY-mm-DD'))
       or
       (sc.status = 11 and sc.offline_time >= to_date('2013-01-01', 'YYYY-mm-DD')));

--统计结果为： 25792

