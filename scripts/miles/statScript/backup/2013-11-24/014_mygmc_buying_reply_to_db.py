#!/usr/bin/python

#***********************************************************************
# Purpose: kick off other shell script by script code
# Revision History:
#   2012-07-06 : jie.zou  added myGMC statistic for task 8566
#***********************************************************************


import re
from gm_common import *


def check_buying_reply(compId):
  global buying_reply_counter
  try:
    if buying_reply_counter.has_key(compId) :
      buying_reply_counter[compId] = buying_reply_counter[compId]+1
    else :
      buying_reply_counter[compId] = 1
  except :
    error("compId not exist or error. compId:"+compId)



def flush_buying_reply_to_db(arr):
  """
     write to db:
  """

  log("flushing buying reply to stat db...")
  data=[]
  total=0

  year_id=get_curr_year_no()
  week_id=get_curr_week_no()
  stat_date=get_curr_date()
  action_type=STAT_TYPE.REPLY_CNT

  for key in arr :
    item = action_log()
    item.comp_id=key
    item.counter=arr[key]
    item.ind_group_id=cdict[key]
    data.append(item)
    total=total+1

#  load_to_client_action_table(year_id=year_id, week_id=week_id, stat_date=stat_date, action_type=action_type, data=data)
  lead_or_refresh_to_client_action_table(year_id=year_id, week_id=week_id, stat_date=stat_date, action_type=action_type, data=data)

  log("insert total " + str(total) + " records")		
  return True


def flush_to_db():
  log("processing myGMC buying reply counter ...")
  flush_buying_reply_to_db(buying_reply_counter)



if __name__=="__main__":
  """ The main pattern to process the raw nginx log
  """

  log("processing mygmc buying reply log")

  # define global holder
  buying_reply_counter={}

  # get cache data
  sdict,cdict,udict=get_supplier_list()

  counter = 1

  while True:
    line = sys.stdin.readline()

    # print message ever 10000 lines
    counter=counter + 1
    if counter % 10000 == 0 : 
      log("line %s" % counter)

    if not line :
      log("Total line:%s" % counter)
      break

    comp_id = get_compId_from_line(line, "compId=")
    check_buying_reply(comp_id)


  #the end flush to db
  flush_to_db()

