


/* Formatted on 2014/6/5 16:08:26 (QP5 v5.256.13226.35538) */
  SELECT st.comp_id,
         SUM (CASE WHEN st.tag_id = 1 THEN 1 ELSE 0 END) newProd,
         SUM (CASE WHEN st.tag_id = 2 THEN 2 ELSE 0 END) selProd
    FROM (SELECT spt.tag_id, sp.comp_id
            FROM seller$prod_tag spt, seller$product sp
           WHERE 1 = 1 AND spt.product_id = sp.product_id) st
GROUP BY st.comp_id;



/* Formatted on 2014/6/5 16:11:26 (QP5 v5.256.13226.35538) */
SELECT sc.comp_id,
       sc.owner_id,
       (SELECT count(0)
          FROM seller$prod_tag spt
         WHERE     spt.tag_id = 1
               AND EXISTS
                      (SELECT NULL
                         FROM seller$product sp
                        WHERE 1 = 1 AND sp.comp_id = sc.comp_id and spt.product_id = sp.product_id)) newProd,
       (SELECT count(0)
          FROM seller$prod_tag spt
         WHERE     spt.tag_id = 2
               AND EXISTS
                      (SELECT NULL
                         FROM seller$product sp
                        WHERE 1 = 1 AND sp.comp_id = sc.comp_id and spt.product_id = sp.product_id)) selProd
  FROM seller$company sc
 WHERE 1 = 1 AND sc.status = 7;
 
 
 
 
/* Formatted on 2014/6/5 16:20:20 (QP5 v5.256.13226.35538) */
SELECT sc.comp_id,
       sc.owner_id,
       (SELECT count(spt.tag_id)
            FROM seller$prod_tag spt, seller$product sp
           WHERE 1 = 1 AND sp.comp_id = sc.comp_id and spt.tag_id = 1 and spt.product_id = sp.product_id)
          newProd,
       (SELECT count(spt.tag_id)
            FROM seller$prod_tag spt, seller$product sp
           WHERE 1 = 1 AND sp.comp_id = sc.comp_id and spt.tag_id = 2 and spt.product_id = sp.product_id)
          selProd
  FROM seller$company sc
 WHERE 1 = 1 AND sc.status = 7;
 
 
 select * from seller$prod_tag spt
 
 
 

/* Formatted on 2014/6/10 14:47:56 (QP5 v5.256.13226.35538) */

/* Formatted on 2014/6/10 14:51:36 (QP5 v5.256.13226.35538) */
/* Formatted on 2014/6/10 14:55:52 (QP5 v5.256.13226.35538) */
SELECT temp.comp_id compId,
          (SELECT sc.owner_id
             FROM seller$company sc
            WHERE sc.comp_id = temp.comp_id)
       || '|'
       || temp.info
          info
  FROM (  SELECT st.comp_id,
                 (   SUM (CASE WHEN st.tag_id = 1 THEN 1 ELSE 0 END)
                  || '|'
                  || SUM (CASE WHEN st.tag_id = 2 THEN 2 ELSE 0 END))
                    info
            FROM (SELECT spt.tag_id, sp.comp_id
                    FROM seller$prod_tag spt, seller$product sp
                   WHERE 1 = 1 AND spt.product_id = sp.product_id) st
        GROUP BY st.comp_id) temp
        
        
        
        
        
        



SELECT spt.tag_id, sp.comp_id
                    FROM seller$prod_tag spt, seller$product sp
                   WHERE 1 = 1 AND spt.product_id = sp.product_id
                   and sp.comp_id in (select sc.comp_id from seller$company sc where sc.status <> 7)