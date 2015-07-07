#!/usr/bin/python

#***********************************************************************
# Purpose: kick off other shell script by script code
# Revision History:
#   2012-07-06 : jie.zou  added myGMC statistic for task 8566
#***********************************************************************


import re
from gm_common import *


def check_product_update(compId):
  global update_product_counter
  try:
    if update_product_counter.has_key(compId) :
      update_product_counter[compId] = update_product_counter[compId]+1
    else :
      update_product_counter[compId] = 1
  except :
    error("compId not exist or error. compId:"+compId)


def check_product_add(compId):
  global add_product_counter
  try:
    if add_product_counter.has_key(compId) :
      add_product_counter[compId] = add_product_counter[compId]+1
    else :
      add_product_counter[compId] = 1
  except :
    error("compId not exist or error. compId:"+compId)



def flush_product_retrieve_to_db(arr, stat_type):
  data=[]
  total=0

  year_id=get_curr_year_no()
  week_id=get_curr_week_no()
  stat_date=get_curr_date()
  action_type=stat_type

  for key in arr:
    if cdict.has_key(key):
      item = action_log()
      item.comp_id=key
      item.counter=arr[key]
      item.ind_group_id=cdict[key]
      data.append(item)
      total=total+1
 
#  load_to_client_action_table(year_id=year_id, week_id=week_id, stat_date=stat_date, action_type=action_type, data=data)
  lead_or_refresh_to_client_action_table(year_id=year_id, week_id=week_id, stat_date=stat_date, action_type=action_type, data=data)

  log("insert total " + str(total) + " records")    
  return True;


def flush_to_db():
  log("processing add product counter ...")
  flush_product_retrieve_to_db(add_product_counter,STAT_TYPE.CREATE_PD_CNT)

  log("processing upadte product counter ...")
  flush_product_retrieve_to_db(update_product_counter,STAT_TYPE.UPDATE_PD_CNT)


if __name__=="__main__":
  """ The main pattern to process the raw nginx log
  """

  log("processing mygmc product click log")

  # define global holder
  add_product_counter={}
  update_product_counter={}

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
      if(line.find("productId: ")!=-1) :
        check_product_add(comp_id)
      else :
        check_product_update(comp_id)


  #the end flush to db
  flush_to_db()

