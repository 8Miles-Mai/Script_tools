/* Formatted on 2014/7/8 11:21:08 (QP5 v5.256.13226.35538) */
  SELECT ssk.keyword keyword,
         SUM (ssk.exposure_cnt) exposureCount,
         SUM (ssk.click_cnt) clickCount,
         SUM (ssk.sell_keyword_exp) sellKeywordExp,
         SUM (ssk.sell_keyword_click) sellKeywordClick,
         SUM (ssk.selected_exp) selectedExp,
         SUM (ssk.selected_click) selectedClick,
         SUM (ssk.nature_exp) natureExp,
         SUM (ssk.nature_click) natureClick,
         ssk.year year,
         ssk.month month,
         ssk.month_of_date dayOfMonth,
         ssk.day time,
         ssk.comp_id compId,
         TO_CHAR (TO_DATE (ssk.full_date, 'YYYY-mm-DD'), 'YYYY-mm-DD') fullDate
    FROM stat$search_kw_comp_hly ssk
   WHERE     1 = 1
         AND ssk.keyword = :keyword
         AND ssk.comp_id = :compId
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
         ssk.day
ORDER BY ssk.year,
         ssk.month,
         ssk.month_of_date,
         ssk.day
                                               paramMap={endYear=2014, compId=100609, endFullDate=20140708, startYear=2014, keyword=meat grinder, startFullDate=20140604, startMonth=6, endMonth=7}