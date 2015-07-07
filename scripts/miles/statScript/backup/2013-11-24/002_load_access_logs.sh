#!/bin/bash

#***********************************************************************
# Purpose: dump portal access log to Oracle db
# Revision History:
# 2012-05-18 : Fung initialized
# 2012-11-22 : jie.zou, added HK access.log 
# 2013-03-06 : jie.zou, copy log file from '../web01/..','../web02/..','../web03/..'
#***********************************************************************

. gm_common.sh

# Global Variables define here:
#***********************************************************************
log_file=$DATA_DIR"/access_yyyymmdd.log.bz2"
hk_log_file=$DATA_DIR"/hk_access_yyyymmdd.log.bz2"


# Global Function define here:
#***********************************************************************
# get working access log file from starage to local working folder

function copy_file_from_nas(){
    log "copy_file_from_nas"

    #amended by jie.zou, 2012-11-07 1610, modify log file path for IDC environment
#    log_dir="/app_data/portal/logs/web01/nginx_logs"
#    if [ -e "$log_dir/$log_file_name" ] ; then
#	cp "$log_dir/$log_file_name" $DATA_DIR -v
#    else=
#	error "No this log file $log_dir/$log_file_name"
#    fi 

    #amended by jie.zou, 2013-03-06 1214, copy log file from '../web01/..','../web02/..','../web03/..'
    for i in 1 2 3 ; do 
        log_dir="/app_data/portal/logs/web0${i}/nginx_logs"
        if [ -e "$log_dir/$log_file_name.log.bz2" ] ; then
           cp "$log_dir/$log_file_name.log.bz2" $DATA_DIR/$log_file_name.t${i}log.bz2 -v
        else=
           error "No this log file $log_dir/$log_file_name.t${i}.log.bz2"
        fi
    done

}


#amended by jie.zou, 2012-11-22 0840, added hk log file 
function copy_hk_file_from_nas(){
    log "copy_hk_file_from_nas"

    hk_log_dir="/app_data/portal/logs/hk_web01"

    if [ -e "$hk_log_dir/$hk_log_file_name" ] ; then
	cp "$hk_log_dir/$hk_log_file_name" "$DATA_DIR/hk_$hk_log_file_name" -v
    else
	error "No this log file $hk_log_dir/$hk_log_file_name"
    fi
}



# remove old log file from storage before batch start
function remove_log_from_storage(){
    log "removing old files from storage"
    find $DATA_DIR -type f -name "*access_*" -mtime +2 -exec rm  {} \;
}


#  Main script define here :
#***********************************************************************
# 1. get log file 
# 2  cat log file , pipe to python script 

if [ "$1" == "" ] ; then
        export curr_date=`get_last_day_str`
else
        export curr_date="$1"
fi


if [ "$2" == "" ] ; then
	export period=1
else
	export period="$2"
fi	

#clean storage for download new log
remove_log_from_storage

#  loop for load many days in one batch, period=1 by default, copy files
for((j=0;j<period;j++));
do

	dstr=`echo $curr_date | sed 's/\-//g'`


	#amended by jie.zou, 2012-11-22 0840, added hk log file 
	hk_log_file_name="access_${dstr}.log.bz2"
	hk_log_file="$DATA_DIR/$log_file_name"

	copy_hk_file_from_nas


	# revice the db_file
#	log_file_name="access_${dstr}.log.bz2"
#amended by jie.zou, 2013-03-06 1214, copy log file from '../web01/..','../web02/..','../web03/..'
	log_file_name="access_${dstr}"
	log_file="$DATA_DIR/$log_file_name"

	copy_file_from_nas 

	log "filename: "+$DATA_DIR/*access_${dstr}.*log.bz2
        bzcat $DATA_DIR/*access_${dstr}.*log.bz2 | ./002_extract_access_log_to_db.py

	curr_date=`date -d "$curr_date 1 day" "+%Y-%m-%d"`

done






