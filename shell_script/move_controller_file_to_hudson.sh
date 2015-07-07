#/bin/bash

svn_dir=/Users/miles/work/resource/mvo_resource/deployment/source_control/gmvo

if [ ! -d $svn_dir ] ; then
    echo "svn dir is not exists.[$svn_dir]"
	exit 1
fi

if [ "$1" == "" ] ; then
    echo "version_code is required."
	exit 1
else
	version_code=$1
	echo "version_code = $version_code"
fi

if [ ! -d $svn_dir/$version_code  ] ; then
	echo "floder is not exists. [$svn_dir/$version_code]"
	exit 1
fi

echo -n "Make sure version_code is needed ? [Y/n] : "
read YN
if [ ! "$YN" == "Y" ] ; then
	exit 1
fi

echo $version_code

cd $svn_dir
svn update
tar -zcvf $version_code.tar.gz $version_code
scp $version_code.tar.gz deploy@192.168.86.23:/app/deployscript/gmvo/input/$version_code.tar.gz
ssh deploy@192.168.86.23 -C "/app/deployscript/gmvo/input/copy_deploy_files.sh"


exit 0
