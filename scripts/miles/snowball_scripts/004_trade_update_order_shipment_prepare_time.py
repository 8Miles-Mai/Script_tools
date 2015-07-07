__author__ = 'miles'

from config import mysql_gmsales_prd as mysql_config
import mysqlDB

MYSQL_USER=mysql_config["MYSQL_USER"]
MYSQL_SERVER=mysql_config["MYSQL_SERVER"]
MYSQL_PASSWORD=mysql_config["MYSQL_PASSWORD"]
MYSQL_DB=mysql_config["MYSQL_DB"]
MYSQL_PORT=mysql_config["MYSQL_PORT"]

def get_order_item_prepare_max_time():
    print "start...get_order_item_prepare_max_time"
    print MYSQL_USER
    conn = mysqlDB.get_mysql_conn(MYSQL_USER, MYSQL_SERVER, MYSQL_PASSWORD, MYSQL_DB, MYSQL_PORT)
    curr = conn.cursor()
    sql="""
        SELECT item.order_id order_id,
          MAX(item.`processing_time`) process
        FROM
          `order_item` item 
        WHERE 1 = 1 
        GROUP BY item.order_id 
        ORDER BY item.order_id
        """
    curr.execute(sql)
    order_item_process = curr.fetchall()
    curr.close()
    conn.close()
    print "end...get_order_item_prepare_max_time"
    return order_item_process

def update_order_shipment_prepare_time(order_item_process):
    print "start...update_order_shipment_prepare_time"

    sql="""
        UPDATE `order_shipment` SET `goods_prepare_time` = %s, `last_update_by` = '-2' WHERE 1=1 AND `order_id` = %s
        """
    
    temp_data = []

    conn = mysqlDB.get_mysql_conn(MYSQL_USER, MYSQL_SERVER, MYSQL_PASSWORD, MYSQL_DB, MYSQL_PORT)
    curr = conn.cursor()

    for order in order_item_process:
        if not order[0]:
            continue
        if not order[1]:
            continue

        item = []
        item.append(str(order[1]))
        item.append(str(order[0]))
        temp_data.append(item)

    print "flush to mysql"
    curr.executemany(sql, temp_data)
    conn.commit()
    curr.close()
    conn.close()
    
    print "end...update_order_shipment_prepare_time"


if __name__ == '__main__':
    print "begin..."
    order_item_process = get_order_item_prepare_max_time()
    update_order_shipment_prepare_time(order_item_process)
    print "end..."

