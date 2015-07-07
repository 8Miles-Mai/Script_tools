#!/usr/local/bin/python
__author__ = 'miles'

from gm_common import *
import json
import time
#import httplib, urllib
import urllib
import httplib2

def send_edm(inquiry_list):
    print "start...send_edm"
    for id in inquiry_list:
        if not id:
            continue
        url = 'http://192.168.24.151:58080/gmsoa/soaemailservice/sendInquiryMailByInquiryId.gm'
        body = {'inquiryId' : id, 'subject' : inquiry_list[id][1]}
        headers = {"Content-type": "application/x-www-form-urlencoded"}
        response, content = http.request(url, 'POST', headers=headers, body=urllib.parse.urlencode(body))
        data = response.read()
        print response
        print "========"
        print params, data
        conn.close
    print "end...send_edm"


#----------------------------------------------------------------------------------


def get_inquiry_list():
    print "start...get_inquiry_list"
    oraSqlInquiry="""
              select ii.inquiry_id, ii.subject 
              from im$inquiries ii 
              where ii.status = 7
              and not exists (
                  select null 
                  from GM_EDM.I_MAIL$MESSAGEs m 
                  where m.src_entity_type = 40 
                  and m.src_entity_id = ii.inquiry_id 
              )
              and ii.create_time > sysdate - 7
              order by ii.create_time desc
           """
    oraConn=get_oracle_conn()
    oraCurr=oraConn.cursor()

    inquiry_list = {}
    for oraRs in oraCurr.execute(oraSqlInquiry):
        item_arr=[]
        item_arr.append(oraRs[0])
        item_arr.append(oraRs[1])
        inquiry_list[str(oraRs[0])] = item_arr

    oraConn.close()
    print "end...get_inquiry_list"
    return inquiry_list

if __name__ == "__main__":
    print "========  ========"
    print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    print "begin...extract_inquiry_for_edm"
    inquiry_list = get_inquiry_list()

    # At the end query for send edm
    send_edm(inquiry_list)

    print "end...extract_inquiry_for_edm"
    print "======== ========"
