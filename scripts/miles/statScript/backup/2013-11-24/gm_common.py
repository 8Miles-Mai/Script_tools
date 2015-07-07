#!/usr/local/bin/python

import MySQLdb
import cx_Oracle
import os
import json
import urllib2
import urllib
from datetime import *
from pysqlite2 import dbapi2 as sqlite
import sys

#******************************************************************* Global variables 

MYSQL_SERVER  =os.environ["MYSQL_SERVER"]
MYSQL_USER    =os.environ["MYSQL_USER"]
MYSQL_PASSWORD=os.environ["MYSQL_PASSWORD"]
MYSQL_DB      =os.environ["MYSQL_DB"]

ORACLE_SERVICE=os.environ["ORACLE_SERVICE"]
ORACLE_SID    =os.environ["ORACLE_SID"]
ORACLE_PWD    =os.environ["ORACLE_PASSWORD"]
ORACLE_USER   =os.environ["ORACLE_USER"]


SOLR_SRV      =os.environ["SOLR_SRV"]
DATA_DIR      =os.environ["DATA_DIR"]

ERROR_HINT    = """"""


#******************************************************************* log helper 

def log(str):
	print "LOG %s : %s" % (get_now_str(),str)  

def info(str):
	print "INF %s : %s" % (get_now_str(),str)

def error(str):
	print "ERR %s : %s" % (get_now_str(),str)

#******************************************************************* time helper 

def get_now_str():
	now=datetime.now()
	return now.strftime("%Y-%m-%d %H:%M:%S")

def get_date_str():
	now=datetime.now()
        return now.strftime("%Y-%m-%d")

def get_curr_week_no():
	#return datetime.strptime(get_curr_date(),"%Y-%m-%d").isocalendar()[1]
	#return int(datetime.strptime(get_curr_date(),"%Y-%m-%d").strftime("%U"))
	return int(datetime.strptime(get_curr_date(),"%Y-%m-%d").strftime("%U"))+1

def get_curr_year_no():
	return datetime.strptime(get_curr_date(),"%Y-%m-%d").isocalendar()[0]

def get_curr_date():
	if os.environ.has_key("curr_date") :
		return os.environ["curr_date"]
	else :
		return get_date_str()


#*******************************************************************  db helper 

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


def get_oracle_conn():
	try:
#		log("oracle connection info, ORACLE_USER:"+ORACLE_USER+", ORACLE_PWD:"+ORACLE_PWD+", ORACLE_SID:"+ORACLE_SID)
#		oracle_conn = cx_Oracle.connect(user=ORACLE_USER, password=ORACLE_PWD, dsn=ORACLE_SID)
		oracle_conn = cx_Oracle.connect(ORACLE_USER,ORACLE_PWD,ORACLE_SERVICE)
		return oracle_conn
        except:
		ERROR_HINT = " [ get Oracle connection failed ] ORACLE_USER:"+ORACLE_USER+", ORACLE_SID:"+ORACLE_SID
		log(ERROR_HINT)
		return None
		

def get_sqlite_conn(file):
	return sqlite.connect(file)


#*******************************************************************  file helper 

def write_file(fileName,content):
	try:
		fileHandler = open(fileName,"a")
        	fileHandler.write(content)
		fileHandler.close()
	except:
		ERROR_HINT = " [ write file failed ] fileName:"+fileName
		log(ERROR_HINT)
		


def is_file_exists(fileName):
	return os.path.exists(fileName)
	

def read_file(fileName):
	try:
		fileHandler = open(fileName,"r")
		str=fileHandler.read()
		fileHandler.close()
		return str
	except:
		ERROR_HINT = " [ read file failed ] fileName:"+fileName
		log(ERROR_HINT)


#*******************************************************************  email helper 

def send_mail(script_code,log_file):
	jsonstr=read_file("email.cfg")
	email_cfg=json.JSONDecoder().decode(jsonstr)
	import smtplib
	import mimetypes
	from email.MIMEMultipart import MIMEMultipart
	from email.MIMEBase import MIMEBase
	from email.MIMEText import MIMEText
	from email.MIMEAudio import MIMEAudio
	from email.MIMEImage import MIMEImage
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

#*******************************************************************  biz helper

class action_log:
	comp_id=0
	counter=0
	ind_group_id=0
	
class effect_log:
	comp_id=0
	counter=0
	ind_group_id=0
	entity_source=0
	entity_id=0


class aggs_log:
	ind_group_id=0
	stat_type=0
	max_count=0
	min_count=0
	avg_count_wla=0
	avg_count_all=0 
	

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
		
			if counter % 10 == 0 :
				curr.executemany(sql,tmp_data)	
				tmp_data=[]
				conn.commit()
		except:
			log("insert wla$client_action_daily error, comp_id:"+item.comp_id)
			continue

	curr.executemany(sql,tmp_data)	
	conn.commit()	


def load_to_client_effect_table(year_id,week_id,stat_date,stat_type,data):

	conn = get_mysql_conn()
	curr = conn.cursor()

	# initial table
	sql="""
		delete from """ + MYSQL_DB + """.wla$client_effect_daily 
                where year_id=%s and week_id=%s and stat_date=%s and stat_type=%s 
	    """
	curr.execute(sql,(year_id,week_id,stat_date,stat_type))
	
	# insert table
	sql="""
		insert into """ + MYSQL_DB + """.wla$client_effect_daily
		(comp_id,ind_group_id,entity_source,entity_id,year_id,week_id,stat_date,count,stat_type,create_by,create_time,last_update_by,last_update_time) 
		values(%s,%s,%s,%s,%s,%s,%s,%s,%s,0,%s,0,%s)
	    """

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


def load_to_client_aggs_table(year_id,week_id,stat_date,action_data,effect_data):
	
	conn = get_mysql_conn()
	curr = conn.cursor()


	# initial table
	sql="""
		delete from """ + MYSQL_DB + """.wla$client_aggs 
                where year_id=%s and week_id=%s
	    """
	curr.execute(sql,(year_id,week_id))

	# insert table
	sql="""
		insert into """ + MYSQL_DB + """.wla$client_aggs
		(year_id,week_id,ind_group_id,stat_type,stat_date,max_count,min_count,avg_count_all,avg_count_wla,create_by,create_time,last_update_by,last_update_time) 
		values(%s,%s,%s,%s,%s,%s,%s,%s,%s,0,%s,0,%s)
	    """
	
	#insert aggs data from action table
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

	# insert aggs data from effect table
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

'''
   get mapping dictionary :
   1. sdict[product_id] = comp_id
   2. cdict[comp_id]    = ind_id
   3. udict[url]        = comp_id 
'''

def get_product_comp_id_mapping():
	ckpt_file=DATA_DIR+"/CKPT_"+get_date_str()+"_sdict.json"

        if not is_file_exists(ckpt_file):
                url="http://" + SOLR_SRV + "/solr/product/select"
                params={
                        "version":"2.2",
                        "q":"*:*",
                        "start":"0",
                        "rows":"9000000",
                        "fl":"compId,productId",
                        "qt":"standard",
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

	
def get_gmcname_comp_id_mapping():
        ckpt_file=DATA_DIR+"/CKPT_"+get_date_str()+"_udict.json"
        if not is_file_exists(ckpt_file):
                url = "http://" + SOLR_SRV + "/solr/supplier/select"
                params={
                        "version":"2.2",
                        "q":"*:*",
                        "start":"0",
                        "rows":"90000",
                        "fl":"compId,gmcName",
                        "qt":"standard",
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
                comp_id = product["compId"]
                gmc_name  = product["gmcName"]
                udict[gmc_name]  = comp_id
	return udict	


def get_supplier_list():
	return [get_product_comp_id_mapping(),
		get_comp_ind_group_id_mapping(),
		get_gmcname_comp_id_mapping()
		]

