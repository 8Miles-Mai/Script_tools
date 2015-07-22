
 SELECT gcp.*, temp.product_id product_id, temp.leaf_cat_id leafCatId
  FROM gm$cat_path gcp,
       (SELECT spc.leaf_cat_id, spc.product_id
          FROM seller$prod_cat spc
         WHERE 1 = 1 AND spc.product_id IN (3594476)) temp
 WHERE     1 = 1
       AND gcp.leaf_cat_id = temp.leaf_cat_id
       AND is_main3 = 'Y'
       AND (is_main2 = 'Y' OR is_main2 IS NULL)
       AND (is_main1 = 'Y' OR is_main1 IS NULL)