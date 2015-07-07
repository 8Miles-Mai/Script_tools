#!/usr/local/bin/python

from gm_common import *


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

#url = "mongodb://192.168.86.180:27017/tracker_db"
#user_name = "tracker_ro"
#password = "reader"

#url = "mongodb://172.16.0.212:27017/tracker_db"
url = "mongodb://192.168.23.248:27017/tracker_db"
user_name = "reader"
password = "rr1ee2aa3dd4"

def get_product_daily_exp_cnt():

    connection = pymongo.MongoClient(host=url, safe=True, read_preference=pymongo.ReadPreference.SECONDARY)
    #connection = pymongo.MongoClient(host=url, safe=True)
    connection.admin.authenticate(user_name, password)
    db = connection.tracker_db

    query = {"data_queue.evt": "EXP", "$or": [
            {"data_queue.LP": {"$exists": "true"}},
            {"data_queue.GYLP": {"$exists": "true"}},
            {"data_queue.SRP": {"$exists": "true"}},
            {"data_queue.SP": {"$exists": "true"}},
            {"data_queue.CLP": {"$exists": "true"}},
	    {"data_queue.RP": {"$exists": "true"}},
	    {"data_queue.MEP": {"$exists": "true"}},
	    {"data_queue.HP": {"$exists": "true"}},
	    {"data_queue.OTP": {"$exists": "true"}},
            {"data_queue.NP": {"$exists": "true"}}
            ],
                    "date": {"$gt": str(get_curr_date()), "$lt": str(get_tomorrow_date())}
            };
    #query = {}
    global exp_cnt
    cursor = db.logs.find(query,{"date":1, "data_queue":1})
    #cursor = db.logs.find(query).limit(10)
    log(" deal docs ")
    #for doc in cursor:
    #    print(doc["_id"])



    
    for doc in cursor:
        data_queue = doc["data_queue"]
        for d in data_queue:
            isExp = False
            objType = ""
            for key in d:
                if key == "evt":
                    if d[key] == "EXP":
                        isExp = True
                else:
                    objType = key
            if not isExp:
                continue
            if  not (objType in ["LP","GYLP","SRP","SP","CLP","NP","RP","MEP","HP","OTP"]):
                continue

            date = doc["date"][:10]
            if exp_cnt.get(date, '') == '':
                exp_cnt.setdefault(date, {})

            date_dict = exp_cnt[date]
            obj_data = d[objType]
            for obj in obj_data:
                sid = obj.get("sid", '')
                if sid == '':
                    break
                
                if date_dict.get(sid, '') == '':
                    date_dict.setdefault(sid, 1)
                else:
                    date_dict[sid] += 1
    
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
