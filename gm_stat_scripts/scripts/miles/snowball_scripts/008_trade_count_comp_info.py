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
MYSQL_DB = "gmcore"
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
        select pro.product_base_id '商品ID', pro.product_variation_id '组合ID',
            pro.comp_id '公司ID', sc.subdomain '域名',
            case when pro.status = 0 then '草稿' else
                case when pcd.`status` = 0 then '草稿' else
                    case when pcd.`status` = 7 then '上架' else
                        case when pcd.`status` = -13 then '下架' else
                            '草稿'
                        end
                    end
                end
            end '状态',
            pca.category_id '分类ID',
            clc.cat_name '分类名',
            clc.cat_name_cn '分类中文名'
        from pro_product_base pro 
            left join pcd_product_channel_detail pcd
                on pro.product_base_id = pcd.product_base_id
                and pcd.channel_id = 15
            left join m2cchinaerp.`store$company` sc
                on pro.comp_id = sc.comp_id
            left join pca_product_category pca
                on pro.product_base_id = pca.product_base_id
            left join clc_leaf_category clc
                on pca.category_id = clc.leaf_category_id
        where 1=1
        order by pro.product_variation_id asc, pro.product_base_id asc
        """
    curr.execute(sql)
    comp_prod_list = curr.fetchall()
    curr.close()
    conn.close()
    return comp_prod_list

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
                            FROM m2cchinaerp.store$group sg
                            WHERE sg.comp_id = sc.comp_id
                            AND STATUS = 7 ) 在线分组数,
                       ( SELECT ( CASE WHEN count(0) > 0
                                      THEN 'Y' ELSE 'N' END )
                            FROM m2cchinaerp.`store$setting` ss
                            WHERE ss.comp_id = sc.comp_id
                              and cfg_theme_id is not null) 是否设置主题,
                       ( SELECT ( CASE WHEN count(0) > 0
                                      THEN 'Y' ELSE 'N' END )
                            FROM m2cchinaerp.`store$brand` ss
                            WHERE ss.comp_id = sc.comp_id
                            AND STATUS = 7 ) 是否填写品牌故事
                  FROM m2cchinaerp.`store$company` sc
             ) temp, m2cchinaerp.`store$company` sc
        WHERE
             temp.comp_id = sc.comp_id
        """
    curr.execute(sql)
    comp_prod_list = curr.fetchall()
    curr.close()
    conn.close()
    print "end...get_store_info_from_mysql"
    return comp_prod_list


def flush_to_xls(comp_prod_list, store_list):
    print "flushing to stat xml..."

    data=[]
    total=0
    wb = xlwt.Workbook(encoding='utf-8')
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = 'SimSun'
    style.font = font

    wsScore = wb.add_sheet('comp_prod_leafCat')
    wsScore.write(0, 0, '商品ID', style)
    wsScore.write(0, 1, '组合ID', style)
    wsScore.write(0, 2, '公司ID', style)
    wsScore.write(0, 3, '域名', style)
    wsScore.write(0, 4, '状态', style)
    wsScore.write(0, 5, '分类ID', style)
    wsScore.write(0, 6, '分类名', style)
    wsScore.write(0, 7, '分类中文名', style)

    index = 1
    for prod in comp_prod_list :
        ii=0
        for item in prod :
            wsScore.write(index, ii, str(item), style)
            ii=ii+1
        index=index+1

    wsStore = wb.add_sheet('store_info')
    wsStore.write(0, 0, 'comp_id')
    wsStore.write(0, 1, '是否开始建设')
    wsStore.write(0, 2, '是否有logo')
    wsStore.write(0, 3, '在线分组数')
    wsStore.write(0, 4, '是否设置主题')
    wsStore.write(0, 5, '是否填写品牌故事')

    index = 1
    for item_arr in store_list :
        ii = 0
        for item in item_arr :
            wsStore.write(index, ii, str(item))
            ii=ii+1
        index=index+1
     
    nowdate = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    filePath = 'xls/'
    wbName = 'comp_spu_and_store_info_%s.xls' % nowdate
    wb.save(filePath + wbName)
    print "flush company spu and store info into %s" % str(wbName)
    return str(wbName)

SMTP_SERVER="smtp.globalmarket.com"
SMTP_USERNAME="miles.mai@corp.globalmarket.com"
#SMTP_USERNAME="sysmon@corp.globalmarket.com"
#SMTP_PASSWORD="monitor9394@01%"
SMTP_PASSWORD="XIAOmai"
#MAIL_FROM="sysmon@corp.globalmarket.com"
MAIL_FROM="miles.mai@corp.globalmarket.com"

# MAIL_TO_STR = "ken.lei@corp.globalmarket.com;miles.mai@corp.globalmarket.com;windy.guo@corp.globalmarket.com;cherry.weng@corp.globalmarket.com;shirley.lau@corp.globalmarket.com;jalwar.woo@corp.globalmarket.com;eva.lee@corp.globalmarket.com"
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
    # store_list = []
    store_list = get_store_info_from_mysql()
    wbName = flush_to_xls(comp_prod_list, store_list)
    send_mail(wbName)
