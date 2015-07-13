
select * from web$user wu where wu.comp_id = 3129072;

select sq_seller$pg_product.nextval, (select sp.product_id from  seller$product sp where sp.status = 7 and sp.comp_id = 100609 and sp.product_id in (101950, 101960, 101963)) from dual

select * from seller$pg_product spp 

insert into seller$pg_product spp (
select sq_seller$pg_product.nextval, :groupId, sp.product_id, :compId
  from seller$product sp, dual
 where sp.status in (7, 13)
   and sp.comp_id = 100609
   and sp.product_id in (101950, 101960, 101963)
   and not exists (select null
          from seller$pg_product spp
         where spp.product_id = sp.product_id)
)


insert into seller$pg_product spp
  (select gm_portal.sq_seller$pg_product.nextval,
          :groupId, sp.product_id, :compId,
          (select max(spd.seq_no) + 1
             from seller$pg_product spd
            where spd.prod_group_id = :groupId) seqNo,
          :userId, sysdate, :userId, sysdate
     from seller$product sp, dual
    where 1 = 1
      and sp.status in (7, 13)
      and sp.comp_id = :compId
      and not exists (select null
             from seller$pg_product spp
            where spp.product_id = sp.product_id))


select * from seller$pg_product spp where spp.comp_id = 100609