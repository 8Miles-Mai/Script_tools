/* Formatted on 2013/12/10 12:25:56 (QP5 v5.256.13226.35538) */
DECLARE
   v_comp_count   NUMBER (10);
   v_groupId      NUMBER (10);

   --1.查询公司id
   CURSOR C_COMPS
   IS
      SELECT DISTINCT comp_id compid
        FROM seller$products sp
       WHERE     NOT EXISTS
                    (SELECT NULL
                       FROM seller$pg_products spp
                      WHERE spp.product_id = sp.product_id)
             AND status IN (7, 13, -3);
BEGIN
   DBMS_OUTPUT.put_line (' begin.');

   --2.以公司为单位循环处理
   FOR curr_comp IN C_COMPS
   LOOP
      BEGIN
         -- 3.查找到‘Others’分组的ID
         SELECT spg.prod_group_id
           INTO v_groupId
           FROM seller$product_groups spg
          WHERE     1 = 1
                AND spg.comp_id = curr_comp.compId
                AND spg.prod_group_name = 'Others';

         --4.将该公司没有设置分组的产品【上线、下线状态】全部设置到‘Others’分组中
         INSERT INTO seller$pg_products spp
            SELECT gm_portal.sq_seller$pg_product.NEXTVAL,
                   v_groupId,
                   sp.product_id,
                   curr_comp.compId,
                   (SELECT MAX (spd.seq_no) + 1
                      FROM seller$pg_products spd
                     WHERE spd.prod_group_id = v_groupId)
                      seqNo,
                   -2,
                   SYSDATE,
                   -2,
                   SYSDATE
              FROM seller$products sp
             WHERE     1 = 1
                   AND sp.status IN (7, 13, -3)
                   AND sp.comp_id = curr_comp.compId
                   AND NOT EXISTS
                          (SELECT NULL
                             FROM seller$pg_products spp
                            WHERE spp.product_id = sp.product_id);
      --         v_comp_count := v_comp_count + 1;
      --         DBMS_OUTPUT.put_line (
      --            'The ' || v_comp_count || ' comp record had done.');
      --         COMMIT;
      --      EXCEPTION
      --         WHEN OTHERS
      --         THEN
      --            BEGIN
      --               DBMS_OUTPUT.put_line (
      --                     ' ERROR HINT. seller$company.comp_id : '
      --                  || curr_comp.compId);
      --               CONTINUE;
      --            END;
      END;
   END LOOP;

   DBMS_OUTPUT.put_line (' end.');
END;