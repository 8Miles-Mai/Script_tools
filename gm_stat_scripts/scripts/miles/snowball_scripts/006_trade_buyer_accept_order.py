__author__ = 'miles'

from config import mysql_gmsales_prd as mysql_config
import mysqlDB
import json
import time
import httplib, urllib

MYSQL_USER=mysql_config["MYSQL_USER"]
MYSQL_SERVER=mysql_config["MYSQL_SERVER"]
MYSQL_PASSWORD=mysql_config["MYSQL_PASSWORD"]
MYSQL_DB=mysql_config["MYSQL_DB"]
MYSQL_PORT=mysql_config["MYSQL_PORT"]

def accept_order(order_id_list):
    print "start...accept_order"
    for id in order_id_list:
        if not id:
            continue
        print id
        params = urllib.urlencode({'orderId' : id, 'account' : order_id_list[id][3]})
        print params

        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        conn = httplib.HTTPConnection("192.168.24.94", 6090)
        conn.request("POST", "/soa/orderprocessservice/acceptOrder.gm", params, headers)
        response = conn.getresponse()
        print id, response.status, response.reason
        data = response.read()
        print data
        conn.close
    print "end...accept_order"

def get_order_id_by_number(number_list):
    print "start...get_order_id_by_number"
    print MYSQL_USER
    conn = mysqlDB.get_mysql_conn(MYSQL_USER, MYSQL_SERVER, MYSQL_PASSWORD, MYSQL_DB, MYSQL_PORT)
    curr = conn.cursor()
    sql="""
        SELECT
            id orderId,
            number,
            status,
            acount_name
        FROM
            gmsales.sales_order so
        WHERE
            so.number IN %s
        """

    temp_data = []
    order_id_list = {}
    order_number_list = []
    for number in number_list:
        order_number_list.append(str(number))

    temp_data.append(tuple(order_number_list))

    print sql % tuple(temp_data)

    # for mysqlRs in curr.execute(sql, tuple(temp_data)):
    #     item_arr=[]
    #     item_arr.append(mysqlRs[0])
    #     item_arr.append(mysqlRs[1])
    #     order_id_list[str(mysqlRs[0])] = item_arr

    curr.execute(sql % tuple(temp_data))
    mysqlRs = curr.fetchall()
    for rs in mysqlRs:
        item_arr=[]
        item_arr.append(rs[0])
        item_arr.append(rs[1])
        item_arr.append(rs[2])
        item_arr.append(rs[3])
        order_id_list[str(rs[0])] = item_arr

    curr.close()
    conn.close()
    print "end...get_order_id_by_number"
    return order_id_list

if __name__ == '__main__':
    print "begin..."
    number_list = [
        'TB10000883421424749786850'
	,'TB10000883421424749383783'
	,''
    ]
    order_id_list = get_order_id_by_number(number_list)
    accept_order(order_id_list)
    print "end..."

