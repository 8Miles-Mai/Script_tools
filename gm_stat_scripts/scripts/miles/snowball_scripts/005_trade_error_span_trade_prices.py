__author__ = 'miles'

from config import mysql_m2cchinaerp_prd as mysql_config
import mysqlDB
import json
import xlwt
import time

MYSQL_USER=mysql_config["MYSQL_USER"]
MYSQL_SERVER=mysql_config["MYSQL_SERVER"]
MYSQL_PASSWORD=mysql_config["MYSQL_PASSWORD"]
MYSQL_DB=mysql_config["MYSQL_DB"]
MYSQL_PORT=mysql_config["MYSQL_PORT"]

def get_sku_span_prices_info():
    print "start...get_sku_span_prices_info"
    print MYSQL_USER
    conn = mysqlDB.get_mysql_conn(MYSQL_USER, MYSQL_SERVER, MYSQL_PASSWORD, MYSQL_DB, MYSQL_PORT)
    curr = conn.cursor()
    sql="""
        SELECT 
          ps.`product_id`,
          ps.product_sku_id,
          ps.`comp_id`,
          ps.`span_trade_prices` 
        FROM
          `erp$pro$product_sku` ps
        """
    curr.execute(sql)
    sku_spans = curr.fetchall()
    curr.close()
    conn.close()
    print "end...get_sku_span_prices_info"
    return sku_spans

def filter_for_error(sku_spans):
    print "start...filter_for_error"

    temp_data = []

    for span in sku_spans:
        if not span[0]:
            continue
        if not span[1]:
            continue
        if not span[2]:
            continue
        if not span[3]:
            continue

        item = []
        item.append(str(span[0]))
        item.append(str(span[1]))
        item.append(str(span[2]))
        item.append(json.loads(span[3]))
        # print span[3]
        # print type(span[3])
        temp_data.append(item)

    print "deal with spans"

    error_data = []

    for span in temp_data:
        size = len(span[3])
        if size == 1 or size == 0:
            continue
        lo0 = 0
        up0 = 0
        for item in span[3]:
            lo = 0
            up = 0
            for key in item:
                if str(key) == 'lo':
                    lo = item[key]
                if str(key) == 'up':
                    up = item[key]
            
            if int(lo0) <= int(up0) and int(lo) <= int(up) and int(up0) < int(lo):
                lo0 = lo
                up0 = up
                continue
            
            # if lo0 <= up0:
            #     print "1  ", "lo0=", lo0, "up0=", up0
            # if lo <= up:
            #     print "2  ", "lo=", lo, "up=", up
            # print "2.0  ", "lo=", lo, "up=", up
            # if int(lo) == int(up):
            #     print "2.1"
            # if int(lo) < int(up):
            #     print "2.2"
            # if int(lo) > int(up):
            #     print "2.3"
            # if up0 < lo:
            #     print "3  ", "up0=", up0, "lo=", lo
            error_data.append(span)
            print "error  ", "lo0=", lo0, "up0=", up0, "lo=", lo, "up=", up
            print span
            break
    
    # for error in error_data:
    #     print "error=", error
    
    print "end...filter_for_error"
    return error_data

def flush_to_xls(error_data):
    print "flushing to stat xml..."

    data=[]
    total=0
    wb = xlwt.Workbook()
    wsScore = wb.add_sheet('sku_span_prices_info')
    wsScore.write(0, 0, 'spu_id')
    wsScore.write(0, 1, 'sku_id')
    wsScore.write(0, 2, 'comp_id')
    wsScore.write(0, 3, 'span_trade_prices')

    index = 1
    for item_arr in error_data :
        wsScore.write(index, 0, item_arr[0])
        wsScore.write(index, 1, item_arr[1])
        wsScore.write(index, 2, item_arr[2])
        wsScore.write(index, 3, str(item_arr[3]))
        index=index+1
    nowdate = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    filePath = 'xls/'
    wbName = 'sku_span_prices_info_%s.xls' % nowdate
    wb.save(filePath + wbName)
    print "flush sku span prices into %s" % str(wbName)
    return str(wbName)

if __name__ == '__main__':
    print "begin..."
    sku_spans = get_sku_span_prices_info()
    error_data = filter_for_error(sku_spans)
    flush_to_xls(error_data)
    print "end..."

