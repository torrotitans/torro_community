# Torro Community
Torro is a unified data & AI governance engine on the google cloud. It provides a pre-defined business framework for Chief Data Officers or ML Governors to manage the day-to-day data and AI operations on the cloud more effectively with auto lineage approval, complete audit trail reporting, ML model governance review and more. 

Currently, Torro community is under public beta preview and feel free to raise any bugs report and feature requests, any contribution is welcome!

# Torro installation:
## 0.0 Prerequisite:
Prefer Linux OS: Redhat 8+ / Centos 8  
Prefer HW Spec: 4 core 16GB + 500 GB

## 0.1 High level Components:
Backend: Flask + Gunicorn + nginx  
Frontend: React

## 1.0 Setup
### 1.1 GCP Setup
Enable Component:
'Cloud Asset API','Cloud Storage', 'BigQuery', 'IAM', 'Data Catalog', 'Dataproc'

Service account project permission: 
'Cloud Asset Viewer', 'BigQuery Admin', 
'Data Catalog Admin', 'Fine-Grained Reader', 
'Service Account Admin', 'Storage Admin'

### 1.2 Torro Setup
#### Linx dependences:
mysql, nginx, python3-devel, python3-setuptools, gcc-c++, tmux, wget, coreutils, openssl, openssl-devel, lsof, nano, nodejs

#### Python dependences:
refer to engine/requirements.txt

#### Nodejs dependences:
refer to server/package.json

### 1.3 Torro Config
nginx.conf - nginx related configuration  

config.ini - mysql related configuration  
config.py - torro engine configuration
```python
# Edit the parameters below before running 
class ProductionConfig(Config):
    DEBUG = False

    FRONTEND_URL = 'http://34.92.243.193:9000'
    DEFAULT_BUCEKT = 'torro_ai_landing_bucket_prod'
    DEFAULT_PROJECT = 'geometric-ocean-333410'
    DEFAULT_REGION = 'asia-east2'
    DEFAULT_SA = '580079130038-compute@developer.gserviceaccount.com'
    BUCEKT_CMKE = None
    pass
```

### 2.0 Install the engine:

For easy installation
```bash
git clone https://github.com/torrotitans/torro_community.git
cd torro_community/engine
bash init_torro.sh 
```

### 2.1 Step by step installation for engine
2.1.1. Install the OS yum packages:
```bash
yum install -y nginx python3-devel python3-setuptools gcc-c++ tmux wget coreutils openssl openssl-devel lsof nano nodejs

wget https://repo.mysql.com//mysql80-community-release-el8-1.noarch.rpm
rpm -ivh mysql80-community-release-el8-1.noarch.rpm

yum install -y mysql-server
systemctl enable mysqld.service
systemctl start mysqld.service
```

2.1.2. Install the Python packages:
```bash
pip3 install -r requirements.txt
```

2.1.3. Setup the mysql
```sql
alter user 'root'@'localhost' identified by '123456';
-- default pw, it should be modified and same as config.ini
create database torro_api;
```

2.1.4. Provision the database
```bash
# Default DB PW, should be changed and same as config.ini
mysql -uroot -p123456 -Dtorro_api<./dbsql/data_api.sql
mysql -uroot -p123456 -Dtorro_api<./dbsql/form_api.sql
mysql -uroot -p123456 -Dtorro_api<./dbsql/org_api.sql
mysql -uroot -p123456 -Dtorro_api<./dbsql/user_api.sql
mysql -uroot -p123456 -Dtorro_api<./dbsql/workflow_api.sql
```

2.1.5. Provision the nginx server
```bash
nano nginx.conf
```

```squidconf 
user root;
...
        root         /root/torro_community/server/build;
        location / {
            try_files $uri /index.html;
        }
        
        # This part is for the API connection to backend
        location ^~/api/{
            proxy_pass http://127.0.0.1:8080;
            proxy_redirect off;
            proxy_set_header Host \$http_host;
            proxy_set_header X-Real-IP \$remote_addr;
            proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto \$scheme;
            error_log /var/log/nginx/error.log warn;
        }
```

If above conf faced Nginx 403 forbidden, then do the following 
```
nano /etc/selinux/config
```
```bash
#SELINUX=enforcing
SELINUX=disabled
```
```bash
# Restart the VM
reboot
```

2.1.6. Start the nginx server
```bash
systemctl enable nginx.service
systemctl start nginx.service
cp torro_community/engine/nginx.conf /
```

### 2.0 Setup the server
```bash
cd torro_community/server/
npm install
npm run build:PROD -- REACT_APP_API_URL=http://x.x.x.x
```

### 3.0 Run Torro for the first time
```bash
cd torro_community/engine
nohup gunicorn -b 0.0.0.0:8080 main:app --workers 3 --timeout 6000 &
# If the system approval failed and timeout exceed worker timeout, 
# then it will cause the server to crash and restart
```

Go to your website and then use default account 
Acc: TorroAdmin
PW: torro123456

Proceed to setup the LDAP

Create Workspace

Create Use Case

Data Publising

Add User to Use Case

Data Consumption Request

## Licensing
Torro Community Edition is an open source product licensed under AGPLv3.
