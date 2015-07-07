#!/usr/local/bin/python



from gm_common import *


def flush_to_db():
    log("flushing to stat db...")

    data=[]
    total=0
    
    for key in interest_counter :
        item = effect_log()
        item_arr=[]
        item_arr=interest_counter[key]
        item.comp_id=item_arr[0]
        item.ind_group_id=cdict[key]
        item.entity_source=STAT_TYPE.ENT_SRC_LC
        item.entity_id=item_arr[1]
        item.counter=item_arr[2]

        data.append(item)
        total=total+1
        
    year_id=get_curr_year_no()
    week_id=get_curr_week_no()
    stat_date=get_curr_date()
    stat_type=STAT_TYPE.BLY_CNT

    load_to_client_effect_table(year_id=year_id,
                week_id=week_id,
                stat_date=stat_date,
                stat_type=stat_type,
                data=data)

    log("insert total " + str(total) + " records ")
    return True


if __name__ == "__main__":

    # restore cache data
    sdict,cdict,udict=get_supplier_list() 
    
    # global variables 

    interest_counter = {}
    curr_date=sys.argv[1]

    oraSql="""
            SELECT comp_id, comp_id, COUNT (DISTINCT user_id)
                FROM (  SELECT bn.user_id, MIN (bnvl.view_time) view_time, wu.comp_id
                          FROM web$users wu, buyer$needs bn, buyer$need_view_logs bnvl
                         WHERE     1 = 1
                           AND wu.user_id = bnvl.user_id
                           AND bnvl.need_id = bn.need_id
                      GROUP BY bn.user_id, wu.comp_id)
               WHERE     1 = 1
                 AND view_time > TO_DATE ('""" + curr_date + """', 'yyyy-mm-dd')
                 AND view_time < TO_DATE ('""" + curr_date + """', 'yyyy-mm-dd') + 1
            GROUP BY comp_id 
            """

    #log(oraSql)

    oraConn=get_oracle_conn()
    oraCurr=oraConn.cursor()
    for oraRs in oraCurr.execute(oraSql):
        seller_comp_id=str(oraRs[0])
        leaf_cat_id=oraRs[1]
        counter=oraRs[2]

        item_arr=[]
        item_arr.append(seller_comp_id)
        item_arr.append(leaf_cat_id)
        item_arr.append(counter)

        # make sure we have ind_group_id
        if cdict.has_key(seller_comp_id):
            interest_counter[seller_comp_id]=item_arr

    oraConn.close()

    # At the end flush to db 
    flush_to_db()
