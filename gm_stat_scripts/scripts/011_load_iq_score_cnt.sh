#!/bin/bash

#***********************************************************************
# Purpose: count iq_score from oracle
# Revision History:
# 2014-10-11 : Miles.Mai initialized
#***********************************************************************
. gm_common.sh

#  Main script define here :
#***********************************************************************

./011_extract_iq_score_cnt.py

# batch job log house keeping, archive log 30 days ago
#***********************************************************************
housekeep_batch_joblog >> $script_log_file


