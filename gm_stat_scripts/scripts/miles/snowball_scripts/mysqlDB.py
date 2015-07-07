__author__ = 'miles'

import MySQLdb

def get_mysql_conn(MYSQL_USER, MYSQL_SERVER, MYSQL_PASSWORD, MYSQL_DB, MYSQL_PORT):
    try:
        mysql_conn = MySQLdb.connect(user=MYSQL_USER,
                  charset='utf8',
                  host=MYSQL_SERVER,
                  passwd=MYSQL_PASSWORD,
                  db=MYSQL_DB,
                  port=MYSQL_PORT)
        return mysql_conn
    except Exception, e:
        ERROR_HINT = " [ get mysql connection failed ] MYSQL_USER:"+MYSQL_USER+", MYSQL_SERVER:"+MYSQL_SERVER+", MYSQL_DB:"+MYSQL_DB
        print ERROR_HINT
        print e
        return None
