DECLARE
   v_comp_count   NUMBER (10);

   --1.查询在oracle+mysql中，超出view视图数据的厂家
   CURSOR C_COMPS
   IS
      SELECT temp.compId compId, (temp.oraNum - temp.vvNum - temp.gNum) exNum
        FROM (SELECT vv.client_id compId,
                     VV.SELECTED_PRODUCTS vvNum,
                     temp.selNum oraNum,
                     NVL ( (SELECT temp.gNum
                              FROM (SELECT 1183 compId, 6 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 8336 compId, 2 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 29201 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 30768 compId, 7 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 31143 compId, 5 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 31481 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 41416 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 42545 compId, 5 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 42548 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 100419 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 100482 compId, 5 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 501169 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 602522 compId, 4 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 605254 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 608331 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 608548 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 608594 compId, 2 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 609060 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 609124 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 609438 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 610980 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 611520 compId, 2 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 612844 compId, 5 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 615569 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 617267 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 617912 compId, 41 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 618420 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 625225 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 627120 compId, 2 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 627666 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 682276 compId, 2 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 684387 compId, 2 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 685043 compId, 2 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 686356 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 692588 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 694338 compId, 2 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 694486 compId, 3 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 694760 compId, 4 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 694947 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 695041 compId, 2 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 696535 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 696595 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 699312 compId, 5 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 699587 compId, 3 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 701475 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 702596 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 705877 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 706838 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 708776 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 709679 compId, 5 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 711230 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 711966 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 712367 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 712680 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 712710 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 715672 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 716435 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 716486 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 718059 compId, 2 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 718191 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 723935 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 724580 compId, 2 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 724928 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 726174 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 727119 compId, 12 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 727420 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 728052 compId, 2 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 729592 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 729944 compId, 2 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 732381 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 732466 compId, 2 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 732512 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 733655 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 818469 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 918127 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 931491 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 934625 compId, 2 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 936384 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 939753 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 951291 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 951747 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 1689314 compId, 2 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 1692465 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 1692853 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 1695515 compId, 5 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 1698002 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 1701559 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 1704466 compId, 5 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 1716929 compId, 20 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 1718981 compId, 3 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 1801675 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 1801825 compId, 5 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 1806356 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 1811582 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 1814294 compId, 5 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 1817350 compId, 5 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 1830558 compId, 2 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 1831320 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 1835675 compId, 3 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 1837374 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 1839050 compId, 4 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 1842403 compId, 3 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 1868902 compId, 15 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 1877103 compId, 3 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 1881227 compId, 9 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 1885771 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 1898622 compId, 10 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 1898758 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 1898897 compId, 5 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 1900008 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 1905304 compId, 2 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 1909867 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 1917248 compId, 2 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 1919729 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 1919750 compId, 2 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 1921411 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 1921840 compId, 2 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 1922817 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 1927200 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 1938660 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 1939468 compId, 5 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 1943580 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 1943635 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 1945885 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 1948857 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 1948957 compId, 2 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 1950719 compId, 2 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 1954073 compId, 2 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 1971330 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 1976881 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 1998451 compId, 2 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2003325 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2005008 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2005056 compId, 5 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2011830 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2011955 compId, 2 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2015268 compId, 2 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2017922 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2022935 compId, 2 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2023421 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2024026 compId, 6 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2026292 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2041516 compId, 11 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2052534 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2058018 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2068975 compId, 5 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2080158 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2083408 compId, 7 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2084295 compId, 2 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2100065 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2122198 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2201419 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2276656 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2278326 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2283356 compId, 3 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2293821 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2302784 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2308089 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2343759 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2358662 compId, 2 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2371293 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2372321 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2403898 compId, 4 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2407866 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2409634 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2426649 compId, 2 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2466807 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2467900 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2476690 compId, 2 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2506953 compId, 3 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2525059 compId, 3 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2529931 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2533110 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2535540 compId, 5 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2538768 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2542498 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2578675 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2590994 compId, 2 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2592740 compId, 3 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2595326 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2600996 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2603104 compId, 4 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2605929 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2610069 compId, 2 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2615796 compId, 7 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2633329 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2651162 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2663050 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2663525 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2687575 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2690817 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2695773 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2705746 compId, 2 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2708499 compId, 5 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2713010 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2713258 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2718230 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2720944 compId, 3 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2733701 compId, 2 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2736167 compId, 2 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2740034 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2759077 compId, 2 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2767952 compId, 2 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2777639 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2794514 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2799557 compId, 2 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2808922 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2809186 compId, 3 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2810174 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2810285 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2816136 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2818069 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2818401 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2821735 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2825049 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2835581 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2864668 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2874400 compId, 4 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2874786 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2906185 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2911901 compId, 3 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 2979401 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 3016451 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 3048095 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 3079001 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 3082233 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 3092557 compId, 5 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 3105539 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 3113731 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 3129072 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 3129722 compId, 5 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 3144994 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 3145307 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 3145895 compId, 10 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 3146269 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 3146791 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 3147097 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 3147418 compId, 3 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 3147954 compId, 13 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 157418213 compId, 5 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 157431269 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 157434119 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 157442934 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 157455825 compId, 20 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 157476589 compId, 6 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 157476990 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 157477973 compId, 1 gnum FROM DUAL
                                    UNION ALL
                                    SELECT 157478573 compId, 2 gnum FROM DUAL) temp
                             WHERE temp.compId(+) = vv.client_id),
                          0)
                        gNum
                FROM sfa08.vw_seller_servinfo vv,
                     (  SELECT sp.comp_id, COUNT (0) selNum
                          FROM seller$product sp
                         WHERE     1 = 1
                               AND EXISTS
                                      (SELECT NULL
                                         FROM seller$prod_tag spt
                                        WHERE     spt.product_id = sp.product_id
                                              AND spt.tag_id = 2)
                      GROUP BY sp.comp_id) temp
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
         -- 4.删除超出的橱窗产品，按最近添加的删除
        delete from seller$prod_tag sptt                                  
               where sptt.prod_tag_id in                                        
                     (select prod.prod_tag_id                                   
                        from (select temp.prod_tag_id, rownum num               
                                from (select spt.prod_tag_id                    
                                        from seller$prod_tag spt                
                                       where 1 = 1                              
                                         and spt.tag_id = 2                
                                         and exists (select null                
                                                from seller$product sp          
                                               where sp.comp_id = curr_comp.compId       
                                                 and sp.status = 7)       
                                       order by spt.create_time desc) temp) prod
                       where prod.num > 0                                       
                         and prod.num <= curr_comp.exNum);                              

      END;
   END LOOP;

   DBMS_OUTPUT.put_line (' end.');
END;