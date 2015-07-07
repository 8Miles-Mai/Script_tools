#!/usr/local/bin/python

import json
import sys
from datetime import *
from gm_common import *


def flush_all_promotion_product_to_db():
    log("flushing all promotion product status to db...")
    data=[]
    total=0
    for item in product_counter :
         _due_date='%04d%02d%02d'%(item['promotionContract']['dueDate']['year']+1900,item['promotionContract']['dueDate']['month'],item['promotionContract']['dueDate']['date'])

         promotion_time = int(_due_date)
         now_time = int(datetime.now().strftime("%Y%m%d"))

         #init all promotion product status into seller$product_tag
         if promotion_time<now_time :
             for product_ids in item['entities'] :
                 data.append(product_ids['entityId'])
                 total=total+1


    tag_type=PRODUCT_TAG.PROMOTION
    save_promotion_product_status_to_db(tag_type=tag_type, data=data)

    log("update total " + str(total) + " records ")
    return True


def flush_expire_promotion_product_to_db():
    log("flushing expire promotion product status to db...")
    
    data=[]
    total=0
    for item in product_counter :
         _due_date='%04d%02d%02d'%(item['promotionContract']['dueDate']['year']+1900,item['promotionContract']['dueDate']['month'],item['promotionContract']['dueDate']['date'])

         promotion_time = int(_due_date)
         now_time = int(datetime.now().strftime("%Y%m%d"))

#         log("promotion_time"+str(promotion_time)+", now_time:"+str(now_time))
         if promotion_time>now_time :
             for product_ids in item['entities'] :
                 data.append(product_ids['entityId'])
                 total=total+1

    tag_type=PRODUCT_TAG.PROMOTION
    delete_promotion_product_status_to_db(tag_type=tag_type, data=data)

    log("update total " + str(total) + " records ")
    return True



if __name__ == "__main__":

    database_name="promotions"
    collection_name="promotions"
    log("get product tag status from MongoDB by database:" + database_name + " and collection: "+collection_name)
    mcl = get_mongodb_collection(database_name, MDB_USER, MDB_PASSWORD)
    product_counter = mcl.promotions.find({'offlineType':0,'entities.entityId':{'$exists':'true'}},{'entities.entityId':1,'_id':0,'promotionContract.dueDate':1})

    # init all promotion product status into seller$product_tag
#    flush_all_promotion_product_to_db()

    # delete expire promotion product status from seller$product_tag
    flush_expire_promotion_product_to_db()
