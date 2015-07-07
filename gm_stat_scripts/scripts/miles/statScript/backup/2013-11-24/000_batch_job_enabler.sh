#/bin/bash

#***********************************************************************
# Purpose: kick off other shell script by script code
# Revision History:
# 2012-05-21 : Fung initialized
# 2012-07-10 : jie.zou added myGMC statistics model
#***********************************************************************



cd `dirname $0`

. gm_common.sh

# get parameters from command line
# param 1, script code
# param 2, parameters to the main shell, the start date of the batch, last day by default
# param 3, parameters to the main shell, the period of the batch, 1 day by default. 
# e.g. for 001-006 "001 2012-05-01 30" means load 001 job for 30 DAYS start from 2012-05-01
#      for 007, "007 2012-05-01 4" means run 007 to calculate for 4 WEEKS start from the WEEK of date 2012-05-01 
#      for 010-014 "010 2012-05-01 30" means load 010 job for 30 DAYS start from 2012-07-10
#***********************************************************************
export script_code=$1
export script_param1=$2
export script_param2=$3

# get main shell script by code
#***********************************************************************
export script_name=`ls $script_code*.sh`

if [ ! -e "$script_name" ] ; then
	echo "!!!! SCRIPT NOT FOUND FOR SCRIPT CODE : $script_code"
	exit 1
fi

# create log file as script_code+timestamp.log
#***********************************************************************
timestamp=`time_now`

#amended by jie.zou, 2012-11-06, modify python log file path for IDC environment 
export script_log_file="/app/gmbatch/logs/${script_code}_$timestamp.log"
echo "Please check the log file $script_log_file"


# print script header
#***********************************************************************
print_log_header >> $script_log_file

# remove the old dict files, only keep recent 3 days
#***********************************************************************
remove_dict_files >> $script_log_file



# check lock file 
#***********************************************************************
# TO-DO

# create lock file 
#***********************************************************************
# TO-DO


# the most important line to kick off the main shell
#***********************************************************************
/bin/bash $script_name $script_param1 $script_param2 >> $script_log_file 


export script_return_flag=$?

# print log footer, summerization
#***********************************************************************
print_log_footer >> $script_log_file


# send email notification
#***********************************************************************
send_email >> $script_log_file
