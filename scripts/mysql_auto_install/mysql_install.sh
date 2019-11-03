#!/bin/bash

mysql_bin=/usr/local/mysql
mysql_data_dir=/data/mysql/data
#echo "export PATH=/usr/local/mysql/bin:$PATH" >> /etc/profile
grep -r mysql/bin /etc/profile >/dev/null
if [ $? != 0 ];then
    echo "export PATH=${mysql_bin}/bin:\$PATH" >> /etc/profile
else 
    echo 'Mysql配置文件已存在.....请检查'
    exit
fi
source /etc/profile
#卸载mariadb
rpm -e --nodeps `rpm -qa | grep mariadb` 2>/dev/null
echo "安装程序正在进行，请稍后..............."
cd /tmp
mysql_version=`ls mysql*.tar.gz | head -1 | awk -F".tar.gz" '{print $1}'`
mkdir -p $mysql_bin
tar -zxf $mysql_version* -C $mysql_bin
mv $mysql_bin/$mysql_version/* $mysql_bin
rm -rf $mysql_bin/$mysql_version

#创建Mysql_Data目录
mkdir -p $mysql_data_dir
useradd -M -s /sbin/nologin mysql
chown -R mysql. $mysql_data_dir


#无限制，无临时密码安装
mysqld --initialize-insecure --user=mysql --basedir=$mysql_bin --datadir=$mysql_data_dir

#配置文件的准备
cat >/etc/my.cnf <<EOF
[mysqld]
user=mysql
basedir=$mysql_bin
datadir=$mysql_data_dir
socket=$mysql_data_dir/mysql.sock
server_id=6
port=3306
[mysql]
socket=$mysql_data_dir/mysql.sock
EOF
#启动Mysql.......
cp $mysql_bin/support-files/mysql.server /etc/init.d/mysqld
service mysqld start

