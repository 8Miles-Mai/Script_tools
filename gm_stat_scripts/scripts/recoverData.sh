#/bin/bash

#***********************************************************************
# Purpose: recover 005 data from 2012-04-01 to 2014-07-01
# 2014-07-28 : Miles.Mai initialized
#***********************************************************************



cd `dirname $0`

#. gm_common.sh

#fromDay="2014-04-01"
#toDay="2014-07-01"

#fromDay="2014-01-01"
#toDay="2014-04-01"

#fromDay="2013-07-01"
#toDay="2014-01-01"

#fromDay="2013-01-01"
#toDay="2013-07-01"

#fromDay="2014-07-29"
#toDay="2014-08-04"

fromDate=`date -d "$fromDay" +"%Y-%m-%d"`
toDate=`date -d "$toDay" +"%Y-%m-%d"`

echo "Start date: $fromDate"
echo "End date: $toDate"

while [ "$fromDate" != "$toDate" ]
do
	echo "Dealing date: $fromDate"
	./000_batch_job_enabler.sh 002 "$fromDate"
	fromDate=`date -d "$fromDate +1 day" +"%Y-%m-%d"`
done

echo "end of script"

