URL=http://192.168.86.23:8080/hudson/user/gmmiles/my-views/view
DO=build?delay=0sec

echo $1 $2

view=`awk -F '[",]' '/'$1'/{print $4}' views.config`
job=`awk -F '[",]' '/'$2'/{print $4}' jobs.config`

echo view=$view
echo job=$job

do_url=$URL/$view/job/$job/$DO

open $do_url

#open http://192.168.86.23:8080/hudson/user/gmmiles/my-views/view/sit_deploy/job/snowball_sit_sub_soa/build?delay=0sec
