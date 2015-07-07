#!/usr/local/bin/python
#import pymongo
import MySQLdb
import cx_Oracle
import xlwt
import time


# MYSQL_SERVER = "192.168.86.121"
# MYSQL_USER = "root"
# MYSQL_PASSWORD = "123456"
# MYSQL_DB = "m2cchinaerp"
# MYSQL_PORT = 3306

MYSQL_SERVER = "192.168.24.240"
MYSQL_USER = "app_erp"
MYSQL_PASSWORD = "IntoErpOK"
MYSQL_DB = "m2cchinaerp"
MYSQL_PORT = 3308

ORACLE_SERVICE="192.168.23.238:1521/core01.db.globalmarket.com"
ORACLE_USER="query_molo"
ORACLE_PASSWORD="QueRy_MoLo_qwe!@#"

# ORACLE_SERVICE="192.168.86.17:1521/core01.db.globalmarket.com"
# ORACLE_USER="APP_SOA2"
# ORACLE_PASSWORD="abc12355555"

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

def get_oracle_conn():
    try:
        oracle_conn = cx_Oracle.connect(ORACLE_USER, ORACLE_PASSWORD, ORACLE_SERVICE)
        return oracle_conn
    except Exception,e:
        print e
        return None

def get_spu_comp_prod_from_mysql():
    conn = get_mysql_conn()
    curr = conn.cursor()
    sql="""
        SELECT DISTINCT comp_id, m2b_prod_id  FROM
          (
          SELECT pp.`comp_id`, pp.`m2b_prod_id` 
          FROM `erp$pro$product` pp 
          WHERE pp.`status` = 7 
            AND pp.`m2b_prod_id` IS NOT NULL
            AND pp.`m2b_prod_id` <> 0 
          UNION ALL 
          SELECT pps.`comp_id`, pps.`m2b_prod_id` 
          FROM `erp$pro$product_sku` pps 
          WHERE pps.`status` = 7 
            AND pps.`m2b_prod_id` IS NOT NULL
            AND pps.`m2b_prod_id` <> 0 
            ) temp
        """
    curr.execute(sql)
    comp_prod_list = curr.fetchall()
    curr.close()
    conn.close()
    return comp_prod_list

def get_product_leaf_cat_id(comp_prod_list):
    print "start...get_product_leaf_cat_id"

    sql="""
        SELECT pc.comp_id,
               pc.product_id,
               pc.leaf_cat_id,
               glc.cat_name
          FROM seller$prod_cats pc, gm$leaf_cats glc
         WHERE 1 = 1 
           AND pc.leaf_cat_id = glc.leaf_cat_id 
           AND pc.comp_id IN %s
           AND pc.product_id in %s
        """
    
    conn = get_oracle_conn()
    curr = conn.cursor()
    temp_data = []
    comp_id_list = []
    prod_id_list = []
    counter = 0
    prod_list = {}
    for prod in comp_prod_list:
        if not prod[0]:
            continue
        if not prod[1]:
            continue
        comp_id_list.append(int(prod[0]))
        prod_id_list.append(int(prod[1]))
        counter += 1
        if counter % 1000 == 0:
            temp_data.append(tuple(comp_id_list))
            temp_data.append(tuple(prod_id_list))

            for oraRs in curr.execute(sql % tuple(temp_data)):
                item_arr=[]
                item_arr.append(oraRs[0])
                item_arr.append(oraRs[1])
                item_arr.append(oraRs[2])
                item_arr.append(oraRs[3])
                prod_list[str(oraRs[1])] = item_arr
            temp_data = []
            comp_id_list = []
            prod_id_list = []

    temp_data.append(tuple(comp_id_list))
    temp_data.append(tuple(prod_id_list))

    for oraRs in curr.execute(sql % tuple(temp_data)):
        item_arr=[]
        item_arr.append(oraRs[0])
        item_arr.append(oraRs[1])
        item_arr.append(oraRs[2])
        item_arr.append(oraRs[3])
        prod_list[str(oraRs[1])] = item_arr
    
    return prod_list
    print "end...get_product_leaf_cat_id"

def flush_to_xls(prod_list):
    print "flushing to stat xml..."

    data=[]
    total=0
    wb = xlwt.Workbook()
    wsScore = wb.add_sheet('comp_prod_leafCat')
    wsScore.write(0, 0, 'compId')
    wsScore.write(0, 1, 'prodId')
    wsScore.write(0, 2, 'leafCatId')
    wsScore.write(0, 3, 'leafCatName')

    index = 1
    for key in prod_list :
        item_arr=[]
        item_arr=prod_list[key]
        wsScore.write(index, 0, item_arr[0])
        wsScore.write(index, 1, item_arr[1])
        wsScore.write(index, 2, item_arr[2])
        wsScore.write(index, 3, item_arr[3])
        index=index+1
    nowdate = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    filePath = 'xls/'
    wbName = 'comp_prod_leafCat_%s.xls' % nowdate
    wb.save(filePath + wbName)
    print "flush comp prod leafCat info into %s" % str(wbName)
    return str(wbName)

SMTP_SERVER="smtp.globalmarket.com"
SMTP_USERNAME="sysmon@corp.globalmarket.com"
SMTP_PASSWORD="monitor9394@01%"
MAIL_FROM="sysmon@corp.globalmarket.com"


MAIL_TO_STR = "miles.mai@corp.globalmarket.com;windy.guo@corp.globalmarket.com;cherry.weng@corp.globalmarket.com;shirley.lau@corp.globalmarket.com"

def send_mail(wbName):
    import smtplib
    import mimetypes
    from email.mime.multipart import MIMEMultipart
    from email.mime.base import MIMEBase
    from email.mime.text import MIMEText
    from email.mime.audio import MIMEAudio
    from email.mime.image import MIMEImage
    from email.Encoders import encode_base64
    from email import Encoders
    from email.utils import COMMASPACE, formatdate
    msg_root = MIMEMultipart()
    msg_root['From'] = MAIL_FROM
    smtp_server = SMTP_SERVER
    smtp_username = SMTP_USERNAME
    smtp_password = SMTP_PASSWORD
    mail_from = MAIL_FROM
    mail_to_str = MAIL_TO_STR
    mail_to = mail_to_str.split(";")
    msg_root['To'] = mail_to
    msg_root['Subject'] = " Company snowball m2b_prod_id leafCatId, by Batch job [count_spu_sku_num] "
    html_mail_body='<html>Company snowball m2b_prod_id leafCatId</html>'
    msg = MIMEMultipart()
    msg['To'] = mail_to_str
    msg.attach(MIMEText(html_mail_body,'plain','utf-8'))
    msg_root.attach(msg)

    print 'aaaaa'
    msg['Subject'] = " Company snowball m2b_prod_id leafCatId, by Batch job [count_spu_sku_num] "
    filePath = '/app/gmbatch/scripts/miles/snowball_scripts/xls/' + wbName
    print filePath
    fd = file(filePath,"rb")
    mimetype,mimeencoding = mimetypes.guess_type(filePath)
    if mimeencoding or (mimetype is None):
        mimetype = "application/octet-stream"
    maintype,subtype = mimetype.split("/")
    if maintype == "text":
        retval = MIMEText(fd.read(), _subtype = subtype)
    else:
        retval = MIMEBase(maintype,subtype)
        retval.set_payload(fd.read())
        Encoders.encode_base64(retval)

    retval.add_header("Content-Disposition","attachment",filename = wbName)
    fd.close()
    msg.attach(retval)

    mailServer = smtplib.SMTP(smtp_server, 25)

    mailServer.set_debuglevel(0)
    mailServer.ehlo()
    # mailServer.startls()
    mailServer.login(smtp_username, smtp_password)
    mailServer.sendmail(mail_from, mail_to, msg.as_string())
    mailServer.close()

    print "email send to %s" % mail_to

#-------------------------------------------------------------------------------------------


if __name__ == '__main__':
    print "begin..."
    comp_prod_list = get_spu_comp_prod_from_mysql()
    # comp_prod_list = ((100609, 101972), (100609, 102026))
    # print comp_prod_list
    prod_list = get_product_leaf_cat_id(comp_prod_list)
    wbName = flush_to_xls(prod_list)
    send_mail(wbName)