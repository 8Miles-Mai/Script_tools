#!/usr/local/bin/python

from gm_common import *

def flush_to_db():
    log("flushing to stat db...")
    # TO_DO get time by parameter
    data=[]
    total=0
    for key in display_counter :
        item = effect_log()
        item_arr = []
        item_arr = display_counter[key]
        item.comp_id=item_arr[0]
        item.counter=item_arr[1]

        if cdict.has_key(item.comp_id) :
            item.ind_group_id=cdict[item.comp_id]
            item.entity_source=STAT_TYPE.ENT_SRC_PRD
            item.entity_id=key
            data.append(item)
            total=total+1

    year_id=get_curr_year_no()
    week_id=get_curr_week_no()
    stat_date=get_curr_date()
    stat_type=STAT_TYPE.DISPLAY_CNT
    load_to_client_effect_table(year_id=year_id, week_id=week_id, stat_date=stat_date, stat_type=stat_type, data=data)
    log("insert total " + str(total) + " records")
    return True


class log_item:
    click_from = ''
    time = ''
    referrer = ''
    url = ''
    agent = ''
    language = ''
    ip = ''
    country = ''
    city = ''
    session_id = ''
    user_id = ''
    user_type = ''
    load_time = ''
    stay_time = ''
    keyword = ''
    cat = ''
    show_types = ''
    show_pids = ''
    show_sids = ''
    show_blids = ''
    page_pid = ''
    page_sid = ''
    page_blid = ''
    resolution = ''
    color = ''
    isFlashEnabled = ''
    isJavaEnabled = ''
    mouseXY = ''
    scrollXY = ''
    utmcsr = ''
    utmccn = ''
    utmcmd = ''
    utmctr = ''
    utmcct = ''
    utmgclid = ''


def splitFileShowTimes(line):
    item_list = line.split("\t")
    item = log_item

    if len(item_list) >=34:
        item.time = item_list[0]
        item.referrer = item_list[1]
        item.url = item_list[2]
        item.agent = item_list[3]
        item.language = item_list[4]
        item.ip = item_list[5]
        item.country = item_list[6]
        item.city = item_list[7]
        item.session_id = item_list[8]
        item.user_id = item_list[9]
        item.user_type = item_list[10]
        item.load_time = item_list[11]
        item.stay_time = item_list[12]
        item.keyword = item_list[13]
        item.cat = item_list[14]
        item.show_types = item_list[15]
        item.show_pids = item_list[16]
        item.show_sids = item_list[17]
        item.show_blids = item_list[18]
        item.page_pid = item_list[19]
        item.page_sid = item_list[20]
        item.page_blid = item_list[21]
        item.resolution = item_list[22]
        item.color = item_list[23]
        item.isFlashEnabled = item_list[24]
        item.isJavaEnabled = item_list[25]
        item.mouseXY = item_list[26]
        item.scrollXY = item_list[27]
        item.utmcsr = item_list[28]
        item.utmccn = item_list[29]
        item.utmcmd = item_list[30]
        item.utmctr = item_list[31]
        item.utmcct = item_list[32]
        item.utmgclid = item_list[33]
        return item
    else:
        item = None
        return item


def check_product_display(line):
    global display_counter
    item = splitFileShowTimes(line)
    if None != item:
        if len(item.show_types) >1:
            product_list = item.show_pids.split("+")
            i = -1
            for product_ids in product_list :
                i = i+1
                try :
                    pids = product_ids.split("_")
                    for product_id in pids :
                        item_arr = []
                        try :
                            comp_id=sdict[product_id]
                            if product_id and comp_id :
                                item_arr.append(comp_id)
                                if product_id and product_id!='-' :
                                    if display_counter.has_key(product_id) :
                                        item_arr.append(display_counter[product_id][1]+1)
                                    else :
                                        item_arr.append(1)
                                    display_counter[product_id]=item_arr
                        except:
                            continue
                except:
                    continue




if __name__ == "__main__":

    # restore cache data
    sdict,cdict,udict=get_supplier_list() 
    
    # global variables 
    display_counter = {}    

    counter = 1
    while True :
        line=sys.stdin.readline()

        # print message ever 1000 lines    
        counter=counter + 1
        if counter % 1000 == 0 : 
            log("line %s" % counter)
        if not line :
            log("Total line:%s" % counter)
            break
        
        item_arr=[]
        check_product_display(line)


    # At the end flush to db 
    flush_to_db()



