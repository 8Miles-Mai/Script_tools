select * from seller$prod_tag spt where spt.product_id = 524970 and spt.tag_id = 1;

--°Ñ2¸ÄÎª1
merge into seller$prod_tag spt
using (select count(0) num
         from seller$prod_tag
        where product_id = 524970
          and tag_id = 1) temp
on (temp.num <> 0)
when matched then
  update set spt.tag_id = 2, spt.last_update_time = sysdate where spt.product_id = 524970
          and spt.tag_id = 1
when not matched then
  insert values
    (gm_portal.sq_seller$prod_tag.nextval, 524970, 1, 0, 0, sysdate, 0, sysdate);