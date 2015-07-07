#!/bin/bash

#***********************************************************************
# Purpose: get promotion product status from mongodb and save promotion product status to oracle
# Revision History:    2013-11-09    Jie created
#***********************************************************************

. gm_common.sh


# Global Variables define here:
#***********************************************************************



# Global Function define here:
#***********************************************************************





#  Main script define here :
#***********************************************************************

if [ "$1" == "" ] ; then
    export curr_date=`get_last_day_str`
else
    export curr_date="$1"
fi

log "calling python ..."
log "loading promotion data from mongodb for $curr_date"
#./008_set_promotion_product_status_to_db.py $curr_date


