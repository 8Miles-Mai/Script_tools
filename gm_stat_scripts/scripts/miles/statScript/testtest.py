#!/usr/local/bin/python

import re
from gm_common import *


def check_comp_login():
    global login_counter,comp_id
    curr_date = get_curr_date()
    loginSQL="""
                select comp_id compId, count(0) num 
                  from """ + MYSQL_DB + """.wla$login_logs 
                 where login_time >= '""" + str(get_curr_date()) + """' 
                   and login_time < '""" + str(get_tomorrow_date()) + """' 
                 group by comp_id
            """

    loginConn=get_mysql_conn()
    loginCurr = loginConn.cursor()
    
    log(loginSQL)
    n = loginCurr.execute(loginSQL)

    #res = loginCurr.fetchall()    
    
    #log(res)
    
    for loginRs in loginCurr.fetchall():
        comp_id=str(loginRs[0])
        countNum=str(loginRs[1])
        login_counter[comp_id]=countNum
            

    loginConn.close()

#    pattern="compId-([\d]*)"
#    m=re.search(pattern,line)
#    if m :
#        comp_id=m.group(1)
#        if not login_counter.has_key(comp_id):
#            login_counter[comp_id]=1



#2012-07-06 1645, amended by jie.zou, for task 
def check_product_update():
    global update_product_counter
    pattern="gmvo/mygm/product/product/saveForEdit.gm"
    m=re.search(pattern,line)
    if m:
        if update_product_counter.has_key(comp_id):
            update_product_counter[comp_id]=update_product_counter[comp_id]+1
        else:
            update_product_counter[comp_id]=1

    pattern="gmvo/mygm/product/prod/saveForEdit.gm"
    m=re.search(pattern,line)
    if m:
        if update_product_counter.has_key(comp_id):
            update_product_counter[comp_id]=update_product_counter[comp_id]+1
        else:
            update_product_counter[comp_id]=1
    return True



#2012-07-06 1645, amended by jie.zou, for task 
def check_product_create():
    global create_product_counter
    pattern1="gmvo/mygm/product/product/saveForAdd.gm"
    pattern2="gmvo/mygm/product/prod/saveForAdd.gm"
    pattern3="gmvo/mygm/product/product/saveForPeAdd.gm"
    pattern4="gmvo/mygm/product/prod/saveForPeAdd.gm"
    m1=re.search(pattern1,line)
    m2=re.search(pattern2,line)
    m3=re.search(pattern3,line)
    m4=re.search(pattern4,line)    

    if m1 or m2 or m3 or m4:
        if create_product_counter.has_key(comp_id):
            create_product_counter[comp_id]=create_product_counter[comp_id]+1
        else:
            create_product_counter[comp_id]=1
    return True



def flush_to_db_by_type(arr, stat_type):
    data=[]
    total=0
    for key in arr:
        if cdict.has_key(key):
            item = action_log()
            item.comp_id=key
            item.counter=arr[key]
            item.ind_group_id=cdict[key]
            data.append(item)
            total=total+1
    year_id=get_curr_year_no()
    week_id=get_curr_dfsdfsfdweek_no()
    stat_date=get_curr_date()
    log("stat_date = %s" % stat_date )
    action_type=stat_type
    log("stat_type = %s" % stat_type )
    load_to_client_action_table(year_id=year_id,
                                week_id=week_id,
                                stat_date=stat_date,
                                action_type=action_type,
                                data=data)
    log("insert total " + str(total) + " records ")



def flush_to_db():
    
    log("processing login counter ...")
    flush_to_db_by_type(login_counter,STAT_TYPE.LOGIN_CNT)

    log("processing create product counter ...")
    #flush_to_db_by_type(create_product_counter,STAT_TYPE.CREATE_PD_CNT)

    log("processing upadte product counter ...")
    #flush_to_db_by_type(update_product_counter,STAT_TYPE.UPDATE_PD_CNT)



if __name__=="__main__":
    """ The main pattern to process the raw nginx log """
       
    log("processing performance log")

    
    # define global holder
    login_counter={}
    update_product_counter={}
    create_product_counter={}
    
    # get cache data
    sdict,cdict,udict=get_supplier_list()    

    counter = 1
    while True:
        line = sys.stdin.readline()
    
        # print message ever 10000 lines    
        counter=counter + 1
        if counter % 10000 == 0 : 
            log("line %s" % counter)

        # 
        if not line :
            log("Total line:%s" % counter)
            break

        comp_id=0
        #check_comp_login()
        #check_product_update()
        #check_product_create()

        
    check_comp_login()
    #the end flush to db
    flush_to_db()
