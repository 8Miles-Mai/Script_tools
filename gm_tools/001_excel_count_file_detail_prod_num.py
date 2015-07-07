__author__ = 'miles'

import MySQLdb
import xlrd


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
    # print sql
    # curr.execute(sql, (file_type, start_num, limit))
    curr.execute(sql, (file_type, start_num, limit))
    data = curr.fetchall()
    return data

def count_product_num_for_each(data):
    item_list = []
    #base_path = "/app_data/portal/"
    base_path = "/app/gmbatch/scripts/miles/file_details_scripts/exce/"
    counter = 0
    
    sql = """
        UPDATE """ + MYSQL_DB + """.wla$file_details SET prodNum = %s WHERE file_detail_id = %s
    """
    conn = get_mysql_conn()
    curr = conn.cursor()

    for temp in data:
        try:
            item = []
            
            file_path = base_path + str(temp[1])
            work_book = xlrd.open_workbook(file_path)
            table = work_book.sheets()[0]
            row_num = int(table.nrows) - 7
            item.append(int(row_num))
            item.append(int(temp[0]))
            item_list.append(item)
            counter += 1
            print item
            #print row_num
            if counter % 1000 == 0:
                curr.executemany(sql, item_list)
                item_list=[]
                conn.commit()

        except Exception, e:
            print e
            print 'update_error item = %s', item

    curr.executemany(sql, item_list)
    conn.commit()


if __name__=="__main__":
    data = get_file_details_data('P', 0, 4000)
    count_product_num_for_each(data)
