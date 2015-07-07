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
			select client_id,count(1) from gm_stats.vw_client_im_replies 
			where first_reply_time > to_date('""" + curr_date + """','yyyy-mm-dd')  
			and  first_reply_time < to_date('""" + curr_date + """', 'yyyy-mm-dd')+1  
			group by client_id
			"""

	oraConn=get_oracle_conn()
	oraCurr=oraConn.cursor()
	total=0
	for oraRs in oraCurr.execute(oraSql):
		
		comp_id=str(oraRs[0])
		counter=oraRs[1]

		item_arr=[]
		item_arr.append(comp_id)
		item_arr.append(counter)

		
		# make sure we have ind_group_id
		if cdict.has_key(comp_id):
			replies_counter[comp_id]=item_arr
				
	oraConn.close()
	

	# At the end flush to db 
	flush_to_db()
