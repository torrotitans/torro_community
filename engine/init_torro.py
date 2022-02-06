#!/usr/bin/python
# -*- coding: UTF-8 -*
"""

"""
import google
import os
from google.cloud import storage
from config import config
from db.connection_pool import MysqlConn
import googleapiclient.discovery
from config import configuration

from db.base import DbBase
config_name = os.getenv('FLASK_CONFIG') or 'default'
Config = config[config_name]


def init_gcp():


    project = Config.DEFAULT_PROJECT
    bucket_name = Config.DEFAULT_BUCEKT
    location = Config.DEFAULT_REGION
    bucket_cmek = Config.BUCEKT_CMKE
    # create torro bucket
    storage_client = storage.Client(project)
    bucket = storage_client.create_bucket(bucket_name, location=location)
    if bucket_cmek:
        bucket.default_kms_key_name = bucket_cmek
    bucket.patch()
    # create approval tagtemplate
    tag_template_name = 'Data Approval Tag'
    des = 'AD group for Data Approvers'
    label = 'Data Approver AD group'
    tag_template_id, project, location = create_tag_template(tag_template_name, label, des, location, project)
    # exit(0)
    # update db
    conn = MysqlConn()
    db_name = configuration.get_database_name()
    db_operator = DbBase()
    condition = "tag_template_id='%s'" % tag_template_id
    column_fields = ('project_id', 'location')
    values = (project, location)
    sql = db_operator.create_update_sql(db_name, 'tagTemplatesTable', column_fields, values, condition)
    print('ModifyTablePolicyTags update_sql dataOnboardTable:', sql)
    return_count = db_operator.updete_exec(conn, sql)


def init_db():
    # run sql in dbsql
    pass


def create_tag_template(tag_template_name, label, des, location, project):

    credentials, _ = google.auth.default()
    # location = Config.DEFAULT_REGION
    service = googleapiclient.discovery.build(
        'datacatalog', 'v1beta1', credentials=credentials)

    fields = {}

    field = {'displayName': '', 'type': {'primitiveType': ''},
                      'description': '', 'order': 1}
    tag_template_id = tag_template_name.replace(' ', '_').lower().strip()
    field_id = label.replace(' ', '_').lower().strip()
    field['displayName'] = label
    field['description'] = des
    field['type']['primitiveType'] = 'STRING'
    fields[field_id] = field
    tag_template_body = {'displayName': tag_template_name, 'fields': {}}
    tag_template_body['fields'] = fields

    tag_template = service.projects().locations().tagTemplates().create(
        parent='projects/{project}/locations/{location}'.format(project=project, location=location),
        tagTemplateId=tag_template_id,
        body=tag_template_body
    ).execute()
    return tag_template_id, project, location

def check_service_account_permission():
    pass
# CORS(app, supports_credentials=True)
if __name__ == '__main__':
    init_gcp()
