echo "Loading PRODUCTION environment parms..."


#---------------------------
# Common Config 
#---------------------------
export ORACLE_HOME=/app/gmbatch/ORACLE_HOME

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$ORACLE_HOME/product/11.2.0/client_1/lib/
export PYTHONPATH=/app/gmbatch/scripts
export PYTHON_EGG_CACHE=/tmp/.python-eggs

export TODAY=`date +%Y-%m-%d`



#---------------------------
# DataBase Link Config 
#---------------------------
# 1. oracle config 

export ORACLE_SID="(DESCRIPTION =(ADDRESS = (PROTOCOL = TCP)(HOST =192.168.23.239)(PORT = 1521)) (CONNECT_DATA =(SERVER = SHARED)(SID = core01)))"
export ORACLE_SERVICE="192.168.23.238:1521/core01.db.globalmarket.com"
export ORACLE_USER="app_portal_stats"
export ORACLE_PASSWORD="Stat0RLeav?YorN2"

#added by jie.zou, 2012-11-07 1558, for create python environment
export ORACLE_HOME=/app/deploy/oracle_client/product/11.2.0/client_1
export LD_LIBRARY_PATH=.:$ORACLE_HOME/lib:/lib:/usr/lib:/usr/local/lib


# 2. mysql config 

# insert result to prd mysql database
#export MYSQL_SERVER="192.168.23.240"
export MYSQL_SERVER="192.168.86.230"
export MYSQL_USER="app_wla"
export MYSQL_PASSWORD="webloganalysis"
export MYSQL_DB="web_log_analysis"

#insert result to test mysql database
#export MYSQL_SERVER="192.168.86.90"
#export MYSQL_USER="app_wla"
#export MYSQL_PASSWORD="webloganalysis"
#export MYSQL_DB="web_log_analysis"


# 3. solr config 

#export SOLR_SRV="192.168.22.32:18080"
export SOLR_SRV="192.168.24.56:18080"

# 4. mongodb config 

#added by jie.zou, 2013-11-08 1004, add new mongodb config
export MDB_SERVER="192.168.86.51"
export MDB_PORT=27017
export MDB_USER="test"
export MDB_PASSWORD="test"
export MDB_DATABASE_NAME="promotions"
export MDB_PROMOTION_COLLECTION_NAME="promotions"



#---------------------------
# Log File Config 
#---------------------------
export DATA_DIR="/app/gmbatch/data"
export LOGS_DIR="/app/gmbatch/logs"
export ARCH_DIR="/app_data/portal/logs/batch_server"
export REPORT_DIR="/app/gmbatch/report"



#---------------------------
# Send Email Config 
#---------------------------
#export SMTP_SERVER="211.150.64.59"
#export SMTP_SERVER="192.168.24.65"
export SMTP_SERVER="smtp.globalmarket.com"
export SMTP_USERNAME="sysmon@corp.globalmarket.com"
export SMTP_PASSWORD="monitor9394@01%"
export MAIL_FROM="sysmon@corp.globalmarket.com"




