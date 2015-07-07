
echo "copy gmvo daily to backup begin."

cd /app/gmbatch/scripts/test/recoverdata/

#echo "copy 192.168.24.80 daily"
#scp deploy_ro@192.168.24.80:/app/deploy/tomcat/logs/gmvo /app/gmbatch/scripts/test/recoverdata/80/gmvo_`date +"%Y-%m-%d"`
#scp deploy_ro@192.168.24.80:/app/deploy/tomcat/logs/performance /app/gmbatch/scripts/test/recoverdata/80/performance_`date +"%Y-%m-%d"`
#scp deploy_ro@192.168.24.80:/app/deploy/tomcat/logs/catalina.out /app/gmbatch/scripts/test/recoverdata/80/catalina.out_`date +"%Y-%m-%d"`

#echo "copy 192.168.24.81 daily"
#scp deploy_ro@192.168.24.81:/app/deploy/tomcat/logs/gmvo /app/gmbatch/scripts/test/recoverdata/81/gmvo_`date +"%Y-%m-%d"`
#scp deploy_ro@192.168.24.81:/app/deploy/tomcat/logs/performance /app/gmbatch/scripts/test/recoverdata/81/performance_`date +"%Y-%m-%d"`
#scp deploy_ro@192.168.24.81:/app/deploy/tomcat/logs/catalina.out /app/gmbatch/scripts/test/recoverdata/81/catalina.out_`date +"%Y-%m-%d"`

#echo "copy 192.168.24.82 daily"
#scp deploy_ro@192.168.24.82:/app/deploy/tomcat/logs/gmvo /app/gmbatch/scripts/test/recoverdata/82/gmvo_`date +"%Y-%m-%d"`
#scp deploy_ro@192.168.24.82:/app/deploy/tomcat/logs/performance /app/gmbatch/scripts/test/recoverdata/82/performance_`date +"%Y-%m-%d"`
#scp deploy_ro@192.168.24.82:/app/deploy/tomcat/logs/catalina.out /app/gmbatch/scripts/test/recoverdata/82/catalina.out_`date +"%Y-%m-%d"`

#tar -jcvf /app/gmbatch/scripts/test/recoverdata/80/gmvo_`date +"%Y-%m-%d"`.tar.bz2 /app/gmbatch/scripts/test/recoverdata/80/gmvo_`date +"%Y-%m-%d"`
#tar -jcvf /app/gmbatch/scripts/test/recoverdata/80/performance_`date +"%Y-%m-%d"`.tar.bz2 /app/gmbatch/scripts/test/recoverdata/80/performance_`date +"%Y-%m-%d"`
#tar -jcvf /app/gmbatch/scripts/test/recoverdata/80/catalina.out_`date +"%Y-%m-%d"`.tar.bz2 /app/gmbatch/scripts/test/recoverdata/80/catalina.out_`date +"%Y-%m-%d"`

#rm -rf /app/gmbatch/scripts/test/recoverdata/80/gmvo_`date +"%Y-%m-%d"`
#rm -rf /app/gmbatch/scripts/test/recoverdata/80/performance_`date +"%Y-%m-%d"`
#rm -rf /app/gmbatch/scripts/test/recoverdata/80/catalina.out_`date +"%Y-%m-%d"`

#tar -jcvf /app/gmbatch/scripts/test/recoverdata/81/gmvo_`date +"%Y-%m-%d"`.tar.bz2 /app/gmbatch/scripts/test/recoverdata/81/gmvo_`date +"%Y-%m-%d"`
#tar -jcvf /app/gmbatch/scripts/test/recoverdata/81/performance_`date +"%Y-%m-%d"`.tar.bz2 /app/gmbatch/scripts/test/recoverdata/81/performance_`date +"%Y-%m-%d"`
#tar -jcvf /app/gmbatch/scripts/test/recoverdata/81/catalina.out_`date +"%Y-%m-%d"`.tar.bz2 /app/gmbatch/scripts/test/recoverdata/81/catalina.out_`date +"%Y-%m-%d"`

#rm -rf /app/gmbatch/scripts/test/recoverdata/81/gmvo_`date +"%Y-%m-%d"`
#rm -rf /app/gmbatch/scripts/test/recoverdata/81/performance_`date +"%Y-%m-%d"`
#rm -rf /app/gmbatch/scripts/test/recoverdata/81/catalina.out_`date +"%Y-%m-%d"`

#tar -jcvf /app/gmbatch/scripts/test/recoverdata/82/performance_`date +"%Y-%m-%d"`.tar.bz2 /app/gmbatch/scripts/test/recoverdata/82/performance_`date +"%Y-%m-%d"`
#tar -jcvf /app/gmbatch/scripts/test/recoverdata/82/catalina.out_`date +"%Y-%m-%d"`.tar.bz2 /app/gmbatch/scripts/test/recoverdata/82/catalina.out_`date +"%Y-%m-%d"`
#tar -jcvf /app/gmbatch/scripts/test/recoverdata/82/gmvo_`date +"%Y-%m-%d"`.tar.bz2 /app/gmbatch/scripts/test/recoverdata/82/gmvo_`date +"%Y-%m-%d"`

#rm -rf /app/gmbatch/scripts/test/recoverdata/82/gmvo_`date +"%Y-%m-%d"`
#rm -rf /app/gmbatch/scripts/test/recoverdata/82/performance_`date +"%Y-%m-%d"`
#rm -rf /app/gmbatch/scripts/test/recoverdata/82/catalina.out_`date +"%Y-%m-%d"`


scp deploy_ro@192.168.24.80:/app/deploy/tomcat/logs/catalina.out-`date +"%Y%m%d"`.gz /app/gmbatch/scripts/test/recoverdata/80/
scp deploy_ro@192.168.24.81:/app/deploy/tomcat/logs/catalina.out-`date +"%Y%m%d"`.gz /app/gmbatch/scripts/test/recoverdata/81/
scp deploy_ro@192.168.24.82:/app/deploy/tomcat/logs/catalina.out-`date +"%Y%m%d"`.gz /app/gmbatch/scripts/test/recoverdata/82/
#20140701


#scp deploy_ro@192.168.24.80:/app/deploy/tomcat/logs/catalina.out-20140628.gz /app/gmbatch/scripts/test/recoverdata/80/
#scp deploy_ro@192.168.24.81:/app/deploy/tomcat/logs/catalina.out-20140628.gz /app/gmbatch/scripts/test/recoverdata/81/
#scp deploy_ro@192.168.24.82:/app/deploy/tomcat/logs/catalina.out-20140628.gz /app/gmbatch/scripts/test/recoverdata/82/

#scp deploy_ro@192.168.24.80:/app/deploy/tomcat/logs/catalina.out-20140629.gz /app/gmbatch/scripts/test/recoverdata/80/
#scp deploy_ro@192.168.24.81:/app/deploy/tomcat/logs/catalina.out-20140629.gz /app/gmbatch/scripts/test/recoverdata/81/
#scp deploy_ro@192.168.24.82:/app/deploy/tomcat/logs/catalina.out-20140629.gz /app/gmbatch/scripts/test/recoverdata/82/

#scp deploy_ro@192.168.24.80:/app/deploy/tomcat/logs/catalina.out-20140630.gz /app/gmbatch/scripts/test/recoverdata/80/
#scp deploy_ro@192.168.24.81:/app/deploy/tomcat/logs/catalina.out-20140630.gz /app/gmbatch/scripts/test/recoverdata/81/
#scp deploy_ro@192.168.24.82:/app/deploy/tomcat/logs/catalina.out-20140630.gz /app/gmbatch/scripts/test/recoverdata/82/
#cp /app_data/logs/gmvo01/gmvo_2014-06-24.log.bz2 /app/gmbatch/scripts/test/recoverdata/80/
#cp /app_data/logs/gmvo02/gmvo_2014-06-24.log.bz2 /app/gmbatch/scripts/test/recoverdata/81/
#cp /app_data/logs/gmvo03/gmvo_2014-06-24.log.bz2 /app/gmbatch/scripts/test/recoverdata/82/

#cp /app_data/logs/gmvo01/gmvo_2014-06-25.log.bz2 /app/gmbatch/scripts/test/recoverdata/80/
#cp /app_data/logs/gmvo02/gmvo_2014-06-25.log.bz2 /app/gmbatch/scripts/test/recoverdata/81/
#cp /app_data/logs/gmvo03/gmvo_2014-06-25.log.bz2 /app/gmbatch/scripts/test/recoverdata/82/

#cp /app_data/logs/gmvo01/gmvo_2014-06-26.log.bz2 /app/gmbatch/scripts/test/recoverdata/80/
#cp /app_data/logs/gmvo02/gmvo_2014-06-26.log.bz2 /app/gmbatch/scripts/test/recoverdata/81/
#cp /app_data/logs/gmvo03/gmvo_2014-06-26.log.bz2 /app/gmbatch/scripts/test/recoverdata/82/



echo "copy gmvo daily to backup end."
