#!/usr/bin/python

#***********************************************************************
# Purpose: kick off other shell script by script code
# Revision History:
#   2012-07-06 : jie.zou  added myGMC statistic for task 8566
#***********************************************************************

import re
from gm_common import *


def check_product_click(productId):
  global click_product_counter
  try:
    if click_product_counter.has_key(productId) :
      click_product_counter[productId] = click_product_counter[productId]+1
    else :
      click_product_counter[productId] = 1
  except :
    error("compId not exist or error. productId:"+str(productId))



def flush_click_product_to_db(arr):
  """
     write to db:
  """

  log("flushing click product to stat db...")
  data=[]
  total=0

  year_id=get_curr_year_no()
  week_id=get_curr_week_no()
  stat_date=get_curr_date()
  stat_type=STAT_TYPE.CLICK_CNT

  for key in arr:
    if sdict.has_key(key) :
      comp_id = sdict[key]
      if cdict.has_key(str(comp_id)):
        item               = effect_log()
        item.entity_source = STAT_TYPE.ENT_SRC_PRD
        item.entity_id     = key
        item.comp_id       = comp_id
        item.counter       = arr[key]/2
        item.ind_group_id  = cdict[str(comp_id)]
        data.append(item)
        total=total+1
    else :
      error("error, product click statistics, not mapping exist compId. numberId:"+str(key))

#  load_to_client_effect_table(year_id=year_id, week_id=week_id, stat_date=stat_date, stat_type=stat_type, data=data)
  load_or_refresh_to_client_effect_table(year_id=year_id, week_id=week_id, stat_date=stat_date, stat_type=stat_type, data=data)

  log("insert total " + str(total) + " records")    
  return True;


def flush_to_db():
  log("processing myGMC product click counter ...")
  flush_click_product_to_db(click_product_counter)



if __name__=="__main__":
  """ The main pattern to process the raw nginx log
  """

  log("processing mygmc product click log")

  # define global holder
  click_product_counter={}

  # get cache data
  sdict,cdict,udict=get_supplier_list()
#  mdict = get_mygmc_member_id_comp_id_mapping_list()

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

    product_id = get_compId_from_line(line, "productId:")
    if product_id != "" :
      check_product_click(product_id)


  #the end flush to db
  flush_to_db()

