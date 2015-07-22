UPDATE `wla$client_effect_daily_arc` w
   SET w.ind_group_id =
          (SELECT DISTINCT (q.ind_group_id)
             FROM `wla$client_action_daily` q
            WHERE     q.comp_id = w.comp_id
                  AND q.year_id = 2013
                  AND q.week_id in (24,25,26,27,28,29,30,31,32,33,34)),
       w.last_update_by = 12,
       w.last_update_time = now()
 WHERE w.year_id = 2013 AND w.week_id IN (50, 49) AND w.ind_group_id = 0