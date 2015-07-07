#!/bin/bash

#***********************************************************************
# Purpose: dump portal porduct display log to Oracle db
# Revision History:
# 2012-05-17 : Fung initialized
#***********************************************************************

. gm_common.sh


# Global Variables define here:
#***********************************************************************



# Global Function define here:
#***********************************************************************





#  Main script define here :
#***********************************************************************
# 1.pipe to python script 

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

#  loop for load many days in one batch, period=1 by default
for((j=0;j<period;j++));
do

	log "calling python ..."
	log "calculate aggregation for the WEEK of date $curr_date"
	./007_cal_aggs_for_db.py $curr_date
	curr_date=`date -d "$curr_date 1 week" "+%Y-%m-%d"`
	
done


