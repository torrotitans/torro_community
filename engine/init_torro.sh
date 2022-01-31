
echo "  ______                        ___    ____"
echo " /_  __/___  ______________    /   |  /  _/"
echo "  / / / __ \/ ___/ ___/ __ \  / /| |  / /  "
echo " / / / /_/ / /  / /  / /_/ / / ___ |_/ /   "
echo "/_/  \____/_/  /_/   \____(_)_/  |_/___/   "
                                           
echo "Welcome and thank you for choosing Torro.ai"
echo "The installation will begin shortly"
echo "It is expected to take around 30 mins"

echo "<<==================== Creating Working folders ====================>>"
mkdir /home/torro_admin
mkdir /home/torro_admin/torro_backend
cp -r ./* /home/torro_admin/torro_backend/

echo "<<==================== Installing OS dependencies ====================>>"
yum install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm
yum install -y wget
yum install -y coreutils
yum install -y python3-devel
yum install -y python3-setuptools
yum install -y tmux
yum install -y gcc-c++
yum -y install gcc automake autoconf libtool make
yum -y install zlib zlib-devel openssl openssl-devel pcre pcre-devel
wget https://repo.mysql.com//mysql80-community-release-el8-1.noarch.rpm
rpm -ivh mysql80-community-release-el8-1.noarch.rpm

yum install -y lsof
# yum install -y git
yum install -y mysql-server
systemctl enable mysqld.service
systemctl list-unit-files|grep mysqld
systemctl start mysqld.service
ps -ef|grep mysql

echo "<<==================== Configing MySQL Login ====================>>"
mysql <<EOF
alter user 'root'@'localhost' identified by '123456';
create database torro_api;
EOF

echo "<<==================== Installing the Webserver ====================>>"
cd /home/torro_admin
wget http://nginx.org/download/nginx-1.19.9.tar.gz
tar -zxvf nginx-1.19.9.tar.gz nginx-1.19.9/
cd nginx-1.19.9
./configure --prefix=/home/torro_admin/nginx --with-http_ssl_module
make
make install
cd /home/torro_admin/torro_backend
\cp -f ./nginx.conf /home/torro_admin/nginx/conf/
cd /home/torro_admin/nginx/
mkdir /home/torro_admin/nginx/conf/crt/
mkdir /var/log/nginx/
echo ''> /var/log/nginx/error.log
openssl genrsa -out /home/torro_admin/nginx/conf/crt/server.key &>/dev/null
openssl req -new -x509 -key /home/torro_admin/nginx/conf/crt/server.key -subj "/CN=commmon" -out /home/torro_admin/nginx/conf/crt/server.crt &>/dev/null
cd /home/torro_admin/nginx/sbin/
./nginx

yum install -y nodejs

cd /home/torro_admin/torro_backend
echo "<<==================== Initiating the MySQL db for the first time ====================>>"

mysql -uroot -p123456 -Dtorro_api<./dbsql/data_api.sql
mysql -uroot -p123456 -Dtorro_api<./dbsql/form_api.sql
mysql -uroot -p123456 -Dtorro_api<./dbsql/org_api.sql
mysql -uroot -p123456 -Dtorro_api<./dbsql/user_api.sql
mysql -uroot -p123456 -Dtorro_api<./dbsql/workflow_api.sql

echo "<<==================== Installing Python dependencies ====================>>"
export FLASK_CONFIG=production

# pip3 install --upgrade pip
# python3 -m pip install --upgrade setuptools
pip3 install -r requirements.txt

echo "<<==================== Configuring Python Backend ====================>>"
python3 init_torro.py

echo "<<==================== Starting the Backend Webserver ====================>>"
nohup gunicorn -b 0.0.0.0:8080 main:app &
