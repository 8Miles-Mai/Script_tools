#!/usr/local/bin/python

from gm_common import *
import xlwt

def flush_to_xls():
    log("flushing to stat xml...")

    data=[]
    total=0
    wb = xlwt.Workbook()
    wsScore = wb.add_sheet('company scores')
    wsScore.write(0, 0, 'SFAID')
    wsScore.write(0, 1, 'ind_group_id')
    wsScore.write(0, 2, '>0.6')
    wsScore.write(0, 3, '>0.7')
    wsScore.write(0, 4, '>0.8')
    wsScore.write(0, 5, '>0.9')
    wsScore.write(0, 6, 'cLevel')
    index = 2
    for key in score_counter :
        item_arr=[]
        item_arr=score_counter[key]
        wsScore.write(index, 0, item_arr[0])
        wsScore.write(index, 1, cdict[key])
        wsScore.write(index, 2, item_arr[1])
        wsScore.write(index, 3, item_arr[2])
        wsScore.write(index, 4, item_arr[3])
        wsScore.write(index, 5, item_arr[4])
        wsScore.write(index, 6, item_arr[5])

        index=index+1

    wsScore.write(1, 0, '--------')
    wsScore.write(1, 1, '--------')
    wsScore.write(1, 2, xlwt.Formula("sum(C3:C" + str(index) +")"))
    wsScore.write(1, 3, xlwt.Formula("sum(D3:D" + str(index) +")"))
    wsScore.write(1, 4, xlwt.Formula("sum(E3:E" + str(index) +")"))
    wsScore.write(1, 5, xlwt.Formula("sum(F3:F" + str(index) +")"))
    wsScore.write(1, 6, '--------')

    wsLevel = wb.add_sheet('level count')
    wsLevel.write(0, 0, 'cLevel')
    wsLevel.write(0, 1, '>0.6')
    wsLevel.write(0, 2, '>0.7')
    wsLevel.write(0, 3, '>0.8')
    wsLevel.write(0, 4, '>0.9')
    index = 1
    for key in level_counter :
        item_arr=[]
        item_arr=level_counter[key]
        wsLevel.write(index, 0, item_arr[0])
        wsLevel.write(index, 1, item_arr[1])
        wsLevel.write(index, 2, item_arr[2])
        wsLevel.write(index, 3, item_arr[3])
        wsLevel.write(index, 4, item_arr[4])
        log("level count %s" % item_arr)
        index=index+1


    wbName = 'xls/company_scores_' + str(get_last_date()) + '.xls'
    wb.save(wbName)
    log("flush company scores info into " + str(wbName))
    return True


#----------------------------------------------------------------------------------

if __name__ == "__main__":

    # restore cache data
    sdict,cdict,udict=get_supplier_list()

    # global variables 

    score_counter = {}
    level_counter = {}

    oraSqlScore="""
              SELECT st.compId,
                     SUM (CASE WHEN st.iqScore = '0.6' THEN 1 ELSE 0 END) score6,
                     SUM (CASE WHEN st.iqScore = '0.7' THEN 1 ELSE 0 END) score7,
                     SUM (CASE WHEN st.iqScore = '0.8' THEN 1 ELSE 0 END) score8,
                     SUM (CASE WHEN st.iqScore = '0.9' THEN 1 ELSE 0 END) score9,
                     (select vv.cont_level from gm_oss.vw_seller_cont vv where vv.client_id = st.compId) cLevel
                FROM (SELECT ep.comp_Id compId,
                             CAST (ep.iq_score AS DECIMAL (18, 1)) iqScore
                        FROM gm_portal.expand$products ep
                       WHERE ep.IQ_score >= 0.6) st
            GROUP BY st.compId
           """

    oraSqlLevel="""
              SELECT NVL (st.cLevel, 'Null'),
                     SUM (CASE WHEN st.iqScore = '0.6' THEN 1 ELSE 0 END) score6,
                     SUM (CASE WHEN st.iqScore = '0.7' THEN 1 ELSE 0 END) score7,
                     SUM (CASE WHEN st.iqScore = '0.8' THEN 1 ELSE 0 END) score8,
                     SUM (CASE WHEN st.iqScore = '0.9' THEN 1 ELSE 0 END) score9
                FROM (SELECT ep.comp_Id compId,
                             CAST (ep.iq_score AS DECIMAL (18, 1)) iqScore,
                             (SELECT vv.cont_level
                                FROM gm_oss.vw_seller_cont vv
                               WHERE vv.client_id = ep.comp_Id)
                                cLevel
                        FROM gm_portal.expand$products ep
                       WHERE ep.IQ_score >= 0.6) st
            GROUP BY st.cLevel
            ORDER BY st.cLevel
           """
#####TODO#####
    oraConn=get_oracle_conn()
    oraCurr=oraConn.cursor()
    for oraRs in oraCurr.execute(oraSqlScore):
        seller_comp_id=str(oraRs[0])
        score6=oraRs[1]
        score7=oraRs[2]
        score8=oraRs[3]
        score9=oraRs[4]
        cLevel=oraRs[5]

        # make sure we have ind_group_id
        if cdict.has_key(seller_comp_id):
            item_arr=[]
            item_arr.append(seller_comp_id)
            item_arr.append(score6)
            item_arr.append(score7)
            item_arr.append(score8)
            item_arr.append(score9)
            item_arr.append(cLevel)
            score_counter[seller_comp_id]=item_arr

    for oraRs in oraCurr.execute(oraSqlLevel):
        seller_level=str(oraRs[0])
        score6=oraRs[1]
        score7=oraRs[2]
        score8=oraRs[3]
        score9=oraRs[4]

        # make sure we have ind_group_id
        item_arr=[]
        item_arr.append(seller_level)
        item_arr.append(score6)
        item_arr.append(score7)
        item_arr.append(score8)
        item_arr.append(score9)
        level_counter[seller_level]=item_arr

    oraConn.close()


    # At the end flush to xls
    flush_to_xls()