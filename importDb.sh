#!/bin/bash

sysType=$(uname)
pass='123456'
dbName='fmd'

if [ $sysType == 'Linux' ]; then
	sqlExe=/usr/bin/mysql
else
	sqlExe=/Applications/XAMPP/bin/mysql
fi

echo "delete old datbase ${dbName}"
$sqlExe -uroot -p${pass} -e "drop database if exists ${dbName}";

echo "create datbase ${dbName}"
$sqlExe -uroot -p${pass} -e "create database if not exists ${dbName}";

for sqlFile in `ls *.sql` ; do
	if [ -d $sqlFile ] ; then
		echo $sqlFile is dir
	else
		echo "install $sqlFile"
		$sqlExe -uroot -p${pass}  ${dbName} < $sqlFile
	fi
done

echo "install done"

