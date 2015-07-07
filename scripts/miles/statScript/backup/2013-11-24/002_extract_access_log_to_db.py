#!/usr/local/bin/python

import re
from gm_common import * 


def check_robot():
	""" check against the agent, differential all type of robot
	"""
        #print user_agent 
	global robot_type
	if "Googlebot" in user_agent:
		robot_type="google"
        elif "Baiduspider" in user_agent:
		robot_type="baidu"	  
	elif "Sosospider" in user_agent:
		robot_type="soso"
        elif "bingbot" in user_agent:
		robot_type="bing"
        elif re.search("AhrefsBot|spider|YandexBot|crawler|JianKongBao",user_agent) :
		rebot_type="othrcrwler" 


def check_server():
       """ differential server by server name
       """
       global server_type 
       if "www.globalmarket.com" == server_name :
		server_type="portal"
       elif "gmc.globalmarket.com" in server_name :
		server_type="subsite"
       elif re.search("(newimg|static).globalmarket.com",server_name) : 
	        server_type="newimg"		

       
def check_response_code():
	""" differential response code 
	"""
	global code_type
	code=int(response_code)
	if (300 <= code < 400) :
		code_type="3xx"
	elif (400 <= code < 500) :
		code_type="4xx"
        elif (503 == code ) :
		code_type="LMT"
	elif (500 <= code < 600) :
		code_type="5xx"
	else :
		code_type = "200"


def check_request_type() :
	""" check if it's
	    1. *.gm interactive
            2. .html
            3. static : js|css|jpg...
	    4. cgi py
        """
	global request_type
        if re.search(".com[\S]+[^/.]+(\.gm[^c]*)",request_url) :
                request_type="itractve"
        elif re.search("/[^/.]+(\.html)",request_url) :
                request_type="html"
        elif re.search("/[^/]+(\.js|\.css|\.bmp|\.png|\.jpg|\.gif|\.swf|\.ico|\.txt)",request_url) :
                request_type="static"
        elif re.search("/[^/.]+(\.py)",request_url) :
                request_type="cgi"
        elif re.search(".globalmarket.com/(\?[^?]*)?$",request_url) :
                request_type="homepage"
        else :
                request_type="unknwurl"


def flush_to_db():
	"""
	   write to db:
    """
	data=[]
	total=0
	for key in prod_click_counter:
		if sdict.has_key(key) :
			if cdict.has_key(sdict[key]) :
				item = effect_log()
				item.entity_source=STAT_TYPE.ENT_SRC_PRD
				item.entity_id=key
				item.comp_id=sdict[key]
				item.counter=prod_click_counter[key]
				item.ind_group_id=cdict[item.comp_id]
				data.append(item)
				total=total+1
	year_id=get_curr_year_no()
	week_id=get_curr_week_no()
	stat_date=get_curr_date()
	stat_type=STAT_TYPE.CLICK_CNT
	load_to_client_effect_table(year_id=year_id,
				    			week_id=week_id,
				    			stat_date=stat_date,
				    			stat_type=stat_type,
				    			data=data)
	log("insert total " + str(total) + " records")		
	return True;


def get_product_id():
	product_pattern="http://www.globalmarket.com/product-info/.*-([\d]*).html"
        m=re.search(product_pattern,request_url)
	if m :
		return m.group(1)


def get_gmc_name():
	url_pattern="(.*).gmc.globalmarket.com"
        m=re.search(url_pattern,server_name)
	if m :
		return m.group(1)	


def add_prod_counter(pid):
	global prod_click_counter
        if prod_click_counter.has_key(pid):
		 p=prod_click_counter[pid]
		 prod_click_counter[pid]=p+1
	else:
		 prod_click_counter[pid]=1
		 

if __name__=="__main__":
        """ The main pattern to process the raw nginx log
        """
	# restore cache data
	sdict,cdict,udict=get_supplier_list()

	# all product counter holder
	prod_click_counter={}

	# line processing counter 	
	counter = 1
	    
	code_types=["200","3xx","4xx","5xx","LMT"]
	server_types=["others","portal","subsite","newimg"]
	robot_types=["organic","google","baidu","soso","bing","othrcrwler"]
	request_types=["html","itractve","static","homepage","unknwurl","cgi"]

        main_pattern='([\d.]+)(, ([\d.]+))* ([\d.]+) - - \[([^\]]+)]\[([^\]]+)]"([A-Z]+) ([\S]+) ([\S]+)" ([0-9]+) ([0-9]+)"([\S]+)" "([^\"]+)" "([^\"]+)" "([\d.]+) ([^\"]+)" "([^\"]+)" "([^\"]+)"'	
	log("Processing input string...")          	
        while True:
	    
	    # default type defines here 
	    code_type="200"  # 3xx , 4xx, 5xx
	    server_type="others" # portal, subsite
            robot_type="organic" # google , baidu, soso ,bing, other spider
            request_type="html" # interactive, cgi, static,unknown
	    request_uri =""
            
            # read line from command line pipeline
	    line = sys.stdin.readline()
	    
	    if not line : 
		log("total line: %d" % counter )
	        break	
	    
	    # print line number after every 500,000 lines, indicates the progress.
	    counter = counter + 1
	    if counter % 500000 == 0 : 
		log("line: %d" % counter )

	    # search the pattern 
	    m=re.search(main_pattern,line)
            if m :

		# 1. break the line into fields here
		client_ip=m.group(1)
                access_time=m.group(5)
		server_name=m.group(6)
                http_method=m.group(7)
                request_url=m.group(8)
                http_protocal=m.group(9)
                response_code=m.group(10)
		body_size=m.group(11)
		cache_status=m.group(14)
		referer=m.group(12)
	        user_agent=m.group(13)
	        upstream_time=m.group(15)
	        upstream_server=m.group(16)
                chinacdn=m.group(17)
		akacdn=m.group(18)	         

		request_time = re.search(":([\d]{2}:[\d]{2}:[\d]{2})",access_time).group(1)	

		# 2. call checker 
		check_robot()
		check_server()
		check_response_code()
		check_request_type()
	        
                # 3. we only count the 200 code and not robot visitors		
		if code_type == "200" and robot_type == "organic" :     
			# 3.1 if subsite visting , add to companies counter directory
			#if server_type == "subsite" :
			#	gmcname=get_gmc_name()
			#	if gmcname :
			#		if udict.has_key(gmcname) :
			#			comp_id=udict[gmcname]
			#			add_counter(comp_id)
			
			# 3.2 if portal visiting , and it's visiting the product-info page, 
			# get the comp_id from product_id
			# and add to product conters
			if server_type == "portal" :
				pid=get_product_id()
				if pid :
					if sdict.has_key(pid) :
						add_prod_counter(pid)

	#At the end , flush to db
	flush_to_db()	
