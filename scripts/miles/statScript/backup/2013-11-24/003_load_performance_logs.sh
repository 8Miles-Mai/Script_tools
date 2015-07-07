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
		for j in 1 2 3 ; do
			k=`expr $j + 4`
			cp "$src_dir/gmvo0${j}/performance_${curr_date}.log.tar.gz" "$DATA_DIR/performance_${curr_date}.t${k}log.tar.gz" -v
		done
		
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
remove_log_from_storage


#  loop for load many days in one batch, period=1 by default
for((j=0;j<period;j++));
do

#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130701.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130702.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130703.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130704.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130705.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130706.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130707.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130708.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130709.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130710.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130711.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130712.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130713.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130714.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130715.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130716.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130717.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130718.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130719.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130720.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130721.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130722.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130723.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130724.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130725.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130726.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130727.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130728.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130729.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130730.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130731.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130801.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130802.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130803.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130804.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130805.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130806.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130807.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130808.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130809.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130810.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130811.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130812.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130813.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130814.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130815.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130816.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130817.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130818.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130819.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130820.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130821.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130822.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130823.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130824.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130825.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130826.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130827.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130828.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130829.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130830.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130831.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130901.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130902.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130903.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130904.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130905.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130906.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130907.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130908.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130909.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130910.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130911.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130912.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130913.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130914.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130915.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130916.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130917.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130918.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130919.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130920.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130921.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130922.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130923.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130924.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130925.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130926.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130927.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#zcat /app/gmbatch/scripts/test/recoverdata/*/catalina.out-20130928.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py



#log "date: ${curr_date}"

#	copy_file_from_nas
#	log_files=""
#	for log_file in $DATA_DIR/performance_${curr_date}.*; do
#		log_files="$log_files $log_file"
#	done
#	log "procesing file : $log_files"
#	zcat $log_files | strings | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py
#	curr_date=`date -d "$curr_date 1 day" "+%Y-%m-%d"`


currDate=`date +"%Y%m%d"`
echo "$currDate"

zcat /app_data/logs/gmvo0*/catalina.out-$currDate.gz | grep "compId-"  | grep "START" | ./003_extract_performance_log_to_db.py


done

