#曝光
select st.compId, st.month, sum(st.amount) 
from (
  select comp_id compId, month(stat_date) month, count amount from `wla$client_effect_daily_arc` where comp_id in (2045889,2018487,689609,3086480,721478,2409634,2058225,796790,1943580,1833646,1943593,1695515,717605,1833646) and year_id = 2014 and stat_type = 5
  union all
  select comp_id compId, month(stat_date) month, count amount from `wla$client_effect_daily` where comp_id in (2045889,2018487,689609,3086480,721478,2409634,2058225,796790,1943580,1833646,1943593,1695515,717605,1833646) and year_id = 2014 and stat_type = 5
) st
group by st.compId, st.month;





#点击
select st.compId, st.month, sum(st.amount) 
from (
  select comp_id compId, month(stat_date) month, count amount from `wla$client_effect_daily_arc` where comp_id in (2045889,2018487,689609,3086480,721478,2409634,2058225,796790,1943580,1833646,1943593,1695515,717605,1833646) and year_id = 2014 and stat_type = 6
  union all
  select comp_id compId, month(stat_date) month, count amount from `wla$client_effect_daily` where comp_id in (2045889,2018487,689609,3086480,721478,2409634,2058225,796790,1943580,1833646,1943593,1695515,717605,1833646) and year_id = 2014 and stat_type = 6
) st
group by st.compId, st.month;



SELECT st.compId, sum(st.amount)
  FROM (SELECT comp_id compId, count amount
          FROM `wla$client_effect_daily_arc`
         WHERE     comp_id IN
                      (689609,717605,721478,796790,1695515,1833646,1943580,1943593,2018487,2045889,2058225,2409634,3086480)
               AND year_id = 2014
               and stat_date >= '2014-05-19'
               and stat_date < '2014-05-26'
               AND stat_type = 5
        UNION ALL
        SELECT comp_id compId, count amount
          FROM `wla$client_effect_daily`
         WHERE     comp_id IN
                      (689609,717605,721478,796790,1695515,1833646,1943580,1943593,2018487,2045889,2058225,2409634,3086480)
               AND year_id = 2014
               and stat_date >= '2014-05-19'
               and stat_date < '2014-05-26'
               AND stat_type = 5) st
GROUP BY st.compId;





SELECT st.compId, sum(st.amount)
  FROM (SELECT comp_id compId, count amount
          FROM `wla$client_effect_daily_arc`
         WHERE     comp_id IN
                      (2045889,
                       2018487,
                       689609,
                       3086480,
                       721478,
                       2409634,
                       2058225,
                       796790,
                       1943580,
                       1833646,
                       1943593,
                       1695515,
                       717605,
                       1833646)
               AND year_id = 2014
               and stat_date >= '2014-04-21'
               and stat_date < '2014-05-19'
               AND stat_type = 6
        UNION ALL
        SELECT comp_id compId, count amount
          FROM `wla$client_effect_daily`
         WHERE     comp_id IN
                      (2045889,
                       2018487,
                       689609,
                       3086480,
                       721478,
                       2409634,
                       2058225,
                       796790,
                       1943580,
                       1833646,
                       1943593,
                       1695515,
                       717605,
                       1833646)
               AND year_id = 2014
               and stat_date >= '2014-04-21'
               and stat_date < '2014-05-19'
               AND stat_type = 6) st
GROUP BY st.compId;