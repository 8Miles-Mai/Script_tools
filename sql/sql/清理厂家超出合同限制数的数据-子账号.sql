DECLARE
   v_comp_count   NUMBER (10);

   --1.查询在oracle+mysql中，超出view视图数据的厂家
   CURSOR C_COMPS
   IS
      SELECT temp.compId compId,
               (temp.oraNum - temp.vvNum - temp.gNum) exNum
          FROM (SELECT vv.client_id compId,
                       vv.sub_accounts vvNum,
                       temp.selNum oraNum,
                       NVL ( (SELECT temp.gNum
                                FROM (SELECT 613918 compId, 1 gnum FROM DUAL
                                      UNION ALL
                                      SELECT 615569 compId, 1 gnum FROM DUAL
                                      UNION ALL
                                      SELECT 681609 compId, 1 gnum FROM DUAL
                                      UNION ALL
                                      SELECT 713870 compId, 1 gnum FROM DUAL
                                      UNION ALL
                                      SELECT 1827184 compId, 3 gnum FROM DUAL
                                      UNION ALL
                                      SELECT 1868902 compId, 1 gnum FROM DUAL
                                      UNION ALL
                                      SELECT 1918936 compId, 1 gnum FROM DUAL
                                      UNION ALL
                                      SELECT 2024982 compId, 1 gnum FROM DUAL
                                      UNION ALL
                                      SELECT 2036371 compId, 1 gnum FROM DUAL
                                      UNION ALL
                                      SELECT 2366150 compId, 1 gnum FROM DUAL
                                      UNION ALL
                                      SELECT 2605223 compId, 1 gnum FROM DUAL
                                      UNION ALL
                                      SELECT 2663525 compId, 1 gnum FROM DUAL) temp
                               WHERE temp.compId(+) = vv.client_id),
                            0)
                          gNum
                  FROM sfa08.vw_seller_servinfo vv,
                       (  SELECT wu.comp_Id, (COUNT (0) - 1) selNum
                            FROM web$user wu
                           WHERE wu.status = 7
                        GROUP BY wu.comp_id) temp
                 WHERE     1 = 1
                       AND vv.client_id = temp.comp_id
                       AND (vv.selected_products) < temp.selNum) temp
         WHERE 1 = 1 AND (temp.vvNum + temp.gNum) < temp.oraNum;
BEGIN
   DBMS_OUTPUT.put_line (' begin.');

   --2.以公司为单位循环处理
   FOR curr_comp IN C_COMPS
   LOOP
      BEGIN
         -- 4.冻结超出的子账号，按最近添加的冻结
        UPDATE web$user wu
               SET wu.status = -4,
                   wu.last_update_time = SYSDATE,
                   wu.last_update_by = 0
             WHERE     1 = 1
                   AND wu.comp_id = :compId
                   AND wu.user_id IN (SELECT us.user_id
                                        FROM (SELECT temp.user_id, ROWNUM num
                                                FROM (  SELECT wu.user_id
                                                          FROM web$user wu
                                                         WHERE     wu.comp_id = curr_comp.compId
                                                               AND wu.status = 7
                                                               AND NOT EXISTS
                                                                          (SELECT NULL
                                                                             FROM seller$company sc
                                                                            WHERE     sc.comp_id =
                                                                                         wu.comp_id
                                                                                  AND sc.owner_id =
                                                                                         wu.user_id)
                                                      ORDER BY wu.create_time DESC) temp)
                                             us
                                       WHERE us.num > 0 AND us.num <= :userNum);                              

      END;
   END LOOP;

   DBMS_OUTPUT.put_line (' end.');
END;