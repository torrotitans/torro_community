# Torro Community
Torro is a unified data & AI governance engine on the google cloud. It provides a pre-defined business framework for Chief Data Officers or ML Governors to manage the day-to-day data and AI operations on the cloud more effectively with auto lineage approval, complete audit trail reporting, ML model governance review and more. 

Currently, Torro community is under public beta preview and feel free to raise any bugs report and feature requests, any contribution is welcome!

## 1.0 GCP Setup 
```
Enable Component:
'Cloud Asset API', 'Cloud Asset API', 'Cloud Storage', 'BigQuery', 'IAM'

Service account project permission: 
'Cloud Asset Viewer', 'BigQuery Admin', 
'Data Catalog Admin', 'Fine-Grained Reader', 
'Service Account Admin', 'Storage Admin'
```


## 2.0 Config files
```
Torro: config.ini
GCP: config.py
Ldap/offline: common/common_input_form_status.py: *offline_flag*
```

### 3.0 Run the init script

```
git clone torro_backend
run: init_torro.sh
```

### 4.0 Setup the webserver
- Install dependencies: `npm install`

- Start the server: `npm run start`

- Views are on: `localhost:8080`

## Licensing
Torro Community Edition is an open source product licensed under AGPLv3.
