   select sp.*
     from seller$product sp
    where sp.create_time > to_date('2013-12-11', 'YYYY-mm-DD')
      and sp.status in (7, 13)
      and not exists (select null
             from seller$object_assignment soa
            where soa.comp_id = sp.comp_id
              and soa.entity_id = sp.product_id)   ;       

              
              
              
SELECT *
  FROM seller$prod_photo
 WHERE product_id = 3807619  
 
 SELECT p.*
          FROM seller$company c, seller$product p
         WHERE c.comp_id = p.comp_id
           AND p.product_id = 3807619

select sp.product_id,
       sp.status,
       sc.status,
       sp.create_by,
       sp.create_time,
       sp.last_update_by,
       sp.last_update_time

select sp.create_time, sp.last_update_time, sp.product_id, sc.comp_id
  from seller$product sp, seller$company sc
 where sp.comp_id = sc.comp_id
   and sc.status = 7
   and sp.status = 7
   and not exists (select null
          from seller$prod_photo spp
         where spp.comp_id = sc.comp_id
           and spp.product_id = sp.product_id);
           
           select * from seller$prod_photo spp where spp.product_id = 256472;
           
           select
           
           3871698
           
           
select count(0) from seller$product sp where sp.status in (7, 13, -3) and sp.thumbnail is null;

select * from seller$pg_product spp where spp.prod_group_id = 62000 order by spp.create_time desc;
select * from seller$product_group spg where spg.comp_id = 33042 and spg.prod_group_id = 62000;


select * from seller$prod_attribute spa where spa.product_id = 3873985;


select count(0) from seller$product sp where sp.comp_id = 2775757 and sp.status = 7;




select * from seller$product sp where sp.product_id in (520972,972006,218185,513706,557084,214664,557229,214778,520978,214776,212261,513692,520993,557129,520975);
select * from seller$product sp where sp.product_id = 3871698;