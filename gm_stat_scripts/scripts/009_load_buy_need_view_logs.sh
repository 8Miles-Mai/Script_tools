#!/bin/bash

#***********************************************************************
# Purpose: get and set seller BL left view time and modify BL offline/online status 
# Revision History:    2013-11-09    Jie Created
#***********************************************************************

. gm_common.sh


# 1.pipe to python script 

if [ "$1" == "" ] ; then
    export curr_date=`get_last_day_str`
else
    export curr_date="$1"
fi

log "calling python ..."
#log "get and set BL left view time"
#./009_set_buy_need_limit_times_to_db.py $curr_date

log "make temp offline BL status as online"
./009_set_buy_need_status_to_db.py

