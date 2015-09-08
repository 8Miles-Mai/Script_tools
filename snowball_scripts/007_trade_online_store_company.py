__author__ = 'miles'
#coding:utf-8

from config import mysql_m2cchinaerp_prd as mysql_config
import mysqlDB
import json
import time
import httplib, urllib

MYSQL_USER=mysql_config["MYSQL_USER"]
MYSQL_SERVER=mysql_config["MYSQL_SERVER"]
MYSQL_PASSWORD=mysql_config["MYSQL_PASSWORD"]
MYSQL_DB=mysql_config["MYSQL_DB"]
MYSQL_PORT=mysql_config["MYSQL_PORT"]

def online_store_company():
    print "start...online_store_company"
    conn = mysqlDB.get_mysql_conn(MYSQL_USER, MYSQL_SERVER, MYSQL_PASSWORD, MYSQL_DB, MYSQL_PORT)
    curr = conn.cursor()
    sql="""
        UPDATE `m2cchinaerp`.`store$company` s, ( 
            SELECT DISTINCT(sc.`comp_id`)
            FROM
                `m2cchinaerp`.`store$company` sc,
                `m2cchinaerp`.`store$banner` head_banner, `m2cchinaerp`.`store$cfg$banner` head_banner_cfg,
                `m2cchinaerp`.`store$banner` hot_banner, `m2cchinaerp`.`store$cfg$banner` hot_banner_cfg
            WHERE 1=1
                AND sc.`status` = 0
                AND sc.`logo` IS NOT NULL
                AND head_banner.`comp_id` = sc.`comp_id` AND head_banner.`cfg_banner_id` = head_banner_cfg.`cfg_banner_id` and head_banner.`store_company_id` = sc.`store_company_id`
                AND head_banner_cfg.`type` = 1 AND head_banner.`status` = 7 AND  head_banner.`image` IS NOT NULL and head_banner_cfg.`market_region_code` = sc.`market_region_code`
                AND hot_banner.`comp_id` = sc.`comp_id` AND hot_banner.`cfg_banner_id` = hot_banner_cfg.`cfg_banner_id` and hot_banner.`store_company_id` = sc.`store_company_id`
                AND hot_banner_cfg.`type` = 2 AND hot_banner.`status` = 7 AND  hot_banner.`image` IS NOT NULL AND hot_banner.`link_entity_id` IS NOT NULL and hot_banner_cfg.`market_region_code` = sc.`market_region_code`
                AND EXISTS (
                    SELECT NULL FROM `gmcore`.`pro_product_base` pb
                    WHERE pb.`status` = 7 AND pb.`comp_id` = sc.`comp_id` and pb.market_region_code = sc.`market_region_code` GROUP BY pb.`comp_id` HAVING(COUNT(0) >= 10)
                )
                AND EXISTS (
                    SELECT NULL FROM `m2cchinaerp`.`store$group` sg, `m2cchinaerp`.`store$group_prod` sgp, `gmcore`.`pro_product_base` pb
                    WHERE sg.`group_id` = sgp.`group_id` AND sgp.`prod_base_id` = pb.`product_base_id` AND pb.`status` = 7
                    and sg.`store_company_id` = sc.`store_company_id`
                    and sgp.store_company_id = sc.store_company_id
                    and pb.market_region_code = sc.market_region_code
                    AND sg.`status` = 7 AND sg.`show_in_homepage` = 1
                    AND sg.`comp_id` = sc.`comp_id`
                    GROUP BY sg.`comp_id` HAVING(COUNT(0) > 3)
                )
            ) ols 
        SET s.`status` = 7 WHERE s.`comp_id` = ols.comp_id
        """

    curr.execute(sql)
    conn.commit()

    curr.close()
    conn.close()
    print "end...online_store_company"

def get_store_can_online_company_id_list():
    print "start...get_store_can_online_company_id_list"
    conn = mysqlDB.get_mysql_conn(MYSQL_USER, MYSQL_SERVER, MYSQL_PASSWORD, MYSQL_DB, MYSQL_PORT)
    curr = conn.cursor()
    sql="""
        SELECT DISTINCT(sc.`comp_id`)
        FROM 
            `m2cchinaerp`.`store$company` sc, 
            `m2cchinaerp`.`store$banner` head_banner, `m2cchinaerp`.`store$cfg$banner` head_banner_cfg,
            `m2cchinaerp`.`store$banner` hot_banner, `m2cchinaerp`.`store$cfg$banner` hot_banner_cfg
        WHERE 1=1
            AND sc.`status` = 0 
            AND sc.`logo` IS NOT NULL
            AND head_banner.`comp_id` = sc.`comp_id` AND head_banner.`cfg_banner_id` = head_banner_cfg.`cfg_banner_id` and head_banner.`store_company_id` = sc.`store_company_id`
            AND head_banner_cfg.`type` = 1 AND head_banner.`status` = 7 AND  head_banner.`image` IS NOT NULL and head_banner_cfg.`market_region_code` = sc.`market_region_code`
            AND hot_banner.`comp_id` = sc.`comp_id` AND hot_banner.`cfg_banner_id` = hot_banner_cfg.`cfg_banner_id` and hot_banner.`store_company_id` = sc.`store_company_id`
            AND hot_banner_cfg.`type` = 2 AND hot_banner.`status` = 7 AND  hot_banner.`image` IS NOT NULL AND hot_banner.`link_entity_id` IS NOT NULL and hot_banner_cfg.`market_region_code` = sc.`market_region_code`
            AND EXISTS (
                SELECT NULL FROM `gmcore`.`pro_product_base` pb
                WHERE pb.`status` = 7 AND pb.`comp_id` = sc.`comp_id` and pb.market_region_code = sc.`market_region_code` GROUP BY pb.`comp_id` HAVING(COUNT(0) >= 10)
            )
            AND EXISTS (
                SELECT NULL FROM `m2cchinaerp`.`store$group` sg, `m2cchinaerp`.`store$group_prod` sgp, `gmcore`.`pro_product_base` pb
                WHERE sg.`group_id` = sgp.`group_id` AND sgp.`prod_base_id` = pb.`product_base_id` AND pb.`status` = 7
                and sg.`store_company_id` = sc.`store_company_id`
                and sgp.store_company_id = sc.store_company_id
                and pb.market_region_code = sc.market_region_code
                AND sg.`status` = 7 AND sg.`show_in_homepage` = 1
                AND sg.`comp_id` = sc.`comp_id`
                GROUP BY sg.`comp_id` HAVING(COUNT(0) > 3)
            )
        ORDER BY sc.`comp_id`
        """

    comp_id_list = []

    curr.execute(sql)
    mysqlRs = curr.fetchall()
    for rs in mysqlRs:
        comp_id_list.append(rs[0])

    curr.close()
    conn.close()
    print "==== ==== ==== ====",current_time,"==== ==== ==== ===="
    print current_time,comp_id_list
    print "==== ==== ==== ====",current_time,"==== ==== ==== ===="
    print "end...get_store_can_online_company_id_list"
    return comp_id_list

if __name__ == '__main__':
    print "begin..."
    global current_time
    current_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    print current_time
    comp_id_list = get_store_can_online_company_id_list()
    if comp_id_list :
        online_store_company()
    print "end..."

