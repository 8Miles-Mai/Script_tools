/* Formatted on 2014/7/8 11:19:51 (QP5 v5.256.13226.35538) */
SELECT *
  FROM (SELECT sub.keyword keyword,
               sub.exCnt exposureTotalCount,
               sub.clCnt clickTotalCount,
               sub.pdCnt exposureProductNum,
               ROWNUM seqNo
          FROM (  SELECT ssp.keyword,
                         SUM (ssp.exposure_cnt) exCnt,
                         SUM (ssp.click_cnt) clCnt,
                         COUNT (DISTINCT (ssp.product_id)) pdCnt
                    FROM stat$search_kw_prod_hly ssp
                   WHERE     1 = 1
                         AND ssp.comp_id = :compId
                         AND (   (    ssp.year = :startYear
                                  AND ssp.month >= :startMonth)
                              OR (    ssp.year = :endYear
                                  AND ssp.month <= :endMonth))
                         AND ssp.full_date >= :startFullDate
                         AND ssp.full_date <= :endFullDate
                GROUP BY ssp.keyword
                ORDER BY exCnt DESC) sub)
 WHERE 1 = 1 AND seqNo <= :endRow AND seqNo >= :startRow
                                  
 
 paramMap={endRow=10, endYear=2014, compId=100609, endFullDate=20140708, startYear=2014, startRow=1, startFullDate=20140604, startMonth=6, endMonth=7}