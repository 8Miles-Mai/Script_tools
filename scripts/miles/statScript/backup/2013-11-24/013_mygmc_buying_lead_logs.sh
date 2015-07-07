#!/bin/bash

#***********************************************************************
# Purpose: kick off other shell script by script code
# Revision History:
#   2012-07-06 : jie.zou  added myGMC statistic for task 8566
#***********************************************************************

. gm_common.sh

# Defined Global Variables:
#---------------------------------------------------------------------------------------------------------------
log_files="$DATA_DIR/mygmc#yyyymmdd#0.txt.bz2"


# Define Global Function:
#---------------------------------------------------------------------------------------------------------------
# get working performace log file from starage, to local working folder

function copy_file_from_nas(){
        log "to-do copying file from storage server"
        src_dir="/app_data/portal/logs/mygmcapp01"
        if [ -e "$src_dir" ] ; then
                cp "$src_dir/mygmc#${curr_date}#0.txt.bz2" "$DATA_DIR/mygmc#${curr_date}#0.txt.bz2" -v
        fi
}

function remove_log_from_storage(){
    log "removing old files from storage"
    find $DATA_DIR -type f -name "mygmc#*" -mtime +2 -exec rm  {} \;
}


#  Main Script Progress:
#---------------------------------------------------------------------------------------------------------------
# 1. get log file 
# 2  cat log file , grep the compId-xxxx pattern , pipe to python script


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
for((j=0;j<period;j++));
do
		curr_date=`date -d "$curr_date 0 day" "+%Y%m%d"`

#        copy_file_from_nas

        log_files=""

        for log_file in $DATA_DIR/mygmc#${curr_date}#0.*; do
                log_files="$log_files $log_file"
        done

        log "procesing file : $log_files"
		curr_date=`date -d "$curr_date 0 day" "+%Y-%m-%d"`

        bzcat $log_files | grep "BuyingLSearchController.getBuyingLeadBaseInfo" | grep "compId" | ./013_mygmc_buying_lead_to_db.py

        curr_date=`date -d "$curr_date 1 day" "+%Y%m%d"`

done

