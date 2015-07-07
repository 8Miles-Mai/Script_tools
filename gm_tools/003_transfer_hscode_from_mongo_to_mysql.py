#!/usr/bin/python
import pymongo
import MySQLdb

MONGO_URL = "mongodb://192.168.86.51:27017/snowball"
MONGO_USER_NAME = "app_soa"
MONGO_PASSWORD = "app_soa"
MONGO_DB = "snowball"

MYSQL_SERVER = "192.168.86.121"
MYSQL_USER = "root"
MYSQL_PASSWORD = "123456"
MYSQL_DB = "m2cchinaerp"
MYSQL_PORT = 3306

#MONGO_URL = "mongodb://192.168.24.88:27017/snowball"
#MONGO_USER_NAME = "app_soa"
#MONGO_PASSWORD = "app_soa"
#MONGO_DB = "snowball"

#MYSQL_SERVER = "192.168.24.240"
#MYSQL_USER = "app_erp"
#MYSQL_PASSWORD = "IntoErpOK"
#MYSQL_DB = "m2cchinaerp"
#MYSQL_PORT = 3308

def get_mysql_conn():
    try:
        mysql_conn = MySQLdb.connect(user=MYSQL_USER,
                  charset='utf8',
                  host=MYSQL_SERVER,
                  passwd=MYSQL_PASSWORD,
                  db=MYSQL_DB,
                  port=MYSQL_PORT)
        return mysql_conn
    except Exception, e:
    	print e
        ERROR_HINT = " [ get mysql connection failed ] MYSQL_USER:"+MYSQL_USER+", MYSQL_SERVER:"+MYSQL_SERVER+", MYSQL_DB:"+MYSQL_DB
        return None

def get_mongo_conn():
    try:
        mongo_conn = pymongo.MongoClient(host=MONGO_URL, safe=True, read_preference=pymongo.ReadPreference.SECONDARY)
        mongo_conn.admin.authenticate(MONGO_USER_NAME, MONGO_PASSWORD)
        return mongo_conn
    except Exception, e:
        print e
        ERROR_HINT = " [ get mongo connection failed ] MONGO_URL:"+MONGO_URL+", MONGO_USER_NAME:"+MONGO_USER_NAME+", MONGO_PASSWORD:"+MONGO_PASSWORD
        return None

def generate_hscode_from_mysql(data_list):
    conn = get_mysql_conn()
    curr = conn.cursor()
    sql="""
         SELECT
              pp.`product_id` productId,
              pps.`m2b_prod_id` m2bProductId,
              pps.`comp_id` compId,
              pp.`sales_markets` salesMarkets,
              st.`hs_code` hsCode
            FROM
              `erp$pro$product` pp,
              `erp$pro$product_sku` pps,
              `erp$pro$sku_trade_info` st
            WHERE 1 = 1
              AND pps.product_id = pp.product_id
              AND st.`product_sku_id` = pps.`product_sku_id`
        """
              #     AND pps.`m2b_prod_id` IN %s
              # AND pps.`comp_id` IN %s
    temp_data = []
    m2bProdIds = []
    compIds = []
    counter = 0
    data_map = {}
    for data in data_list:
        data_map[data['m2bProductId']] = data
        # m2bProdIds.append(data['m2bProductId'])
        # compIds.append(data['compId'])
        
    # print data_map
    # print type(data_map)
    # tmp_arr = []
    # tmp_arr.append(tuple(m2bProdIds))
    # tmp_arr.append(tuple(compIds))
    # temp_data.append(tuple(tmp_arr))
    # curr.executemany(sql, temp_data)
    curr.execute(sql)
    hscode_list = curr.fetchall()
    tmp_arr = {}
    for doc in hscode_list:
        tmp_arr[doc[1]] = doc
        
    global eu_countries
    temp_data = []
    # for data in data_list:
    #     hscode_data = tmp_arr.get(data['m2bProductId'])
    #     if not hscode_data:
    #         continue
    #     if hscode_data[2] != data['compId']:
    #         continue
    #     spuId = hscode_data[0]
    #     m2bProductId = hscode_data[1]
    #     compId = hscode_data[2]
        
    #     hscode_temp = {}
    #     if len(str(hscode_data[4])):
    #         if str(hscode_data[4]) == 'none':
    #             pass
    #         else:
    #             hscode = eval(hscode_data[4])
    #             if type(hscode) is dict:
    #                 hscode_temp = hscode
    #             else:
    #                 hscode_temp['USA'] = str(hscode_data[4])

    #     salesMarkets = hscode_data[3]
    #     if salesMarkets:
    #         salesMarkets = salesMarkets.split(',')
    #         if data.has_key('euHSCode'):
    #             for market in salesMarkets:
    #                 if market in eu_countries:
    #                     hscode_temp[str(market)+''] = str(data['euHSCode'])+''

    for m2bProductId, hscode_data in tmp_arr.iteritems():
        # print hscode_data
        data = data_map.get(m2bProductId)
        compId = hscode_data[2]
        spuId = hscode_data[0]
        hscode_temp = {}
        if len(str(hscode_data[4])):
            if str(hscode_data[4]) == 'none':
                pass
            else:
                hscode = eval(hscode_data[4])
                if type(hscode) is dict:
                    hscode_temp = hscode
                else:
                    hscode_temp['USA'] = str(hscode_data[4])

        salesMarkets = hscode_data[3]
        if data:
            if salesMarkets:
                salesMarkets = salesMarkets.split(',')
                if data.has_key('euHSCode'):
                    for market in salesMarkets:
                        if market in eu_countries:
                            hscode_temp[str(market)+''] = str(data['euHSCode'])+''
        if data:
            hscode_temp['CHN'] = str(data['chinaHSCode'])
        item = []
        item.append(str(hscode_temp))
        item.append(str(m2bProductId))
        item.append(str(compId))
        item.append(str(spuId))
        temp_data.append(item)
        
    sql="""
        UPDATE `erp$pro$product` SET `hs_code` = %s WHERE `product_id` = (SELECT pps.`product_id` FROM `erp$pro$product_sku` pps WHERE pps.`m2b_prod_id` = %s AND pps.`comp_id` = %s AND pps.`product_id` = %s)
        """
    print "flush to mysql"
 #   curr.executemany(sql, temp_data)
    conn.commit()
    curr.close()
    conn.close()


def get_product_hscode():
    print "start...get_product_hscode"
    connection = get_mongo_conn()
    db = connection.snowball

    cursor = db.product_hscodes.find()
    
    prod_hscode_list = []
    counter = 0
    for prod in cursor:
        item = {}
        if not prod.has_key('compId'):
        	print 'compId is null item == %s' % item 
        	continue
        if not prod.has_key('productId'):
        	print 'productId is null item == %s' % item
        	continue
        if not prod.has_key('chinaHSCode'):
        	print 'chinaHSCode is null item == %s' % item
        	continue
        item['compId'] = prod['compId']
        item['m2bProductId'] = prod['productId']
        item['chinaHSCode'] = prod['chinaHSCode']
        if prod.has_key('usaHSCode'):
                if len(str(prod['usaHSCode'])):
        	    item['usaHSCode'] = prod['usaHSCode']
        if prod.has_key('euHSCode'):
                if len(str(prod['euHSCode'])):
        	    item['euHSCode'] = prod['euHSCode']

        prod_hscode_list.append(item)
        counter += 1
        # if counter % 1000 == 0:
        #     generate_hscode_from_mysql(prod_hscode_list)
        #     prod_hscode_list = []

    print counter
    generate_hscode_from_mysql(prod_hscode_list)
    connection.close()
    print "end...get_product_hscode"

#-------------------------------------------------------------------------------------------

def get_eu_countries():
    global eu_countries
    eu_countries.append("AUT")
    eu_countries.append("BEL")
    eu_countries.append("BGR")
    eu_countries.append("CZE")
    eu_countries.append("DNK")
    eu_countries.append("EST")
    eu_countries.append("FIN")
    eu_countries.append("FRA")
    eu_countries.append("DEU")
    eu_countries.append("GRC")
    eu_countries.append("HUN")
    eu_countries.append("ITA")
    eu_countries.append("LVA")
    eu_countries.append("LIE")
    eu_countries.append("LTU")
    eu_countries.append("LUX")
    eu_countries.append("MCO")
    eu_countries.append("NLD")
    eu_countries.append("NOR")
    eu_countries.append("POL")
    eu_countries.append("PRT")
    eu_countries.append("ROM")
    eu_countries.append("SVK")
    eu_countries.append("SVN")
    eu_countries.append("ESP")
    eu_countries.append("SWE")
    eu_countries.append("GBR")


if __name__ == '__main__':
    print "begin..."
    eu_countries = []
    get_eu_countries()
    print "get product hscode from mongodb"
    get_product_hscode()
