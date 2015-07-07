

curr_date=`date +"%Y%m%d"`
echo "$curr_date"


scp deploy_ro@192.168.24.80:/app/deploy/tomcat/logs/catalina.out-$curr_date.gz /app/gmbatch/scripts/test/recoverdata/80/
scp deploy_ro@192.168.24.81:/app/deploy/tomcat/logs/catalina.out-$curr_date.gz /app/gmbatch/scripts/test/recoverdata/81/
#scp deploy_ro@192.168.24.82:/app/deploy/tomcat/logs/catalina.out-$curr_date.gz /app/gmbatch/scripts/test/recoverdata/82/
scp deploy_ro@192.168.24.80:/app/deploy/tomcat/logs/jie/82/catalina.out-$curr_date.gz /app/gmbatch/scripts/test/recoverdata/82/





