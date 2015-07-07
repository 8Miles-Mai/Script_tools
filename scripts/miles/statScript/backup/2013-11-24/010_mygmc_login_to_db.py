#!/usr/bin/python

#***********************************************************************
# Purpose: kick off other shell script by script code
# Revision History:
#   2012-07-06 : jie.zou  added myGMC statistic for task 8566
#***********************************************************************


import re
from gm_common import *

def check_comp_login(user_name):
  global login_counter,comp_id
  try :
#    comp_id = udict[user_name]
    comp_id = nudict[user_name.lower()]
    if not login_counter.has_key(comp_id):
      login_counter[comp_id]=1
  except : 
    error("compId not exist or error. user_name:"+user_name)


def flush_client_action_to_db_by_type(arr, stat_type):
  log("flushing action to stat db...")
  data=[]
  total=0

  year_id=get_curr_year_no()
  week_id=get_curr_week_no()
  stat_date=get_curr_date()
  action_type=stat_type

  for key in arr:
    if cdict.has_key(str(key)):
      item = action_log()
      item.comp_id=key
      item.counter=arr[key]
      item.ind_group_id=cdict[str(key)]
      data.append(item)
      total=total+1
  load_to_client_action_table(year_id=year_id, week_id=week_id, stat_date=stat_date, action_type=action_type, data=data)
#  lead_or_refresh_to_client_action_table(year_id=year_id, week_id=week_id, stat_date=stat_date, action_type=action_type, data=data)

  log("insert total " + str(total) + " records")
  return True;


def flush_to_db():
  log("processing myGMC login counter ...")
  flush_client_action_to_db_by_type(login_counter, STAT_TYPE.LOGIN_CNT)



if __name__=="__main__":
    """ The main pattern to process the raw nginx log
    """

    log("processing mygmc log")

    # define global holder
    login_counter={}

    # get cache data
    sdict,cdict,udict=get_supplier_list()
    nudict = get_mygmc_user_name_comp_id_mapping_list()

    counter = 1
    while True:
      line = sys.stdin.readline()

      # print message ever 10000 lines
      counter=counter + 1
      if counter % 10000 == 0 : 
        log("line %s" % counter)

      # 
      if not line :
        log("Total line:%s" % counter)
        break

      user_name = line.split("\t")[1]
      check_comp_login(user_name)


    #the end flush to db
    flush_to_db()
