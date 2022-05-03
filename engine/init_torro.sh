#!/usr/bin/env bash

echo ""
echo "            ______                        ___    ____"
echo "           /_  __/___  ______________    /   |  /  _/"
echo "            / / / __ \/ ___/ ___/ __ \  / /| |  / /  "
echo "           / / / /_/ / /  / /  / /_/ / / ___ |_/ /   "
echo "          /_/  \____/_/  /_/   \____(_)_/  |_/___/   "
echo ""
echo ""
echo ""
echo "Welcome and thank you for choosing Torro.ai"
echo "The installation will begin shortly"
echo "It is expected to take around 30 mins"
echo ""
echo ""
echo ""

echo "<<==================== Installing OS dependencies ====================>>"
echo ""
echo ""
echo ""
yum install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm
yum install -y nano wget coreutils python3-devel python3-setuptools tmux gcc-c++ gcc automake autoconf libtool make zlib zlib-devel openssl openssl-devel pcre pcre-devel nginx lsof nodejs
wget https://repo.mysql.com//mysql80-community-release-el8-1.noarch.rpm
rpm -ivh mysql80-community-release-el8-1.noarch.rpm
yum install -y mysql-server
echo ""
echo ""
echo ""

echo "<<==================== Configing MySQL Login ====================>>"
echo ""
echo ""
echo ""
systemctl enable mysqld.service
systemctl list-unit-files|grep mysqld
systemctl start mysqld.service
ps -ef|grep mysql
mysql <<EOF
alter user 'root'@'localhost' identified by '123456';
create database torro_api;
EOF
echo ""
echo ""
echo ""

echo "<<==================== Initiating the MySQL db for the first time ====================>>"
echo ""
echo ""
echo ""
cd /root/torro_community/engine
mysql -uroot -p123456 -Dtorro_api<./dbsql/data_api.sql
mysql -uroot -p123456 -Dtorro_api<./dbsql/form_api.sql
mysql -uroot -p123456 -Dtorro_api<./dbsql/org_api.sql
mysql -uroot -p123456 -Dtorro_api<./dbsql/user_api.sql
mysql -uroot -p123456 -Dtorro_api<./dbsql/workflow_api.sql
echo ""
echo ""
echo ""

echo "<<==================== Installing Python dependencies ====================>>"
echo ""
echo ""
echo ""
export FLASK_CONFIG=production

# pip3 install --upgrade pip
# python3 -m pip install --upgrade setuptools
pip3 install -r requirements.txt
echo ""
echo ""
echo ""

echo "<<==================== Installing Nginx ====================>>"
echo ""
echo ""
echo ""
cd /root
wget http://nginx.org/download/nginx-1.19.9.tar.gz
tar -zxvf nginx-1.19.9.tar.gz nginx-1.19.9/
cd nginx-1.19.9
./configure --prefix=/root/nginx --with-http_ssl_module
make
make install
echo ""
echo ""
echo ""

echo "<<==================== Configuring Nginx ====================>>"
echo ""
echo ""
echo ""
openssl genrsa -out /root/torro_community/engine/server.key &>/dev/null
openssl req -new -x509 -key /root/torro_community/engine/server.key -subj "/CN=commmon" -out /root/torro_community/engine/server.crt &>/dev/null
mkdir /var/log/nginx/
echo ''> /var/log/nginx/error.log
mv /root/nginx/conf/nginx.conf /root/nginx/conf/nginx.conf.bak
cp -f /root/torro_community/engine/nginx.conf /root/nginx/conf/
/root/nginx/sbin/nginx
echo ""
echo ""
echo ""

echo "<<==================== Configuring Python Backend ====================>>"
echo ""
echo ""
echo ""
python3 init_torro.py
echo ""
echo ""
echo ""

echo "<<==================== Starting the Backend Webserver ====================>>"
echo ""
echo ""
echo ""
nohup gunicorn -b 0.0.0.0:8080 main:app &
