#!/usr/bin/python

#***********************************************************************
# Purpose: kick off other shell script by script code
# Revision History:
#   2012-07-06 : jie.zou  added myGMC statistic for task 8566
#***********************************************************************

import re
from gm_common import *


def check_buying_lead(compId):
  global buying_lead_counter
  try:
    if buying_lead_counter.has_key(compId) :
      buying_lead_counter[compId] = buying_lead_counter[compId]+1
    else :
      buying_lead_counter[compId] = 1
  except :
    error("compId not exist or error. compId:"+compId)



def flush_buying_lead_to_db(arr):
  """
     write to db:
  """

  log("flushing buying lead to stat db...")
  data=[]
  total=0

  year_id=get_curr_year_no()
  week_id=get_curr_week_no()
  stat_date=get_curr_date()
  stat_type=STAT_TYPE.BLY_CNT

  for key in arr :
    try:
      item = effect_log()
      item_arr=[]
      item_arr=arr
      item.comp_id=key
      item.ind_group_id=cdict[key]
      item.entity_source=STAT_TYPE.ENT_SRC_LC
      item.entity_id=key
      item.counter=arr[key]   
      data.append(item)
      total=total+1
    except:
      error("error not this compId:"+key)

#  load_to_client_effect_table(year_id=year_id, week_id=week_id, stat_date=stat_date, stat_type=stat_type,data=data)	
  load_or_refresh_to_client_effect_table(year_id=year_id, week_id=week_id, stat_date=stat_date, stat_type=stat_type,data=data)	

  log("insert total " + str(total) + " records")		
  return True


def flush_to_db():
  log("processing myGMC buying lead counter ...")
  flush_buying_lead_to_db(buying_lead_counter)



if __name__=="__main__":
  """ The main pattern to process the raw nginx log
  """

  log("processing mygmc buying lead log")

  # define global holder
  buying_lead_counter={}

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
    if comp_id != "" :
      check_buying_lead(comp_id)


  #the end flush to db
  flush_to_db()

