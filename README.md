

## Quick start

- [Clone the Repo]

- Make sure your NodeJS and npm versions are up to date for `React 16.8.6`

- Install dependencies: `npm install` or `yarn`

- Start the server: `npm run start` or `yarn start`

- Views are on: `localhost:3000`

## File Structure

```
material-react-dashboard

├── .eslintrc
├── .gitignore
├── .prettierrc
├── CHANGELOG.md
├── jsconfig.json
├── LICENSE.md
├── package.json
├── README.md
├── public
└── src
	├── mixins
	├── components
	├── utils
	├── icons
	├── layouts
	├── theme
	├── views
	│	├── config_forms
	│	├── forms
	│	├── statusflows
	│	├── tasks
	│	├── user_requests
	│	├── reports
	│	├── errors
	│	└── common_parameters.js
	├── App.js
	├── index.js
	├── serviceWorker.js
	└── Routes.js
```

## Reference Documentation

The documentation for the React Material Kit is can be found [here](https://material-ui.com?ref=devias-io).



## Framework Demo

- [Framework Repo](https://github.com/chcontrol/react-material-dashboard-master.git)
- [Dashboard Page](https://react-material-dashboard.devias.io/app/dashboard)
- [Users Page](https://react-material-dashboard.devias.io/app/customers)
- [Products Page](https://react-material-dashboard.devias.io/app/products)
- [Register Page](https://react-material-dashboard.devias.io/register)
- [Login Page](https://react-material-dashboard.devias.io/login)
- [Account Page](https://react-material-dashboard.devias.io/app/account)
- [Settings Page](https://react-material-dashboard.devias.io/app/settings)

### torro_ai

##### 1.项目依赖
```
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
alter user 'root'@'localhost' identified by '123456';
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
```
Nodejs
```
cd /home/torro_admin
wget https://nodejs.org/dist/v14.17.6/node-v14.17.6-linux-x64.tar.xz
tar -xvf node-v14.17.6-linux-x64.tar.xz
mv node-v14.17.6-linux-x64 nodejs
cp /etc/profile /etc/profile.bak
echo 'export PATH=$PATH:/home/torro_admin/nodejs/bin' >> /etc/profile
source /etc/profile
```
```
ldap3==2.9
aniso8601==8.0.0  
Click==7.0    
DBUtils==1.3    
Flask==1.1.1  
Flask-Cors==3.0.8  
Flask-JWT==0.3.2  
Flask-RESTful==0.3.7  
itsdangerous==1.1.0  
Jinja2==2.10.3 
MarkupSafe==1.1.1  
PyJWT==1.4.2  
PyMySQL==0.9.3  
xmltodict==0.12.0
gunicorn==20.1.0
pycryptodome==3.10.1
```

 安装依赖，请切换到项目工程目录下面。然后使用如下命令进行安装：

```
pip install -r requirements.txt
```

##### 2. 项目的启动文件

```
cd torro_backend
nohup gunicorn -b 0.0.0.0:3128 main:app &
```

##### 3. 项目配置文件

```
config.ini
```

##### 4 .项目数据sql

```
user_api.sql
```
''''
##### 5 .gcp

```
enable 'Cloud Asset API'

project: Cloud Asset Viewer
```
''''
>数据库中默认有一个用户名为：root 密码为：123456

