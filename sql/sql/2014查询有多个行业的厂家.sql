SELECT ww.comp_id, ww.num
  FROM (SELECT count(DISTINCT (w.ind_group_id)) num, w.comp_id, we.week_id, we.stat_date
          FROM `wla$client_action_daily` w, `wla$client_effect_daily_arc` we
         WHERE  1=1 
               AND w.year_id = 2013
               AND w.week_id IN
                      (49, 50)
               and we.comp_id = w.comp_id
               and we.week_id = w.week_id
               and we.year_id = w.year_id
               and we.ind_group_id = 0
        GROUP BY w.comp_id) ww
 WHERE ww.num > 1;