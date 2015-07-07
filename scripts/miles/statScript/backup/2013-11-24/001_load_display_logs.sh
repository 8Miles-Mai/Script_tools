#!/bin/bash

#***********************************************************************
# Purpose: dump portal porduct display log to Oracle db
# Revision History:
# 2012-05-17 : Fung initialized
# 2012-11-07 : jie.zou amended for IDC environment
# 2013-05-27 : jie.zou amended for change static data source
#***********************************************************************
. gm_common.sh


# Global Variables define here:
#***********************************************************************
db_file=$DATA_DIR"/gmstat-????-??-??" 



# copy and remove data file from central storage to $DATA_DIR
#***********************************************************************
function copy_file_from_nas(){
    log "copying file from nas"

    nas_path="/app_data/logs/gmstat"

    if [ -e $nas_path/$db_file_name ] ; then
         cp $nas_path/$db_file_name $DATA_DIR -v 
    else
         error " file not found !! $nas_path/$db_file_name"
    fi
}

# remove old log file from storage before batch start, only keep 3 days' log
function remove_log_from_storage(){
    log "removing old files from storage"
    find $DATA_DIR -type f -name "gmstat*" -mtime +2 -exec rm  {} \;
}



#  Main script define here :
#***********************************************************************

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

#  loop for load many days in one batch, period=1 by default
# revice the db_file
db_file_name="gmstat-$curr_date.*"
db_file="$DATA_DIR/$db_file_name"

copy_file_from_nas

#curr_date=`date -d "$curr_date 1 day" "+%Y-%m-%d"`

if [ -s $db_file".gz" ] ; then
	log "calling python ..."
#        log $db_file".gz"
        zcat $db_file".gz" | ./001_extract_display_log_to_db.py
#        ./001_extract_display_log_to_db.py $db_file".gz"
else
	error "db file $db_file not exitst or error!"
	exit 1
fi

	


# batch job log house keeping, archive log 30 days ago
#***********************************************************************
housekeep_batch_joblog >> $script_log_file


