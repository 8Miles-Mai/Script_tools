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
			select client_id,product_id,count(1),inq_for 
			from gm_stats.vw_client_inq_items 
			where client_recv_time > to_date('""" + curr_date + """','yyyy-mm-dd')  
			and  client_recv_time < to_date('""" + curr_date + """', 'yyyy-mm-dd')+1  
			group by client_id, product_id, inq_for
		   """

	oraConn=get_oracle_conn()
	oraCurr=oraConn.cursor()
	for oraRs in oraCurr.execute(oraSql):
		
		comp_id=str(oraRs[0])
		prod_id=oraRs[1]
		counter=oraRs[2]
		inq_for=oraRs[3]
		
		
		# make sure we have ind_group_id
		if cdict.has_key(comp_id):
			item_arr=[]
			item_arr.append(comp_id)
			item_arr.append(prod_id)
			item_arr.append(counter)
			item_arr.append(inq_for)
			inquiry_counter[comp_id]=item_arr
			
			
			

	oraConn.close()

	# At the end flush to db 
	flush_to_db()
