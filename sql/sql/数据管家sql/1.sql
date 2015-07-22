/* Formatted on 2014/7/8 11:19:27 (QP5 v5.256.13226.35538) */
  SELECT ssk.keyword keyword,
         SUM (ssk.exposure_cnt) exposureCount,
         ssk.year year,
         ssk.month month,
         ssk.month_of_date dayOfMonth,
         TO_CHAR (TO_DATE (ssk.full_date, 'YYYY-mm-DD'), 'YYYYmmDD') fullDate,
         ssk.day time,
         SUM (ssk.click_cnt) clickCount,
         ssk.comp_id compId,
         sub.rk seqNo
    FROM (SELECT keyword, ROWNUM rk
            FROM (  SELECT keyword, SUM (exposure_cnt) cnt
                      FROM stat$search_kw_comp_hly
                     WHERE     1 = 1
                           AND comp_id = :compId
                           AND (   (year = :startYear AND month >= :startMonth)
                                OR (year = :endYear AND month <= :endMonth))
                           AND full_date >= :startFullDate
                           AND full_date <= :endFullDate
                  GROUP BY keyword
                  ORDER BY cnt DESC)
           WHERE ROWNUM <= 10) sub,
         stat$search_kw_comp_hly ssk
   WHERE     1 = 1
         AND ssk.keyword = sub.keyword
         AND comp_id = :compId
         AND (   (ssk.year = :startYear AND ssk.month >= :startMonth)
              OR (ssk.year = :endYear AND ssk.month <= :endMonth))
         AND ssk.full_date >= :startFullDate
         AND ssk.full_date <= :endFullDate
GROUP BY ssk.keyword,
         ssk.year,
         ssk.month,
         ssk.month_of_date,
         ssk.full_date,
         ssk.comp_id,
         sub.rk,
         ssk.day
ORDER BY sub.rk,
         ssk.year,
         ssk.month,
         ssk.month_of_date,
         ssk.day
                                                      
                paramMap={endYear=2014, compId=100609, endFullDate=20140708, startYear=2014, startFullDate=20140604, startMonth=6, endMonth=7}