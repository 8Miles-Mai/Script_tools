
/* 一共 */
/* Formatted on 2014/5/24 11:40:09 (QP5 v5.256.13226.35538) */
  SELECT iir.comp_id, COUNT (DISTINCT (to_char(ii.inquiry_time, 'YYYY-mm-DD') || ii.sender_user_id)) num
    FROM im$inquiry ii, im$inq_recipient iir
   WHERE 1 = 1 AND ii.inquiry_id = iir.inquiry_id
   and ii.status = 7
   and iir.comp_id in (2045889,2018487,689609,3086480,721478,2409634,2058225,796790,1943580,1833646,1943593,1695515,717605,1833646)
   and iir.create_time >= to_date('2014-04-21', 'YYYY-mm-DD')
   and iir.create_time < to_date('2014-05-19', 'YYYY-mm-DD')
GROUP BY iir.comp_id
order by iir.comp_id asc;

/* 按月 */

/* Formatted on 2014/6/3 12:00:02 (QP5 v5.256.13226.35538) */
  SELECT st.compId,
         SUM (CASE WHEN st.mon = '2013-01' THEN num ELSE 0 END) mon1301,
         SUM (CASE WHEN st.mon = '2013-02' THEN num ELSE 0 END) mon1302,
         SUM (CASE WHEN st.mon = '2013-03' THEN num ELSE 0 END) mon1303,
         SUM (CASE WHEN st.mon = '2013-04' THEN num ELSE 0 END) mon1304,
         SUM (CASE WHEN st.mon = '2013-05' THEN num ELSE 0 END) mon1305,
         SUM (CASE WHEN st.mon = '2013-06' THEN num ELSE 0 END) mon1306,
         SUM (CASE WHEN st.mon = '2013-07' THEN num ELSE 0 END) mon1307,
         SUM (CASE WHEN st.mon = '2013-08' THEN num ELSE 0 END) mon1308,
         SUM (CASE WHEN st.mon = '2013-09' THEN num ELSE 0 END) mon1309,
         SUM (CASE WHEN st.mon = '2013-10' THEN num ELSE 0 END) mon1310,
         SUM (CASE WHEN st.mon = '2013-11' THEN num ELSE 0 END) mon1311,
         SUM (CASE WHEN st.mon = '2013-12' THEN num ELSE 0 END) mon1312,
         SUM (CASE WHEN st.mon = '2014-01' THEN num ELSE 0 END) mon1401,
         SUM (CASE WHEN st.mon = '2014-02' THEN num ELSE 0 END) mon1402,
         SUM (CASE WHEN st.mon = '2014-03' THEN num ELSE 0 END) mon1403,
         SUM (CASE WHEN st.mon = '2014-04' THEN num ELSE 0 END) mon1404,
         SUM (CASE WHEN st.mon = '2014-05' THEN num ELSE 0 END) mon1405
    FROM (  SELECT iir.comp_id compId,
                   COUNT (
                      DISTINCT (   TO_CHAR (ii.inquiry_time, 'YYYY-mm-DD')
                                || ii.sender_user_id))
                      num,
                   TO_CHAR (ii.inquiry_time, 'YYYY-mm') mon
              FROM im$inquiry ii, im$inq_recipient iir
             WHERE     1 = 1
                   AND ii.inquiry_id = iir.inquiry_id
                   AND ii.status = 7
                   AND iir.comp_id IN (SELECT sc.comp_id
                                         FROM seller$company sc
                                        WHERE sc.status = 7)
                   AND ii.inquiry_time >= TO_DATE ('2013-01-01', 'YYYY-mm-DD')
                   AND ii.inquiry_time < TO_DATE ('2014-06-01', 'YYYY-mm-DD')
          GROUP BY iir.comp_id, TO_CHAR (ii.inquiry_time, 'YYYY-mm') --order by iir.comp_id asc, to_char(ii.inquiry_time, 'YYYY-mm') asc
                                                                    ) st
   WHERE 1 = 1
GROUP BY st.compId
order by st.compId asc;