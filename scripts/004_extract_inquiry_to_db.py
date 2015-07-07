#!/usr/local/bin/python


from gm_common import *


def flush_to_db():
    log("flushing to stat db...")

    data=[]
    total=0

    for key in inquiry_counter :
        item = effect_log()
        item_arr=[]
        item_arr=inquiry_counter[key]
        item.comp_id=item_arr[0]
        item.ind_group_id=cdict[key]

        if item_arr[3] == STAT_TYPE.INQ_FOR_CMP:
            item.entity_source=STAT_TYPE.ENT_SRC_CMP
            item.entity_id=item_arr[0]
        if item_arr[3] == STAT_TYPE.INQ_FOR_PRD:
            item.entity_source=STAT_TYPE.ENT_SRC_PRD
            item.entity_id=item_arr[1]
        item.counter=item_arr[2]
        data.append(item)
        total=total+1

    year_id=get_curr_year_no()
    week_id=get_curr_week_no()
    stat_date=get_curr_date()
    stat_type=STAT_TYPE.INQ_CNT
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

    inquiry_counter = {}
    curr_date=sys.argv[1]

    oraSql="""
            select seller_comp_id,product_id,count(1),inquiry_type
              from 
              ( select ir.inquiry_id         inquiry_id,
                       (select wu.comp_id
                          from web$users wu, im$inquiries ii
                         where wu.user_id = ii.sender_user_id
                           and ii.inquiry_id = ir.inquiry_id) buyer_comp_id,
                       ir.comp_id seller_comp_id,
                       (select ii.inquiry_type
                          from im$inquiries ii
                         where ii.inquiry_id = ir.inquiry_id) inquiry_type,
                       iip.product_id        product_id,
                       ir.create_time        create_time
                  FROM im$inq_recipients ir,
                       im$inquiries      inq,
                       im$inq_products   iip
                 WHERE ir.create_time > to_date('""" + curr_date + """', 'yyyy-mm-dd')
                   and ir.create_time < to_date('""" + curr_date + """', 'yyyy-mm-dd') + 1
                   AND ir.inquiry_id = inq.inquiry_id 
                   and inq.status = 7
                   and ir.inq_recipient_id = iip.inq_recipient_id(+)
                   and exists
                        (select null
                          from im$inq_sources iis
                         where (iis.source_code = '04031600' OR iis.source_code LIKE '01%')
                           and iis.inquiry_id = ir.inquiry_id) )
            group by seller_comp_id, product_id, inquiry_type
           """

    oraConn=get_oracle_conn()
    oraCurr=oraConn.cursor()
    for oraRs in oraCurr.execute(oraSql):
        seller_comp_id=str(oraRs[0])
        product_id=oraRs[1]
        counter=oraRs[2]
        inquiry_type=oraRs[3]

        # make sure we have ind_group_id
        if cdict.has_key(seller_comp_id):
            item_arr=[]
            item_arr.append(seller_comp_id)
            item_arr.append(product_id)
            item_arr.append(counter)
            item_arr.append(inquiry_type)
            inquiry_counter[seller_comp_id]=item_arr

    oraConn.close()

    # At the end flush to db 
    flush_to_db()

