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



#***********************************************************************
# copy data file from central storage to $DATA_DIR


#  Main script define here :
#***********************************************************************
# 1. . pipe to python script 

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
    log "loading interest buylead data for $curr_date"
    ./005_extract_interest_buylead_to_db.py $curr_date

    curr_date=`date -d "$curr_date 1 day" "+%Y-%m-%d"`

done

