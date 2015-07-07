#!/bin/bash

#***********************************************************************
# Purpose: dump portal performance log to Oracle db
# Revision History:
# 2012-05-18 : Fung initialized
#***********************************************************************

. gm_common.sh

# Global Variables define here:
#***********************************************************************
log_files="$DATA_DIR/performance_yyyy-mm-dd.log.tar.gz.t?? $DATA_DIR/performance_yyyy-mm-dd.log.tar.gz.t??"


# Global Function define here:
#***********************************************************************
# get working performace log file from starage, to local working folder
# There are 4 pices of logs file, all are needed
function copy_file_from_nas(){
    log "to-do copying file from storage server"
    src_dir="/app_data/portal/logs"

    if [ -e "$src_dir" ] ; then

#amended by jie.zou, 2012-11-07 1622, modify variable for IDC environment
        for i in 1 2 3 ; do 
            cp "$src_dir/app0${i}/performance_${curr_date}.log.tar.gz" "$DATA_DIR/performance_${curr_date}.t${i}log.tar.gz" -v
        done

#amended by jie.zou, 2012-11-07 1622, modify variable for IDC environment
#        for j in 1 2 3 ; do
#            k=`expr $j + 4`
#            cp "$src_dir/gmvo0${j}/performance_${curr_date}.log.tar.gz" "$DATA_DIR/gmvo_${curr_date}.t${k}log.tar.gz" -v
#        done

    fi
}

# remove old log file from storage before batch start
function remove_log_from_storage(){
    log "removing old files from storage"
    find $DATA_DIR -type f -name "performance_*" -mtime +2 -exec rm  {} \;
}


#  Main script define here :
#***********************************************************************
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
#remove_log_from_storage


#  loop for load many days in one batch, period=1 by default
for((j=0;j<period;j++));
do

#log "date: ${curr_date}"

#    copy_file_from_nas
#    log_files=""
#    for log_file in $DATA_DIR/performance_${curr_date}.*; do
#        log_files="$log_files $log_file"
#    done
#    log "procesing file : $log_files"
#    zcat $log_files | strings | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#    curr_date=`date -d "$curr_date 1 day" "+%Y-%m-%d"`



currDate=`date +"%Y%m%d"`
#currDate=20131218
#currDate=20140627


echo "$currDate"


#zcat /app_data/logs/gmvo0*/catalina.out-20131126.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/8*/catalina.out-20131206.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/8*/catalina.out-20131207.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/8*/catalina.out-20131208.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/8*/catalina.out-20131209.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/8*/catalina.out-20131210.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/8*/catalina.out-20131211.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/8*/catalina.out-20131212.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py

#bzcat 

#zcat /app_data/logs/gmvo0*/catalina.out-$currDate.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py

zcat /app/gmbatch/scripts/test/recoverdata/8*/catalina.out-$currDate.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py

#bzcat /app/gmbatch/scripts/test/recoverdata/8*/catalina.out-$currDate.log.bz2 | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py


done

