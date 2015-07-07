#!/usr/local/bin/python

import MySQLdb
import cx_Oracle
import pymongo
import os
import json
import urllib2
import urllib
from datetime import *
from pysqlite2 import dbapi2 as sqlite
import sys



###########################
# All Config From ENV 
###########################

#---------------------------
# 1. Define ORACLE Constants
#---------------------------
ORACLE_SERVICE=os.environ["ORACLE_SERVICE"]
ORACLE_SID    =os.environ["ORACLE_SID"]
ORACLE_PWD    =os.environ["ORACLE_PASSWORD"]
ORACLE_USER   =os.environ["ORACLE_USER"]


#---------------------------
# 2. Define MySQL Constants
#---------------------------
MYSQL_SERVER  =os.environ["MYSQL_SERVER"]
MYSQL_USER    =os.environ["MYSQL_USER"]
MYSQL_PASSWORD=os.environ["MYSQL_PASSWORD"]
MYSQL_DB      =os.environ["MYSQL_DB"]


#---------------------------
# 3. Define MongoDB Constants
#---------------------------
MDB_SERVER    = os.environ["MDB_SERVER"]
MDB_PORT      = os.environ["MDB_PORT"]
MDB_USER      = os.environ["MDB_USER"]
MDB_PASSWORD  = os.environ["MDB_PASSWORD"]


#---------------------------
# 4. Define SOLR Constants
#---------------------------
SOLR_SRV      =os.environ["SOLR_SRV"]


#---------------------------
# 5. Define LOG PATH Constants
#---------------------------
DATA_DIR      =os.environ["DATA_DIR"]
ERROR_HINT    = """"""


#---------------------------
# 6. Define STAT_TYPE Constants 
#---------------------------
class STAT_TYPE:
    LOGIN_CNT=1
    CREATE_PD_CNT=2
    UPDATE_PD_CNT=3
    REPLY_CNT=4
    DISPLAY_CNT=5
    CLICK_CNT=6
    INQ_CNT=7
    BLY_CNT=8
    INQ_FOR_CMP='GI'
    INQ_FOR_PRD='PI'
    ENT_SRC_CMP=2
    ENT_SRC_PRD=53
    ENT_SRC_LC=21


#---------------------------
# 7. Define ACTION_LOG Constants 
#---------------------------
class action_log:
    comp_id=0
    counter=0
    ind_group_id=0


#---------------------------
# 8. Define EFFECT_LOG Constants 
#---------------------------
class effect_log:
    comp_id=0
    counter=0
    ind_group_id=0
    entity_source=0
    entity_id=0


#---------------------------
# 9. Define AGGS_LOG Constants 
#---------------------------
class aggs_log:
    ind_group_id=0
    stat_type=0
    max_count=0
    min_count=0
    avg_count_wla=0
    avg_count_all=0 


#---------------------------
# 10. Define product_tag Constants 
#---------------------------
class PRODUCT_TAG:
    NEW=1
    SELECTED=2
    KEYWORD=3
    PROMOTION=4


###########################
# Log Helper 
###########################
#---------------------------
# 1. write log 
#---------------------------
def log(str):
    print "LOG %s : %s" % (get_now_str(),str)  


def info(str):
    print "INF %s : %s" % (get_now_str(),str)


def error(str):
    print "ERR %s : %s" % (get_now_str(),str)



###########################
# Time Helper 
###########################
#---------------------------
# 1. current time 
#---------------------------
def get_now_str():
    now=datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")


#---------------------------
# 2. current date 
#---------------------------
def get_date_str():
    now=datetime.now()
    return now.strftime("%Y-%m-%d")


#---------------------------
# 3. current date (ENV config first)
#---------------------------
def get_curr_date():
    if os.environ.has_key("curr_date") :
        return os.environ["curr_date"]
    else :
        return get_date_str()


#---------------------------
# 4. current week 
#---------------------------
def get_curr_week_no():
    #return datetime.strptime(get_curr_date(),"%Y-%m-%d").isocalendar()[1]
    #return int(datetime.strptime(get_curr_date(),"%Y-%m-%d").strftime("%U"))
    return int(datetime.strptime(get_curr_date(),"%Y-%m-%d").strftime("%U"))+1


#---------------------------
# 5. current year 
#---------------------------
def get_curr_year_no():
    return datetime.strptime(get_curr_date(),"%Y-%m-%d").year


#---------------------------
# 6. tomorrow date (ENV config first)
#---------------------------
def get_tomorrow_date():
    return datetime.strptime(get_curr_date(), "%Y-%m-%d") + timedelta(1)


###########################
# DB Helper 
###########################

#---------------------------
# 1. Get Oracle Connection 
#---------------------------
def get_oracle_conn():
    try:
#        log("oracle connection info, ORACLE_USER:"+ORACLE_USER+", ORACLE_PWD:"+ORACLE_PWD+", ORACLE_SID:"+ORACLE_SID)
#        oracle_conn = cx_Oracle.connect(user=ORACLE_USER, password=ORACLE_PWD, dsn=ORACLE_SID)
        oracle_conn = cx_Oracle.connect(ORACLE_USER,ORACLE_PWD,ORACLE_SERVICE)
        return oracle_conn
    except Exception,e:
        ERROR_HINT = " [ get Oracle connection failed ] ORACLE_USER:"+ORACLE_USER+", ORACLE_SID:"+ORACLE_SID
        log(ERROR_HINT)
        log(e)
        return None


#---------------------------
# 2. Get MySQL Connection 
#---------------------------
def get_mysql_conn():
    try:
        mysql_conn = MySQLdb.connect(user=MYSQL_USER,
                  charset='utf8',
                  host=MYSQL_SERVER,
                  passwd=MYSQL_PASSWORD,
                  db=MYSQL_DB)
        return mysql_conn
    except:
        ERROR_HINT = " [ get mysql connection failed ] MYSQL_USER:"+MYSQL_USER+", MYSQL_SERVER:"+MYSQL_SERVER+", MYSQL_DB:"+MYSQL_DB
        log(ERROR_HINT)
        return None


#---------------------------
# 3. Get MongoDB Collection 
#---------------------------
def get_mongodb_collection(database_name, user_name, user_ps):
#    log(" opening MongoDB connection ...")
    try :
#        mongodb_conn = pymongo.Connection(MDB_SERVER,MDB_PORT)
        mongodb_conn = pymongo.Connection("192.168.86.51",27017)
        db = mongodb_conn.promotions
        db.authenticate('app_soa','app_soa')
    except :
        ERROR_HINT = " [ get MongoDB connection failed ] MongoDB connect error. host:"+MDB_SERVER+", port:"+MDB_PORT+", user:"+user_name;
        log(ERROR_HINT)
        return None
    return  db


#---------------------------
# 4. Get SQLite Connection 
#---------------------------
def get_sqlite_conn(file):
    return sqlite.connect(file)



###########################
# SOLR Helper 
###########################

#---------------------------
# 1. Product-Seller Map  (data: sdict[product_id] = comp_id )
#---------------------------
def get_product_comp_id_mapping():
    ckpt_file=DATA_DIR+"/CKPT_"+get_date_str()+"_sdict.json"

    if not is_file_exists(ckpt_file):
        url="http://" + SOLR_SRV + "/solr/product/select"
        params={
#            "version":"2.2",
            "q":"status:7 compStatus:7",
            "start":"0",
            "rows":"9000000",
            "fl":"compId,productId",
#            "qt":"standard",
            "indent":"on",
            "wt":"json"
        }
        data=urllib.urlencode(params)
        url=url+"?"+data
        print url
        log("Reading supplier dict from " + url)
        jsonstr=urllib2.urlopen(url).read()
        write_file(ckpt_file,jsonstr)
    else:
        jsonstr=read_file(ckpt_file)

    resp = json.JSONDecoder().decode(jsonstr)
    sdict = {}
    log("Packing dict")
    for product in resp["response"]["docs"]:
        product_id = product["productId"]
        comp_id = product["compId"]
        sdict[product_id]= comp_id
    return sdict


#---------------------------
# 2. Seller-Group Map (data: cdict[comp_id] = ind_id )
#---------------------------
def get_comp_ind_group_id_mapping():
    ckpt_file=DATA_DIR+"/CKPT_"+get_date_str()+"_cdict.json"
    cdictTemp={}
    cdict={}
    if not is_file_exists(ckpt_file):
        sql="""
            select CLIENT_ID,IND_GROUP_ID from vw_seller_igroup 
        """
        conn = get_oracle_conn()
        cur = conn.cursor()
        for rs in cur.execute(sql):
            cdictTemp[rs[0]]=rs[1]
        cur.close()
        conn.close()
        jsonstr = json.dumps(cdictTemp)
        write_file(ckpt_file,jsonstr)
        cdict = json.JSONDecoder().decode(jsonstr)    
    else:
        jsonstr=read_file(ckpt_file)    
        cdict = json.JSONDecoder().decode(jsonstr)    
    return cdict


#---------------------------
# 3. GMCName-Seller Map (data: udict[gmcname.url] = comp_id) 
#---------------------------
def get_gmcname_comp_id_mapping():
    ckpt_file=DATA_DIR+"/CKPT_"+get_date_str()+"_udict.json"
    if not is_file_exists(ckpt_file):
        url = "http://" + SOLR_SRV + "/solr/supplier/select"
        params={
#                "version":"2.2",
                "q":"status:7",
                "start":"0",
                "rows":"90000",
                "fl":"compId,gmcName",
#                "qt":"standard",
                "wt":"json"
        }
        data=urllib.urlencode(params)
        url=url+"?"+data
        log("Getting supplier name dict from " + url)
        jsonstr=urllib2.urlopen(url).read()
        write_file(ckpt_file,jsonstr)
    else:
        jsonstr=read_file(ckpt_file)

    resp = json.JSONDecoder().decode(jsonstr)
    udict = {}
    log("Packing dict")
    for product in resp["response"]["docs"]:
        try:
            comp_id = product["compId"]
            gmc_name = product["gmcName"]
            udict[gmc_name] = comp_id
        except:
            continue
    return udict


#---------------------------
# 4. Get UserId-UserName Map 
#---------------------------


#---------------------------
# 5. Get All Dict Files 
#---------------------------
def get_supplier_list():
    return [get_product_comp_id_mapping(),
        get_comp_ind_group_id_mapping(),
        get_gmcname_comp_id_mapping()
        ]



###########################
# Oracle Helper 
###########################
#---------------------------
# 1. get seller BL view times for calcute 
#---------------------------



#---------------------------
# 2. save seller BL view times for calcute 
#---------------------------



#---------------------------
# 3. update BL status as online or offline by the data 
#---------------------------
def update_bl_status_to_db():
    conn = get_oracle_conn()
    curr = conn.cursor()

    # online BL (if buyer$needs.status=13 and not expire, modify status as online, and cant insert record into delta table ) 
    onlineSql="""
               update buyer$need bns
                  set bns.status=7
                      ,LAST_UPDATE_TIME=sysdate
                      ,LAST_UPDATE_BY=0
                where exists
                     (select null
                        from buyer$need bnds
                       where bnds.status=13
                         and bnds.expiry_date>sysdate
                         and to_char(sysdate-1,'D')=1
                         and bnds.need_id=bns.need_id)
               """
    curr.execute(onlineSql)

    conn.commit()


#---------------------------
# 4. save all promotion product status to oracle 
#---------------------------
def save_promotion_product_status_to_db(tag_type, data):

    conn = get_oracle_conn()
    curr = conn.cursor()

    # delete data
    delSql="""delete from seller$prod_tag spt where tag_id="""+str(tag_type)
    curr.execute(delSql)
    conn.commit()

    # insert data
    ins_data=[]
    counter=1

    for product_id in data:
        try :
            counter=counter+1
            insSql=""" insert into seller$prod_tag(prod_tag_id,product_id,tag_id,create_by,create_time,last_update_by,last_update_time) (select sq_seller$prod_tag.nextval, """+str(product_id)+""", """+str(tag_type)+""", 0, sysdate, 0, sysdate from seller$product spd where spd.product_id="""+str(product_id)+""" and not exists (select null from seller$prod_tag where product_id=spd.product_id and tag_id="""+str(tag_type)+""")) """
            curr.execute(insSql)

        except:
            log("insert seller$prod_tags error")
            continue

    conn.commit()


#---------------------------
# 5. delete expire promotion product status from oracle
#---------------------------
def delete_promotion_product_status_to_db(tag_type, data):

    conn = get_oracle_conn()
    curr = conn.cursor()

    # delete data
    counter=1

    for product_id in data:
        try :
            counter=counter+1
            delSql="""delete from seller$prod_tag spt where product_id="""+str(product_id)+""" and tag_id="""+str(tag_type)
#            log("delSql:"+delSql)
            curr.execute(delSql)
        except:
            log("insert seller$prod_tags error")
            continue

    conn.commit()



###########################
# MongoDB Helper 
###########################

#---------------------------
# 1. get data from collection (get data as array, can be read data by codes like 'for i in xx: \n  print i')
#---------------------------
def load_data_from_collection(database_name, collection_name, user_name, user_ps, query_json, where_json):
    collection = get_mongodb_collection(database_name, user_name, user_ps)
    res = []
    data = collection.collection_name.find(where_json, query_json)
    for i in data:
        res.append(str(i))
    return res


###########################
# MySQL Helper 
###########################

#---------------------------
# 1. save data into action table 
#---------------------------
def load_to_client_action_table(year_id,week_id,stat_date,action_type,data):

    conn = get_mysql_conn()
    curr = conn.cursor()
    # initial table
    sql="""
        delete from """ + MYSQL_DB + """.wla$client_action_daily 
                where year_id=%s and week_id=%s and stat_date=%s and action_type=%s 
        """
    curr.execute(sql,(year_id,week_id,stat_date,action_type))

    # insert table
    sql="""
        insert into """ + MYSQL_DB + """.wla$client_action_daily
        (comp_id,count,ind_group_id,year_id,week_id,stat_date,action_type,create_by,create_time,last_update_by,last_update_time) 
        values(%s,%s,%s,%s,%s,%s,%s,0,%s,0,%s)
        """
    tmp_data=[]
    counter=1
    for item in data:
        try :
            counter=counter+1
            tmp_arr=[]
            tmp_arr.append(item.comp_id)
            tmp_arr.append(item.counter)
            tmp_arr.append(item.ind_group_id)
            tmp_arr.append(year_id)
            tmp_arr.append(week_id)
            tmp_arr.append(stat_date)
            tmp_arr.append(action_type)
            # we explictly declare the datetime in sql, to avoid mysql binary replication warning
            tmp_arr.append(get_now_str())
            tmp_arr.append(get_now_str())
            tmp_data.append(tuple(tmp_arr))    

            if counter % 1000 == 0 :
                curr.executemany(sql,tmp_data)    
                tmp_data=[]
                conn.commit()
        except:
            log("insert wla$client_action_daily error, comp_id:"+item.comp_id)
            continue

    curr.executemany(sql,tmp_data)
    conn.commit()


#---------------------------
# 2. save data into effect table 
#---------------------------
def load_to_client_effect_table(year_id,week_id,stat_date,stat_type,data):

# [1. get mysql connection]
    conn = get_mysql_conn()
    curr = conn.cursor()

#[2. delete data]
    sql="""delete from """ + MYSQL_DB + """.wla$client_effect_daily where year_id=%s and week_id=%s and stat_date=%s and stat_type=%s """
    curr.execute(sql,(year_id,week_id,stat_date,stat_type))
    
#[3. insert data]
    sql=""" insert into """ + MYSQL_DB + """.wla$client_effect_daily (comp_id,ind_group_id,entity_source,entity_id,year_id,week_id,stat_date,count,stat_type,create_by,create_time,last_update_by,last_update_time) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,0,%s,0,%s) """

    tmp_data=[]
    counter=1 

    for item in data:
        try :
            counter=counter+1
            tmp_arr=[]
            tmp_arr.append(item.comp_id)
            tmp_arr.append(item.ind_group_id)
            tmp_arr.append(item.entity_source)
            tmp_arr.append(item.entity_id)
            tmp_arr.append(year_id)
            tmp_arr.append(week_id)
            tmp_arr.append(stat_date)
            tmp_arr.append(item.counter)
            tmp_arr.append(stat_type)
            # we explictly declare the datetime in sql, to avoid mysql binary replication warning
            tmp_arr.append(get_now_str())
            tmp_arr.append(get_now_str())
            tmp_data.append(tuple(tmp_arr))

            if counter % 1000 == 0 :
                curr.executemany(sql,tmp_data)    
                tmp_data=[]
                conn.commit()
        except :
            log("insert wla$client_effect_daily error, comp_id:"+item.comp_id)
            continue

    curr.executemany(sql,tmp_data)
    conn.commit()


#---------------------------
# 3. save aggs table 
#---------------------------
def load_to_client_aggs_table(year_id,week_id,stat_date,action_data,effect_data):

#[1. get mysql connection]
    conn = get_mysql_conn()
    curr = conn.cursor()

#[2. delete data]
    sql=""" delete from """ + MYSQL_DB + """.wla$client_aggs  where year_id=%s and week_id=%s """
    curr.execute(sql,(year_id,week_id))

#[3. insert data from action and effect table]
    sql=""" insert into """ + MYSQL_DB + """.wla$client_aggs (year_id,week_id,ind_group_id,stat_type,stat_date,max_count,min_count,avg_count_all,avg_count_wla,create_by,create_time,last_update_by,last_update_time)  values(%s,%s,%s,%s,%s,%s,%s,%s,%s,0,%s,0,%s) """
    
    tmp_data=[]
    counter=1

    for item in action_data:
        try :
            counter=counter+1
            tmp_arr=[]
            tmp_arr.append(year_id)
            tmp_arr.append(week_id)
            tmp_arr.append(item.ind_group_id)
            tmp_arr.append(item.stat_type)
            tmp_arr.append(stat_date)
            tmp_arr.append(item.max_count)
            tmp_arr.append(item.min_count)
            tmp_arr.append(item.avg_count_all)
            tmp_arr.append(item.avg_count_wla)
            # we explictly declare the datetime in sql, to avoid mysql binary replication warning
            tmp_arr.append(get_now_str())
            tmp_arr.append(get_now_str())
            tmp_data.append(tuple(tmp_arr))    
        
            if counter % 1000 == 0 :
                curr.executemany(sql,tmp_data)    
                tmp_data=[]
                conn.commit()
        except :
            log("insert wla$client_aggs error")
    curr.executemany(sql,tmp_data)    
    conn.commit()

    tmp_data=[]
    counter=1

    for item in effect_data:
        counter=counter+1
        tmp_arr=[]
        tmp_arr.append(year_id)
        tmp_arr.append(week_id)
        tmp_arr.append(item.ind_group_id)
        tmp_arr.append(item.stat_type)
        tmp_arr.append(stat_date)
        tmp_arr.append(item.max_count)
        tmp_arr.append(item.min_count)
        tmp_arr.append(item.avg_count_all)
        tmp_arr.append(item.avg_count_wla)
        # we explictly declare the datetime in sql, to avoid mysql binary replication warning
        tmp_arr.append(get_now_str())
        tmp_arr.append(get_now_str())
        tmp_data.append(tuple(tmp_arr))    
        
        if counter % 1000 == 0 :
            curr.executemany(sql,tmp_data)    
            tmp_data=[]
            conn.commit()
    curr.executemany(sql,tmp_data)    
    conn.commit()



###########################
# File Helper 
###########################

#---------------------------
# 1. Write Log File 
#---------------------------
def write_file(fileName,content):
    try:
        fileHandler = open(fileName,"a")
        fileHandler.write(content)
        fileHandler.close()
    except:
        ERROR_HINT = " [ write file failed ] fileName:"+fileName
        log(ERROR_HINT)


#---------------------------
# 2. Find Log File Exists 
#---------------------------
def is_file_exists(fileName):
    return os.path.exists(fileName)


#---------------------------
# 3. Read File (for dict map) 
#---------------------------
def read_file(fileName):
    try:
        fileHandler = open(fileName,"r")
        str=fileHandler.read()
        fileHandler.close()
        return str
    except:
        ERROR_HINT = " [ read file failed ] fileName:"+fileName
        log(ERROR_HINT)



###########################
# Email Helper 
###########################

#---------------------------
# 1. Send Mail By Python 
#---------------------------
def send_mail(script_code,log_file):
    jsonstr=read_file("email.cfg")
    email_cfg=json.JSONDecoder().decode(jsonstr)
    import smtplib
    import mimetypes
    #from email.MIMEMultipart import MIMEMultipart
    #from email.MIMEBase import MIMEBase
    #from email.MIMEText import MIMEText
    #from email.MIMEAudio import MIMEAudio
    #from email.MIMEImage import MIMEImage
    from email.mime.multipart import MIMEMultipart
    from email.mime.base import MIMEBase
    from email.mime.text import MIMEText
    from email.mime.audio import MIMEAudio
    from email.mime.image import MIMEImage
    from email.Encoders import encode_base64
    from email.utils import COMMASPACE, formatdate
    msg_root = MIMEMultipart('related')
    msg_root['From'] = os.environ["MAIL_FROM"]
    smtp_server = os.environ["SMTP_SERVER"]
    smtp_username = os.environ["SMTP_USERNAME"]
    smtp_password = os.environ["SMTP_PASSWORD"]
    mail_from = os.environ["MAIL_FROM"]
    mail_to_str = email_cfg["recipions"][script_code]
    mail_to = mail_to_str.split(";")
    msg_root['To'] = mail_to
    msg_root['Subject'] = " Batch job [%s] is done" % script_code
    html_mail_body=read_file(log_file)
    msg = MIMEMultipart('alternative')
    msg['Subject'] = " Batch job [%s] is done" % script_code
    msg.attach(MIMEText(html_mail_body,'plain','utf-8'))
    msg_root.attach(msg)
    mailServer = smtplib.SMTP(smtp_server, 25)
    mailServer.ehlo()
    mailServer.ehlo()
    mailServer.login(smtp_username, smtp_password)
    mailServer.sendmail(mail_from, mail_to, msg.as_string())
    mailServer.close()
    log("email send to %s" % mail_to)
