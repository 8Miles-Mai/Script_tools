__author__ = 'miles'

import MySQLdb
import xlrd
import urllib2
import os

MYSQL_SERVER="192.168.23.240"
MYSQL_USER = "app_wla"
MYSQL_PASSWORD = "webloganalysis"
MYSQL_DB = "web_log_analysis"

def get_mysql_conn():
    try:
        mysql_conn = MySQLdb.connect(user=MYSQL_USER,
                  charset='utf8',
                  host=MYSQL_SERVER,
                  passwd=MYSQL_PASSWORD,
                  db=MYSQL_DB)
        return mysql_conn
    except Exception, e:
        ERROR_HINT = " [ get mysql connection failed ] MYSQL_USER:"+MYSQL_USER+", MYSQL_SERVER:"+MYSQL_SERVER+", MYSQL_DB:"+MYSQL_DB
        print ERROR_HINT
        print e
        return None

def get_file_details_data(file_type, start_num, limit):
    if start_num < 0:
        print 'star_num < 0'
        return
    if limit <= 0:
        print 'limit <= 0'
        return
    if file_type not in ('P', 'E'):
        print 'file_type must be "P" or "E" '
        return

    sql="""
        SELECT file_detail_id, file_uri FROM """ + MYSQL_DB + """.wla$file_details WHERE file_type = %s AND prodNum is null ORDER BY file_detail_id ASC LIMIT %s, %s
        """
    # sql="""
    #     SELECT file_detail_id, file_uri FROM """ + MYSQL_DB + """.wla$file_details WHERE file_type = %s 
    #     """
    conn = get_mysql_conn()
    curr = conn.cursor()
    print sql
    # curr.execute(sql, (file_type, start_num, limit))
    curr.execute(sql, (file_type, start_num, limit))
    data = curr.fetchall()
    return data

def download_files(data):
    file_path = '/app/gmbatch/scripts/miles/file_details_scripts/exce/'
    base_url = 'http://img01.globalmarket.com/'
    for item in data:
        file_id = item[0]
        file_name = item[1]
        dir = 'exce/' + file_name[:16]
        if os.path.isdir(dir):
            pass
        else:
            os.makedirs(dir)
       
        print dir
        print "download file name: %s", file_name
        url_file = urllib2.urlopen(base_url + file_name)
        #with open(file_path + filename, "wb") as code:
        #    code.write(f.read())
        f = open(file_path+file_name, "wb")
        f.write(url_file.read())
        f.close()
    print "download_file end."


if __name__=="__main__":
    data = get_file_details_data('P', 0, 10000)
    download_files(data)
