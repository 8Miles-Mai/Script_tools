#!/bin/bash

#***********************************************************************
# Purpose: send inquiry edm
# Revision History:
# 2015-04-08 : Miles.Mai initialized
#***********************************************************************
. gm_common.sh

#  Main script define here :
#***********************************************************************


cd /app/gmbatch/scripts/
./012_extract_inquiry_for_edm.py
