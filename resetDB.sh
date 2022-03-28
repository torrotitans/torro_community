#!/usr/bin/env bash

cd engine
mysql -uroot -p123456 -Dtorro_api<./dbsql/data_api.sql
mysql -uroot -p123456 -Dtorro_api<./dbsql/form_api.sql
mysql -uroot -p123456 -Dtorro_api<./dbsql/org_api.sql
mysql -uroot -p123456 -Dtorro_api<./dbsql/user_api.sql
mysql -uroot -p123456 -Dtorro_api<./dbsql/workflow_api.sql