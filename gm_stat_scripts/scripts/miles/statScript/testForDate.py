#!/usr/local/bin/python

import MySQLdb 
#import cx_Oracle            
import pymongo     
import os      
import json      
import urllib2 
import urllib 
from datetime import *
from pysqlite2 import dbapi2 as sqlite
import sys

def get_date_str():
    now=datetime.now()
    return now.strftime("%Y-%m-%d")

def get_curr_date():        
    if os.environ.has_key("curr_date") :
        return os.environ["curr_date"]
    else :     
        return get_date_str()

def get_curr_week_no_no():
	return int(datetime.strptime(get_curr_date(),"%Y-%m-%d").strftime("%U"))+1


if __name__=="__main__":                      
    """ The main pattern to process the raw nginx log """

#    log("processing performance log")

    wk = get_curr_week_no_no()
              
	print "12321"
