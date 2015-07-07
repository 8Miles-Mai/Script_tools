#!/usr/bin/python

import pymongo

url = "mongodb://192.168.86.180:27017/tracker_db"
user_name = "tracker_ro"
password = "reader"

def get_product_daily_clk_cnt():

	connection = pymongo.MongoClient(host=url, safe=True, read_preference=pymongo.ReadPreference.SECONDARY)

	connection.admin.authenticate(user_name, password)
	db = connection.tracker_db

	#db.authenticate("tracker_ro", "reader")
	#print "1"
	query = {"data_queue.evt": "EXP", "$or": [
			{"data_queue.MP": {"$exists": "true"}}
        	],
            		"date": {"$gt": "2014-06-01", "$lt": "2014-06-02"}
        	};

	cnt = {}
	cursor = db.logs.find(query,{"date":1, "data_queue":1})
	#return cursor
	#print "2"
	index = 0
	for doc in cursor:
		#print "3"
		data_queue = doc["data_queue"]
		for d in data_queue:
			isExp = False
			objType = ""
			for key in d:
				if key == "evt":
					if d[key] == "EXP":
						isExp = True
				else:
					objType = key
			if not isExp:
				#print "4"
				continue
			#print objType
			if not (objType == "MP"):
				#print "5"
				#print objType
				continue

			date = doc["date"][:10]
			#print date
			if cnt.get(date, '') == '':
				cnt.setdefault(date, {})

			date_dict = cnt[date]
			obj_data = d[objType]
			#print(objType)
			for obj in obj_data:
				sid = obj.get("sid", '')
				if sid == '':
					#print "6"
					break
				index += 1
				if date_dict.get(sid, '') == '':
					date_dict.setdefault(sid, 1)
				else:
					date_dict[sid] += 1

	connection.close()
	print index
	return cnt

if __name__ == '__main__':
	click_cnt = get_product_daily_clk_cnt()
	f = open("out.txt", "w")
	print >> f, click_cnt
	f.close()

