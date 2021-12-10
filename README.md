# Torro Community
Torro is a unified data & AI governance engine on the google cloud. It provides a pre-defined business framework for Chief Data Officers or ML Governors to manage the day-to-day data and AI operations on the cloud more effectively with auto lineage approval, complete audit trail reporting, ML model governance review and more. 

Currently, Torro community is under public beta preview and feel free to raise any bugs report and feature requests, any contribution is welcome!

## Prerequisite 
```
pip install -r requirements.txt
yum install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm
yum install -y wget
yum install -y coreutils
yum install -y python3-devel
yum install -y tmux
wget https://repo.mysql.com//mysql80-community-release-el8-1.noarch.rpm
rpm -ivh mysql80-community-release-el8-1.noarch.rpm

yum install -y git
yum install -y mysql-server
systemctl enable mysqld.service
systemctl list-unit-files|grep mysqld
systemctl start mysqld.service
ps -ef|grep mysql
mysql
alter user 'root'@'localhost' identified by 'XXXX';
create database torro_api;

yum install -y gcc-c++
yum -y install gcc automake autoconf libtool make
yum -y install zlib zlib-devel openssl openssl-devel pcre pcre-devel
mkdir /home/torro_admin
cd /home/torro_admin
wget http://nginx.org/download/nginx-1.19.9.tar.gz
tar -zxvf nginx-1.19.9.tar.gz nginx-1.19.9/
cd nginx-1.19.9
./configure --prefix=/home/torro_admin/nginx --with-http_ssl_module
make
make install
cd /home/torro_admin/nginx/
mkdir /home/torro_admin/nginx/conf/crt/
mkdir /var/log/nginx/
echo ''> /var/log/nginx/error.log
openssl genrsa -out /home/torro_admin/nginx/conf/crt/server.key &>/dev/null
openssl req -new -x509 -key /home/torro_admin/nginx/conf/crt/server.key -subj "/CN=commmon" -out /home/torro_admin/nginx/conf/crt/server.crt &>/dev/null

cd /home/torro_admin
wget https://nodejs.org/dist/v14.17.6/node-v14.17.6-linux-x64.tar.xz
tar -xvf node-v14.17.6-linux-x64.tar.xz
mv node-v14.17.6-linux-x64 nodejs
cp /etc/profile /etc/profile.bak
echo 'export PATH=$PATH:/home/torro_admin/nodejs/bin' >> /etc/profile
source /etc/profile
```


UI Server startup
- Make sure your NodeJS and npm versions are up to date for `React 16.8.6`
- Install dependencies: `npm install` or `yarn`
- Start the server: `npm run start` or `yarn start`
- Views are on: `localhost:3000`

### Start the Engine

```
cd torro_community/engine
nohup gunicorn -b 0.0.0.0:3128 main:app &
```

### Configure file

```
config.ini
```

### Project SQL

```
user_api.sql
```

### List of GCP IAM

```
enable 'Cloud Asset API'

project: Cloud Asset Viewer
# to be updated
```

## Licensing
Torro Community Edition is an open source product licensed under AGPLv3.
