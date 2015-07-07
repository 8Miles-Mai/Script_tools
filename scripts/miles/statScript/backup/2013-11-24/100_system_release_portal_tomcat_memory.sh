#!/bin/bash

ports="75:8181 76:8181 77:8181"

for port in $ports ; do

 wget "http://192.168.23.$port/gmportal/dataRefresh.gm?flag=refresh" -O /dev/null -t 1 -T 10

done

