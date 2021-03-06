
#按厂家全天多次操作合计为单条记录统计，有3409条数据
SELECT count(0) as 条数, DATE_FORMAT(w.stat_date, '%Y-%m-%d') as 日期
  FROM `wla$client_action_daily` w
 WHERE w.stat_date >= '2014/2/17'
GROUP BY DATE_FORMAT(w.stat_date, '%Y-%m-%d')
ORDER BY DATE_FORMAT(w.stat_date, '%Y-%m-%d');


#按厂家全天分条记录统计，有23424条记录
SELECT sum(w.count) as 次数, DATE_FORMAT(w.stat_date, '%Y-%m-%d') as 日期
  FROM `wla$client_action_daily` w
 WHERE w.stat_date >= '2014/2/17'
GROUP BY DATE_FORMAT(w.stat_date, '%Y-%m-%d')
ORDER BY DATE_FORMAT(w.stat_date, '%Y-%m-%d');