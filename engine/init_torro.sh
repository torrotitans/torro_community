mkdir /home/torro_admin
mkdir /home/torro_admin/torro_backend
cp -r ./* /home/torro_admin/torro_backend/

yum install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm
yum install -y wget
yum install -y coreutils
yum install -y python3-devel
yum install -y tmux
wget https://repo.mysql.com//mysql80-community-release-el8-1.noarch.rpm
rpm -ivh mysql80-community-release-el8-1.noarch.rpm

yum install -y lsof
yum install -y git
yum install -y mysql-server
systemctl enable mysqld.service
systemctl list-unit-files|grep mysqld
systemctl start mysqld.service
ps -ef|grep mysql

mysql <<EOF
alter user 'root'@'localhost' identified by '123456';
create database torro_api;
EOF

yum install -y gcc-c++
yum -y install gcc automake autoconf libtool make
yum -y install zlib zlib-devel openssl openssl-devel pcre pcre-devel
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

cd /home/torro_admin
wget https://nodejs.org/dist/v14.17.6/node-v14.17.6-linux-x64.tar.xz
tar -xvf node-v14.17.6-linux-x64.tar.xz
mv node-v14.17.6-linux-x64 nodejs
cp /etc/profile /etc/profile.bak
echo 'export PATH=$PATH:/home/torro_admin/nodejs/bin' >> /etc/profile
source /etc/profile

cd /home/torro_admin/torro_backend
mysql –uroot –p123456 -Dtorro_api<./dbsql/data_api.sql
mysql –uroot –p123456 -Dtorro_api<./dbsql/form_api.sql
mysql –uroot –p123456 -Dtorro_api<./dbsql/org_api.sql
mysql –uroot –p123456 -Dtorro_api<./dbsql/user_api.sql
mysql –uroot –p123456 -Dtorro_api<./dbsql/data_api.sql

pip3 install -r requirements.txt
python3 init_torro.py
nohup gunicorn -b 0.0.0.0:3128 main:app &
