echo "Loading PRODUCTION environment parms..."

export ORACLE_HOME=/app/gmbatch/ORACLE_HOME
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$ORACLE_HOME/product/11.2.0/client_1/lib/
export PYTHONPATH=/app/gmbatch/scripts
export PYTHON_EGG_CACHE=/tmp/.python-eggs


#export MYSQL_SERVER="192.168.23.234"
export MYSQL_SERVER="192.168.23.240"
export MYSQL_USER="app_wla"
export MYSQL_PASSWORD="webloganalysis"
export MYSQL_DB="web_log_analysis"


#insert result to test mysql database
#--------------------------------------------
#export MYSQL_SERVER="192.168.86.90"
#export MYSQL_USER="app_wla"
#export MYSQL_PASSWORD="webloganalysis"
#export MYSQL_DB="web_log_analysis"
#--------------------------------------------

export TODAY=`date +%Y-%m-%d`


export ORACLE_SID="\
(DESCRIPTION =(ADDRESS = (PROTOCOL = TCP)(HOST =192.168.23.239)(PORT = 1521)) \
(CONNECT_DATA = \
(SERVER = SHARED) \
(SID = core01))) \
"
export ORACLE_SERVICE="192.168.23.238:1521/core01.db.globalmarket.com"
export ORACLE_USER="app_portal_stats"
export ORACLE_PASSWORD="Stat0RLeav?YorN2"


export DATA_DIR="/app/gmbatch/data"
export LOGS_DIR="/app/gmbatch/logs"
export ARCH_DIR="/app_data/portal/logs/batch_server"
export REPORT_DIR="/app/gmbatch/report"

# to call index
#export SOLR_SRV="192.168.22.32:18080"
export SOLR_SRV="192.168.24.62:18080"


# to send email
#export SMTP_SERVER="211.150.64.59"
export SMTP_SERVER="192.168.23.8"
#export SMTP_SERVER="192.168.24.65"
export SMTP_USERNAME="sysmon@corp.globalmarket.com"
export SMTP_PASSWORD="monitor9394"
export MAIL_FROM="sysmon@corp.globalmarket.com"


#2012-07-06 1650, added by jie.zou, for task 8566
export MYGMC_ORACLE_SID="\
(DESCRIPTION =(ADDRESS = (PROTOCOL = TCP)(HOST =192.168.23.239)(PORT = 1521)) \
(CONNECT_DATA = \
(SERVER = SHARED) \
(SID = core01))) \
"
export MYGMC_ORACLE_SERVICE_NAME="core01.db.globalmarket.com"
export MYGMC_ORACLE_USER="app_mygmc"
export MYGMC_ORACLE_PASSWORD="18EAFOVPDT"


#added by jie.zou, 2012-11-07 1558, for create python environment
export ORACLE_HOME=/app/deploy/oracle_client/product/11.2.0/client_1
export LD_LIBRARY_PATH=.:$ORACLE_HOME/lib:/lib:/usr/lib:/usr/local/lib
