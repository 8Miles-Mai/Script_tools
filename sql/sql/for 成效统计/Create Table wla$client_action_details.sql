CREATE TABLE `wla$client_action_details` (
  `client_action_details_id` int(10) NOT NULL AUTO_INCREMENT COMMENT 'Primary Key, auto incremental',
  `comp_id` int(10) NOT NULL COMMENT '厂家ID， 引用核心DB seller$companies. comp_id',
  `ind_group_id` int(2) NOT NULL COMMENT '行业分组ID， 引用核心DB gm$ind_groups.ing_group_id',
  `year_id` int(4) NOT NULL COMMENT '统计数据所属的年份；表中主可能出现当前年份与当前年份-1两个年份；取值范围1900-9999',
  `week_id` int(2) NOT NULL COMMENT '统计数据属于当年的第几周；取值范围1-52,\n            每周从周日开始到周六结束为一周的定义。',
  `stat_date` date NOT NULL COMMENT '统计数据的日期,  如 2012-5-28 ',
  `action_type` int(2) NOT NULL COMMENT '客户行为的统计类型，取值范围1-4；\n            1=登陆次数，\n            2=新增加产品数量，\n            3=产品更新数量，\n            4=回复买家数量，\n            ',
  `count` int(10) NOT NULL COMMENT '统计数字',
  `create_by` int(10) NOT NULL,
  `create_time` datetime NOT NULL,
  `last_update_by` int(10) NOT NULL,
  `last_update_time` datetime NOT NULL,
  `user_id` int(10) NOT NULL COMMENT `用户ID， 引用核心DB web$user. user_id`,
  `entity_id` int(10) NOT NULL COMMENT `实体ID， 厂家ID / 产品ID / 回复`
  PRIMARY KEY (`client_action_daily_id`),
  UNIQUE KEY `uk_stat$client_action_daily` (`stat_date`,`comp_id`,`user_id`,`action_type`),
  KEY `ix_wla$client_action_daily_sdate` (`stat_date`),
  KEY `ix_wla$client_action_daily_ui1` (`ind_group_id`,`action_type`,`year_id`,`week_id`),
  KEY `ix_wla$client_action_daily_ui2` (`year_id`,`week_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2501 DEFAULT CHARSET=utf8 COMMENT='WLA - Web Log Analysis\nDaily Statistics :  实时记录厂家用户对产品级采购需求等的操作统计';
