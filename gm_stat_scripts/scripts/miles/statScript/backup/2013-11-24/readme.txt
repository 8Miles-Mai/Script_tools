(1) Introduction

Scripts path at /app/deploy/scripts and the introduction of all scripts as below

name                          | describtion                                                          | I/O                                                       | status
*********************************************************************************************************************************************************************************
000_batch_job_enabler.sh      | The entry of batch. Kick off batch job and pass parms to batch if any| input:scripts code and parms; output:batch job log        | 
001_load_display_logs.sh      | extract product display logs from sqlite db, dump to mysql db        | input:display log; output:product show up times           | 
002_load_access_logs.sh       | extract click statistic from nginx access log file , dump to mysql db| input:access log ; output:click product times             |
003_load_performance_logs.sh  | extract mvo user action logs from tomcat AOP logs, dump to mysql db  | input:perf log; output:login times, new prod, update prod |           
004_load_inquiry.sh           | extract inquiry statistic from oracle db, dump to mysql db           | input:vw_seller_inquiries; output:inquiry statistic       |
005_load_interest_buylead.sh  | extract buying lead statistic from oracle db, dump to mysql db       | input:vw_interest_buyleads; output:buying lead statistic  |
006_load_replies.sh           | extract reply buyer statistic from oracle db, dump to mysql db       | input:vw_seller_replies; output:reply buyer statistic     |
007_cal_aggs.sh               | calculate aggregation for action and effect table                    | input:action table,effect table;output: aggs table        |


--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


(2) How to run scripts manually?

./000_batch_job_enabler.sh $scripts_code $date $period

There are 3 parms to run 000, scripts code is mandatory but date and period are optional. For 001-006, period is in day, while period is in week for 007. 
Default date is last day and default period is 1.

For example:

"./000_batch_job_enabler.sh 001 2012-04-01 30"   means run 001 batch job for 30 days' data start from 2012-04-01(i.e. 2012-04-01 ~ 2012-04-30)

"./000_batch_job_enabler.sh 007 2012-04-01 3"    means run 007 batch job for 3 weeks' data start from the week of 2012-04-01(i.e. the 14th ~ 16th week of 2012)

"./000_batch_job_enabler.sh 001"   means run 001 batch job for last day data.

"./000_batch_job_enabler.sh 007"   means run 007 batch job for the week of last day data. Generally, it's last week if run on Sunday.


--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

(3) Cron job

Crontab setting at /app/deploy/scripts/batch_cron.txt


#Run 001-006 to analysis log and DB by sequence at 6 AM HKT everyday
0  6  *  *  *  000_batch_job_enabler.sh 001;000_batch_job_enabler.sh 002;000_batch_job_enabler.sh 003;000_batch_job_enabler.sh 004;000_batch_job_enabler.sh 005;000_batch_job_enabler.sh 006

#Run 007 to calculate aggregation at 9 AM HKT every Sunday
0  9  *  *  sun  000_batch_job_enabler.sh 007


