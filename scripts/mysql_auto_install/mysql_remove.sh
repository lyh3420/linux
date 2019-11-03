#!/bin/bash
service mysqld stop
rm -rf /usr/local/mysql/
rm -rf /data/mysql/
rm -rf /etc/my.cnf
rm -rf /etc/init.d/mysqld 
userdel mysql

