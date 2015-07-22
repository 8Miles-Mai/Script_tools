
--һ��ͳ�ƽ��չ���Чѯ�̵Ĳ�Ʒ��
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
                   
--2013-01-01 �� 2013-12-31 ͳ�ƽ��Ϊ�� 654033
--2013-01-01 ���� ͳ�ƽ��Ϊ�� 721585
--ȫ��ͳ�ƽ��Ϊ�� 958311
                   
--����ͳ��ϵͳ�еĲ�Ʒ����ֻͳ��ɾ�������ߡ����� �Ĳ�Ʒ��
select count(0)
  from seller$product sp
 where sp.status in (-3, 13, 7)
   --AND sp.create_time < to_date('2014-01-01', 'YYYY-mm-DD')
   --AND sp.create_time >= to_date('2013-01-01', 'YYYY-mm-DD');
   
--2013-01-01 �� 2013-12-31 ͳ�ƽ��Ϊ�� 2682861
--2013-01-01 ���� ͳ�ƽ��Ϊ�� 2955249
--ȫ��ͳ�ƽ��Ϊ�� 4049057

--������Чѯ�̲�Ʒ�ĳ�����
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
                               
--2013-01-01 �� 2013-12-31 ͳ�ƽ��Ϊ�� 20583
--2013-01-01 ���� ͳ�ƽ��Ϊ�� 21843
--ȫ��ͳ�ƽ��Ϊ�� 23091

--�ġ�ͳ�Ƴ�������
select count(0) 
  from seller$company sc
 where 1 = 1
   and ((sc.status = 7 and sc.create_time < to_date('2014-01-01', 'YYYY-mm-DD'))
       or
       (sc.status = 11 and sc.offline_time >= to_date('2013-01-01', 'YYYY-mm-DD')));

--ͳ�ƽ��Ϊ�� 25792

