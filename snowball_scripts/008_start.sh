#!/bin/bash


export ORACLE_HOME=/app/gmbatch/ORACLE_HOME
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$ORACLE_HOME/product/11.2.0/client_1/lib/

export ORACLE_HOME=/app/deploy/oracle_client/product/11.2.0/client_1
export LD_LIBRARY_PATH=.:$ORACLE_HOME/lib:/lib:/usr/lib:/usr/local/lib

cd /app/gmbatch/scripts/miles/snowball_scripts

./008_trade_count_comp_info.py
