#!/usr/local/bin/python


from gm_common import *


def flush_to_db():
    log("flushing to stat db...")
    # TO_DO get time by parameter
    data=[]
    total=0
    for key in replies_counter :
        item = action_log()
        item_arr=[]
        item_arr=replies_counter[key]
        item.comp_id=item_arr[0]
        item.counter=item_arr[1]
        item.ind_group_id=cdict[key]
        data.append(item)
        total=total+1

    year_id=get_curr_year_no()
    week_id=get_curr_week_no()
    stat_date=get_curr_date()
    action_type=STAT_TYPE.REPLY_CNT
    load_to_client_action_table(year_id=year_id,
                    week_id=week_id,
                    stat_date=stat_date,
                    action_type=action_type,
                    data=data)

    log("insert total " + str(total) + " records ")
    return True


if __name__ == "__main__":

    # restore cache data
    sdict,cdict,udict=get_supplier_list() 

    # global variables 
    replies_counter = {}
    curr_date=sys.argv[1]

    oraSql="""
            select seller_comp_id,count(0)
              from 
                  (select wu.comp_id       seller_comp_id
                          ,'inquiry'       type
                          ,iir.create_time create_time
                     from im$inq_replies iir
                          ,web$users       wu
                    where iir.create_time > to_date('""" + curr_date + """','yyyy-mm-dd')  
                      and iir.create_time < to_date('""" + curr_date + """', 'yyyy-mm-dd')+1 
                      and iir.sender_user_id = wu.user_id
                      and exists (select null from seller$companies scp where scp.comp_id=wu.comp_id)
                  union all
                   select wu.comp_id        seller_comp_id
                          ,'buylead'        type
                          ,ibnr.create_time create_time
                     from im$buyer_need_replies ibnr
                          ,web$users              wu
                    where ibnr.create_time > to_date('""" + curr_date + """','yyyy-mm-dd')  
                      and ibnr.create_time < to_date('""" + curr_date + """', 'yyyy-mm-dd')+1 
                      and ibnr.sender_user_id = wu.user_id
                      and exists (select null from seller$companies scp where scp.comp_id=wu.comp_id)
                   )
            group by seller_comp_id
            """

    oraConn=get_oracle_conn()
    oraCurr=oraConn.cursor()
    total=0
    for oraRs in oraCurr.execute(oraSql):

        seller_comp_id=str(oraRs[0])
        counter=oraRs[1]

        item_arr=[]
        item_arr.append(seller_comp_id)
        item_arr.append(counter)

        # make sure we have ind_group_id
        if cdict.has_key(seller_comp_id):
            replies_counter[seller_comp_id]=item_arr

    oraConn.close()

    # At the end flush to db 
    flush_to_db()
