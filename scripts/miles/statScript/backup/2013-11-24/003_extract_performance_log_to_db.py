#!/usr/local/bin/python

import re
from gm_common import *


def check_comp_login():

	global login_counter,comp_id
	pattern="compId-([\d]*)"
	m=re.search(pattern,line)
	if m :
		comp_id=m.group(1)
		if not login_counter.has_key(comp_id):
			login_counter[comp_id]=1


#2012-07-06 1645, amended by jie.zou, for task 
def check_product_update():
	global update_product_counter
	pattern="/mygm/product/product/edit.gm"
	m=re.search(pattern,line)
	if m:
		if update_product_counter.has_key(comp_id):
			update_product_counter[comp_id]=update_product_counter[comp_id]+1
		else:
			update_product_counter[comp_id]=1
		return True


#2012-07-06 1645, amended by jie.zou, for task 
def check_product_create():
        global create_product_counter
        pattern="/mygm/product/product/add.gm"
        m=re.search(pattern,line)
        if m:
                if create_product_counter.has_key(comp_id):
                        create_product_counter[comp_id]=create_product_counter[comp_id]+1
                else:
                        create_product_counter[comp_id]=1
                return True


def flush_to_db_by_type(arr, stat_type):
        data=[]
        total=0
        for key in arr:
                if cdict.has_key(key):
                        item = action_log()
                        item.comp_id=key
                        item.counter=arr[key]
                        item.ind_group_id=cdict[key]
                        data.append(item)
                        total=total+1
        year_id=get_curr_year_no()
        week_id=get_curr_week_no()
        stat_date=get_curr_date()
        action_type=stat_type
        load_to_client_action_table(year_id=year_id,
                                    week_id=week_id,
                                    stat_date=stat_date,
                                    action_type=action_type,
                                    data=data)
        log("insert total " + str(total) + " records ")	


def flush_to_db():
	
	log("processing login counter ...")
        flush_to_db_by_type(login_counter,STAT_TYPE.LOGIN_CNT)

        log("processing create product counter ...")
        flush_to_db_by_type(create_product_counter,STAT_TYPE.CREATE_PD_CNT)

        log("processing upadte product counter ...")
        flush_to_db_by_type(update_product_counter,STAT_TYPE.UPDATE_PD_CNT)



if __name__=="__main__":
        """ The main pattern to process the raw nginx log
        """
       
	log("processing performance log")	
	
	# define global holder
	login_counter={}
	update_product_counter={}
	create_product_counter={}
	
	# get cache data
        sdict,cdict,udict=get_supplier_list()	

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


		comp_id=0
		check_comp_login()
		if not check_product_update() :
			check_product_create()

        
	#the end flush to db
	flush_to_db()
