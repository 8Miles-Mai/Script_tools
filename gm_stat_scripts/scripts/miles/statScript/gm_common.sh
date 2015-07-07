. env.sh


#---------------------------
# Log Function 
#---------------------------
function log(){
   time=`date +"%Y-%m-%d %H:%M:%S"`
   echo "LOG $time : $1" 
}
function info(){
   time=`date +"%Y-%m-%d %H:%M:%S"`
   echo "IFO $time : $1"
}
function error(){
   time=`date +"%Y-%m-%d %H:%M:%S"`
   echo "ERR $time : $1"
}



#---------------------------
# Time Function 
#---------------------------
function time_now(){
   time=`date +"%Y-%m-%d_%H%M%S"`
   echo "$time"
}
function date_now(){
   date=`date +"%Y-%m-%d"`
   echo "$date"
}
function get_last_day_str(){
   time=`date -d "last day" +"%Y-%m-%d"`
   echo "$time"
}



#---------------------------
# File Function 
#---------------------------
function remove_dict_files(){
   find $DATA_DIR -type f -name "CKPT_*" -mtime +2 -exec rm  {} \;
   log "Removed dict files 3 days ago."
}
function housekeep_batch_joblog(){
   time=`date +"%Y%m%d%H%M%S"`
   logFileNum=`find $LOGS_DIR -type f -name "00*.log" -mtime +30| wc -l`
   if [ $logFileNum -eq "0" ]; then
   		log "No log need to be housekeep."
   else
   		find $LOGS_DIR -type f -name "00*.log" -mtime +30 |cpio -o --format=ustar |gzip > $ARCH_DIR/batch_log_arch_$time.tar.gz
		find $LOGS_DIR -type f -name "00*.log" -mtime +30 -exec rm  {} \;
		log "$logFileNum batch job log files housekeeping completed."
   fi		

}



#---------------------------
# Email Function 
#---------------------------
function print_log_header(){
    t_start_time=`date +%s`	
	log "================================================================================================"
	log "Batch job code: $script_code"
	log "Batch job script name: $script_name"
	log "Batch job parameters: $script_param"
	t_host_name=`hostname`
	log "Run on host: $t_host_name"
	log "Log file name: $script_log_file"
	log "================================================================================================"
}
function print_log_footer(){
	t_end_time=`date +%s`
    t_elapsed=`expr $t_end_time - $t_start_time`	
	log "================================================================================================"
	log "Return flag: $script_return_flag"
	log "Time elapsed: $t_elapsed"
	log "================================================================================================"
}
function send_email(){
	./000_email_api.py $script_code $script_log_file
}



