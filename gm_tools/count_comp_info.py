#!/usr/local/bin/python
# coding=utf-8
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

def get_store_info_from_mysql():
    print "start...get_store_info_from_mysql"
    conn = get_mysql_conn()
    curr = conn.cursor()
    sql="""
        SELECT
             temp.comp_id,
             (
                  CASE
                  WHEN temp.`在线分组数` > 0
                  OR temp.`是否有logo` = 'Y'
                  OR temp.`是否设置主题` = 'Y'
                  OR temp.`是否填写品牌故事` = 'Y' THEN
                       'Y' ELSE 'N' END ) 是否开始建设,
             temp.`是否有logo`,
             temp.`在线分组数`,
             temp.`是否设置主题`,
             temp.`是否填写品牌故事`,
             sc.*
        FROM ( SELECT sc.comp_id,
                       ( CASE WHEN sc.logo IS NULL
                            THEN 'N' ELSE 'Y' END ) 是否有logo,
                       ( SELECT count(0)
                            FROM store$group sg
                            WHERE sg.comp_id = sc.comp_id
                            AND STATUS = 7 ) 在线分组数,
                       ( SELECT ( CASE WHEN count(0) > 0
                                      THEN 'Y' ELSE 'N' END )
                            FROM `store$setting` ss
                            WHERE ss.comp_id = sc.comp_id
                              and cfg_theme_id is not null) 是否设置主题,
                       ( SELECT ( CASE WHEN count(0) > 0
                                      THEN 'Y' ELSE 'N' END )
                            FROM `store$brand` ss
                            WHERE ss.comp_id = sc.comp_id
                            AND STATUS = 7 ) 是否填写品牌故事
                  FROM `store$company` sc
             ) temp, `store$company` sc
        WHERE
             temp.comp_id = sc.comp_id
        """
    curr.execute(sql)
    comp_prod_list = curr.fetchall()
    curr.close()
    conn.close()
    print "end...get_store_info_from_mysql"
    return comp_prod_list


def flush_to_xls(prod_list, store_list):
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

    wsStore = wb.add_sheet('store_info')
    wsStore.write(0, 0, 'comp_id')
    # wsStore.write(0, 1, str('是否开始建设'.encode('utf-8')))
    # wsStore.write(0, 2, str('是否有logo'.encode('utf-8')))
    # wsStore.write(0, 3, str('在线分组数'.encode('utf-8')))
    # wsStore.write(0, 4, str('是否设置主题'.encode('utf-8')))
    # wsStore.write(0, 5, str('是否填写品牌故事'.encode('utf-8')))
    # wsStore.write(0, 6, 'comp_id(2)')
    # wsStore.write(0, 7, 'store_name')
    # wsStore.write(0, 8, 'store_name_cn')
    # wsStore.write(0, 9, 'subdomain')
    # wsStore.write(0, 10, 'logo')
    # wsStore.write(0, 11, 'status')
    # wsStore.write(0, 12, 'profile')
    # wsStore.write(0, 13, 'profile_cn')
    # wsStore.write(0, 14, 'contact')
    # wsStore.write(0, 15, 'mobile')
    # wsStore.write(0, 16, 'tel')
    # wsStore.write(0, 17, 'email')
    # wsStore.write(0, 18, 'apply_time')
    # wsStore.write(0, 19, 'online_time')
    # wsStore.write(0, 20, 'offline_time')
    # wsStore.write(0, 21, 'create_time')
    # wsStore.write(0, 22, 'create_by')
    # wsStore.write(0, 23, 'last_update_time')
    # wsStore.write(0, 24, 'last_update_by')
    

    index = 1
    for item_arr in store_list :
        # item_arr=[]
        # item_arr=store_list[key]
        wsStore.write(index, 0, str(item_arr[0]))
        wsStore.write(index, 1, str(item_arr[1]))
        wsStore.write(index, 2, str(item_arr[2]))
        wsStore.write(index, 3, str(item_arr[3]))
        wsStore.write(index, 4, str(item_arr[4]))
        wsStore.write(index, 5, str(item_arr[5]))
        # wsStore.write(index, 6, str(item_arr[6]))
        # wsStore.write(index, 7, str(item_arr[7]))
        # if item_arr[8]:
        #     wsStore.write(index, 8, str(item_arr[8].encode('utf-8')))
        # else:
        #     wsStore.write(index, 8, str(item_arr[8]))
        # wsStore.write(index, 9, str(item_arr[9]))
        # wsStore.write(index, 10, str(item_arr[10]))
        # wsStore.write(index, 11, str(item_arr[11]))
        # wsStore.write(index, 12, str(item_arr[12]))
        # wsStore.write(index, 13, str(item_arr[13]))
        # if item_arr[14]:
        #     wsStore.write(index, 14, str(item_arr[14].encode('utf-8')))
        # else:
        #     wsStore.write(index, 14, str(item_arr[14]))
        # wsStore.write(index, 15, str(item_arr[15]))
        # wsStore.write(index, 16, str(item_arr[16]))
        # wsStore.write(index, 17, str(item_arr[17]))
        # wsStore.write(index, 18, str(item_arr[18]))
        # wsStore.write(index, 19, str(item_arr[19]))
        # wsStore.write(index, 20, str(item_arr[20]))
        # wsStore.write(index, 21, str(item_arr[21]))
        # wsStore.write(index, 22, str(item_arr[22]))
        # wsStore.write(index, 23, str(item_arr[23]))
        # wsStore.write(index, 24, str(item_arr[24]))
        index=index+1
     
    nowdate = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    filePath = 'xls/'
    wbName = 'comp_spu_and_store_info_%s.xls' % nowdate
    wb.save(filePath + wbName)
    print "flush company spu and store info into %s" % str(wbName)
    return str(wbName)

SMTP_SERVER="smtp.globalmarket.com"
SMTP_USERNAME="miles.mai@corp.globalmarket.com"
SMTP_PASSWORD="monitor9394@01%"
MAIL_FROM="sysmon@corp.globalmarket.com"


# MAIL_TO_STR = "miles.mai@corp.globalmarket.com;windy.guo@corp.globalmarket.com;cherry.weng@corp.globalmarket.com;shirley.lau@corp.globalmarket.com"
MAIL_TO_STR = "miles.mai@corp.globalmarket.com"

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
    msg_root['Subject'] = " Company snowball m2b_prod_id leafCatId and sotre, by Batch job [count_comp_info] "
    html_mail_body='<html>Company snowball m2b_prod_id leafCatId and store info</html>'
    msg = MIMEMultipart()
    msg['To'] = mail_to_str
    msg.attach(MIMEText(html_mail_body,'plain','utf-8'))
    msg_root.attach(msg)

    print 'aaaaa'
    msg['Subject'] = " Company snowball m2b_prod_id leafCatId and sotre, by Batch job [count_comp_info] "
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
    store_list = get_store_info_from_mysql()
    wbName = flush_to_xls(prod_list, store_list)
    send_mail(wbName)
