#!/usr/local/bin/python

from gm_common import *


def flush_to_db():
    log("flushing to stat db...")
    data = []
    total = 0
    for key in click_cnt:
        cnt = click_cnt[key]
        for comp_id in cnt:
            item = effect_log()
            item.comp_id = comp_id
            item.counter = cnt[comp_id]
            if cdict.has_key(item.comp_id):
                item.ind_group_id = cdict[item.comp_id]
                item.entity_source = STAT_TYPE.CLICK_CNT
                item.entity_id = 111111
                data.append(item)
                total = total + 1

        year_id = get_curr_year_no()
        week_id = get_curr_week_no()
        stat_date = key
        stat_type = STAT_TYPE.CLICK_CNT
        log("year_id = " + str(year_id) + " week_id = " + str(week_id) + " stat_date = " + str(stat_date) + " stat_type = " + str(stat_type) + " all")
        load_to_client_effect_table(year_id=year_id, week_id=week_id, stat_date=stat_date, stat_type=stat_type, data=data)
        log("insert total " + str(total) + " records")

    return True

#------------------------------------------------------------------------------------------------------------

url = "mongodb://192.168.86.180:27017/tracker_db"
user_name = "tracker_ro"
password = "reader"

#url = "mongodb://172.16.0.212:27017/tracker_db"
#user_name = "reader"
#password = "rr1ee2aa3dd4"


def get_product_daily_clk_cnt():
    
    connection = pymongo.MongoClient(host=url, safe=True, read_preference=pymongo.ReadPreference.SECONDARY)

    connection.admin.authenticate(user_name, password)
    db = connection.tracker_db

    query = {"data_queue.evt": "EXP", "$or": [
            {"data_queue.MP": {"$exists": "true"}}
            ],
                    "date": {"$gt": str(get_curr_date()), "$lt": str(get_tomorrow_date())}
            };

    global click_cnt
    cursor = db.logs.find(query,{"date":1, "data_queue":1})
    log(" deal docs  ")
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
            if not (objType == "MP"):
                continue

            date = doc["date"][:10]
            if click_cnt.get(date, '') == '':
                click_cnt.setdefault(date, {})

            date_dict = click_cnt[date]
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
    return True


#------------------------------------------------------------


if __name__ == '__main__':
    log(" restore cache data")
    sdict,cdict,udict=get_supplier_list()

    # global variables
    click_cnt = {}
    log(" start get product daily clk cnt ")
    get_product_daily_clk_cnt()
    
    log(" flush to db ")
    flush_to_db()
