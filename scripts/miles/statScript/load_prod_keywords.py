#!/usr/local/bin/python

from gm_common import *
import json

def flush_to_db():
    log("flushing to stat db...")
    # TO_DO get time by parameter
    data=[]
    total=0
    for key in exp_cnt:
        cnt = exp_cnt[key]
        for comp_id in cnt:
            item = effect_log()
            item.comp_id = comp_id
            item.counter = cnt[comp_id]
            if cdict.has_key(item.comp_id):
                item.ind_group_id = cdict[item.comp_id]
                item.entity_source = STAT_TYPE.ENT_SRC_PRD
                item.entity_id = 111111
                data.append(item)
                total=total+1

    year_id=get_curr_year_no()
    week_id=get_curr_week_no()
    stat_date=key
    stat_type=STAT_TYPE.DISPLAY_CNT
    log("year_id = " + str(year_id) + " week_id = " + str(week_id) + " stat_date = " + str(stat_date) + " stat_type = " + str(stat_type) + " all")
    load_to_client_effect_table(year_id=year_id, week_id=week_id, stat_date=stat_date, stat_type=stat_type, data=data)
    log("insert total " + str(total) + " records")

    return True


#----------------------------------------------------------------------------------

url = "mongodb://192.168.23.248:27017/gm_applog"
user_name = "logger_wr"
password = "ayu46m9-9mwv86si"

def get_product_daily_exp_cnt():

    connection = pymongo.MongoClient(host=url, safe=True, read_preference=pymongo.ReadPreference.SECONDARY)
    #connection = pymongo.MongoClient(host=url, safe=True)
    connection.gm_applog.authenticate(user_name, password)
    db = connection.gm_applog

    query = {
		"date": "2014-09-26", 
		"requestUrl": "/gmvo/mygm/product/prod/edit.gm", 
		"hour":"21"
	    };
    global exp_cnt
    cursor = db.vo_visit.find(query,{"compId":1,"entityID":1, "responseBody":1})
    log(" deal docs ")
    count = 0
    productIds = []

    for doc in cursor:
        bodyJson = None
        productID = str(doc["entityID"])
        compId = str(doc["compId"])
        responseBody = doc["responseBody"]
        json_obj = json.loads(responseBody)
        #bodyJson = json.dumps(json_obj, sort_keys=True, indent=4)
        otherKeywords = json_obj['product']['otherKeywords']
        
        if productID == "0":
            continue;

        if compId == "0":
            continue;

        if productID in productIds:
            continue;

        productIds.append(productID)
        if len(otherKeywords):
            sql=" INSERT INTO seller$prod_keyword spk SELECT sq_seller$prod_keyword.NEXTVAL, " + productID + ", " + compId +", t.kw, 0, SYSDATE, 0, SYSDATE, 0 FROM (";
            index = 0;
            for kww in otherKeywords:
                kw = kww.replace('\'','')

                if index == 0:
                    sql += "            SELECT \'" + kw + "\' kw FROM DUAL ";
                else:
                    sql += "            UNION ALL SELECT \'" + kw + "\' kw FROM DUAL ";

                index += 1

            sql +=  ") t WHERE     1 = 1 AND NOT EXISTS (SELECT NULL FROM seller$prod_keyword sp WHERE sp.product_id = " + productID + " and sp.weight <> 1 ); ";

            print sql

        count += 1

    log(count)
    connection.close()


#-------------------------------------------------------------------------------------------


if __name__ == '__main__':
    log(" restore cache data")
    sdict,cdict,udict=get_supplier_list()

    # global variables
    exp_cnt = {}
    log(" start get product daily exp cnt ")
    get_product_daily_exp_cnt()

    log(" flush to db ")
    #flush_to_db()
