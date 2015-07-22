/* Formatted on 2014/7/8 11:21:49 (QP5 v5.256.13226.35538) */
SELECT temp.product_id productId,
       temp.exCnt exposureCount,
       temp.clCnt clickCount,
       temp.craCnt ratio,
       (SELECT spk.keyword
          FROM seller$prod_keyword spk
         WHERE spk.product_id = temp.product_id AND spk.weight = 1)
          keyword,
       (SELECT sp.thumbnail
          FROM seller$product sp
         WHERE sp.product_id = temp.product_id)
          imagePath,
       (SELECT product_name
          FROM seller$product sp
         WHERE sp.product_id = temp.product_id)
          productName
  FROM (SELECT sub.product_id,
               sub.exCnt,
               sub.clCnt,
               sub.craCnt,
               ROWNUM seqNo
          FROM (  SELECT ssp.product_id,
                         SUM (ssp.exposure_cnt) exCnt,
                         ROUND (SUM (ssp.click_cnt) / SUM (ssp.exposure_cnt),
                                5)
                            craCnt,
                         SUM (ssp.click_cnt) clCnt
                    FROM stat$search_kw_prod_hly ssp
                   WHERE     1 = 1
                         AND ssp.keyword = :keyword
                         AND ssp.comp_id = :compId
                         AND (   (    ssp.year = :startYear
                                  AND ssp.month >= :startMonth)
                              OR (    ssp.year = :endYear
                                  AND ssp.month <= :endMonth))
                         AND ssp.full_date >= :startFullDate
                         AND ssp.full_date <= :endFullDate
                GROUP BY ssp.product_id
                ORDER BY exCnt DESC) sub) temp
 WHERE 1 = 1 AND temp.seqNo <= :endRow AND temp.seqNo >= :startRow
 
 
     paramMap={endRow=10, endYear=2014, compId=100609, endFullDate=20140708, orderBy=null, startYear=2014, orderType=null, startRow=1, keyword=meat grinder, startFullDate=20140604, startMonth=6, endMonth=7}