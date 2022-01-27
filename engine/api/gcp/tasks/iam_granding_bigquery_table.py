from api.gcp.tasks.baseTask import baseTask
# from google.cloud import datacatalog_v1beta1
import google
from db.base import DbBase
from db.connection_pool import MysqlConn
from utils.log_helper import lg
import datetime
from utils.status_code import response_code
from config import configuration
import google.auth
import googleapiclient.discovery
from googleapiclient.errors import HttpError
import json
import os
import traceback
from config import config
from core.form_singleton import formSingleton_singleton
from core.workflow_singleton import workflowSingleton_singleton

config_name = os.getenv('FLASK_CONFIG') or 'default'
Config = config[config_name]


# class GrantRoleForBQTable(baseTask):
class GrantRoleForBQTable(baseTask, DbBase):
    api_type = 'gcp'
    api_name = 'GrantRoleForBQTable'
    arguments = {
        "project_id": {"type": str, "default": ''},
        "usecase_name": {"type": str, "default": ''},
        "location": {"type": str, "default": ''},
        'dataset_id': {"type": str, "default": ''},
        "table_id": {"type": str, "default": ''},
    }
    role_list = ['roles/bigquery.dataOwner', 'roles/bigquery.admin']

    def __init__(self, stage_dict):
        super(GrantRoleForBQTable, self).__init__(stage_dict)
        # # print('self.stage_dict:', self.stage_dict)

        self.full_resource_name = None
        self.target_project = self.stage_dict['project_id']

    def execute(self, workspace_id=None, form_id=None, input_form_id=None, user_id=None):

        conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()

            missing_set = set()
            for key in self.arguments:
                check_key = self.stage_dict.get(key, 'NotFound')
                if check_key == 'NotFound':
                    missing_set.add(key)
                # # print('{}: {}'.format(key, self.stage_dict[key]))
            if len(missing_set) != 0:
                return 'Missing parameters: {}'.format(', '.join(missing_set))
            else:
                usecase_name = self.stage_dict['usecase_name']
                project_id = self.stage_dict['project_id']
                location = self.stage_dict['location']
                dataset_id = self.stage_dict['dataset_id']
                table_id = self.stage_dict['table_id']
                # get usecase service account & ad group
                data = self.__get_adgroup_service_accout(workspace_id, usecase_name, db_name, conn)
                if data['code'] != 200:
                    return data['msg']
                service_account = data['data']['sa']
                ad_group_list = data['data']['ad_group_list']
                print('sa and ad:', data)
                ad_group_list = []
                # check if already get the table access
                table_policy = self.__grand_access_roles(service_account, ad_group_list, project_id, dataset_id,
                                                         table_id)
                if not table_policy:
                    return 'Failed to grand access to table: {} for usercase: {}'.format(
                        '.'.join([workspace_id, project_id, dataset_id, table_id]), usecase_name)

                cond = "workspace_id='%s' and project_id='%s' and location='%s' and dataset_id='%s' and table_id='%s'" % (
                    workspace_id, project_id, location, dataset_id, table_id)
                # check table is onaboarded or not
                sql = self.create_select_sql(db_name, 'dataOnboardTable', 'input_form_id, fields', cond)
                table_info = self.execute_fetch_one(conn, sql)
                if not table_info:
                    return 'Table is not onboard: {}'.format(
                        '.'.join([str(workspace_id), project_id, dataset_id, table_id]))
                print('table_info:', table_info)
                # get data info
                data_input_form_id = table_info['input_form_id']
                data_fields = json.loads(table_info['fields'])
                access_fields = []
                for data_field in data_fields:
                    if 'policyTags' not in data_field or 'names' not in data_field['policyTags'] or len(
                            data_field['policyTags']['names']) == 0 or data_field['policyTags']['names'][0] == None:
                        access_fields.append(data_field)
                cond = "data_input_form_id='%s'" % (data_input_form_id)
                sql = self.create_select_sql(db_name, 'dataAccessTable', 'data_access_input_form_id', cond)
                print('dataAccessTable sql:', sql)
                table_access_info = self.execute_fetch_one(conn, sql)
                if table_access_info:
                    now = str(datetime.datetime.today())
                    column_fields = ('data_access_input_form_id', 'fields', 'create_time')
                    values = (input_form_id, json.dumps(access_fields), now)
                    sql = self.create_update_sql(db_name, 'dataAccessTable', column_fields, values, cond)
                    print('GrantRoleForBQTable update_sql dataAccessTable:', sql)
                    return_count = self.updete_exec(conn, sql)

                    # return 'Already get the table access: {}'.format(
                    #     '.'.join([str(workspace_id), project_id, dataset_id, table_id]))
                else:
                    fields = (
                        'data_input_form_id', 'data_access_input_form_id', 'fields', 'create_time')
                    now = str(datetime.datetime.today())
                    values = (
                        data_input_form_id, input_form_id, json.dumps(access_fields),now)
                    sql = self.create_insert_sql(db_name, 'dataAccessTable',
                                                 '({})'.format(', '.join(fields)), values)
                    print('GrantRoleForBQTable create_insert_sql dataAccessTable:', sql)
                    _ = self.insert_exec(conn, sql, return_insert_id=True)
                # print('tagTemplatesTable insert sql:', sql)

                return 'Get the table access successfully: {}'.format(
                    '.'.join([str(workspace_id), project_id, dataset_id, table_id]))

        except HttpError as e:
            return (json.loads(e.content))
        except Exception as e:
            import traceback
            lg.error(traceback.format_exc())
            return response_code.ADD_DATA_FAIL
        finally:
            conn.close()
            # pass

    def __get_adgroup_service_accout(self, workspace_id, usecase_name, db_name, conn):

        service_account = None
        ad_group_list = []

        cond = "WORKSPACE_ID='%s' and USECASE_NAME='%s'" % (
            workspace_id, usecase_name)
        sql = self.create_select_sql(db_name, 'usecaseTable', 'ID,SERVICE_ACCOUNT', cond)
        usecase_info = self.execute_fetch_one(conn, sql)
        if not usecase_info:
            data = response_code.GET_DATA_FAIL
            data['msg'] = 'Cannot find usecase: {}'.format(
                '.'.join([workspace_id, usecase_name]))
            return data
        service_account = usecase_info['SERVICE_ACCOUNT']
        # get ad group
        condition = 'USECASE_ID="%s"' % usecase_info['ID']
        relation_tables = [
            {'table_name': 'adgroupTable', 'join_condition': 'adgroupTable.ID=usecase_to_adgroupTable.AD_GROUP_ID'}
        ]
        sql = self.create_get_relation_sql(db_name, 'usecase_to_adgroupTable', 'GROUP_MAIL', relations=relation_tables,
                                           condition=condition)
        ad_group_infos = self.execute_fetch_all(conn, sql)
        for ad_group in ad_group_infos:
            ad_group_list.append(ad_group['GROUP_MAIL'])
        data = response_code.SUCCESS
        data['data'] = {'sa': service_account, 'ad_group_list': ad_group_list}
        return data

    def __grand_access_roles(self, service_account, ad_group_list, project_id, dataset_id, table_id):
        try:
            access_roles = ['roles/bigquery.dataViewer']
            # # default access json
            access_json = {'roles/bigquery.dataViewer': ['serviceAccount:{}'.format(service_account)]}
            for ad_group in ad_group_list:
                access_json['roles/bigquery.jobUser'].append('group:{}'.format(ad_group))
                access_json['roles/bigquery.dataViewer'].append('group:{}'.format(ad_group))
            print('access_json:', access_json)
            credentials, project = google.auth.default()
            service = googleapiclient.discovery.build(
                'bigquery', 'v2', credentials=credentials)

            table_policy = service.tables().getIamPolicy(
                resource='projects/{project}/datasets/{dataset}/tables/{table}'.format(
                    project=project_id, dataset=dataset_id, table=table_id),
            ).execute()
            print('table_policy:', table_policy)
            if 'bindings' not in table_policy:
                return 'Get table policy failed for: {}'.format(
                    '.'.join([project_id, dataset_id, table_id]))
            # job_user_flag = 0
            data_viewer_flag = 0
            for index, role_info in enumerate(table_policy['bindings']):
                role = role_info['role']
                if role == access_roles[0]:
                    data_viewer_flag = 1
                    now_members = table_policy['bindings'][index]['members']
                    print('now_members:', now_members, access_json[role])
                    now_members.extend(access_json[role])
                    table_policy['bindings'][index]['members'] = list(set(now_members))
                # if role == access_roles[1]:
                #     data_viewer_flag = 1
                #     now_members = table_policy['bindings'][index]['members']
                #     table_policy['bindings'][index]['members'] = list(set(now_members.extend(access_json[role])))
            # if job_user_flag == 0:
            #     role = access_roles[0]
            #     table_policy['bindings'].append({'role': role,
            #                                      'members': access_json[role]})
            if data_viewer_flag == 0:
                role = access_roles[0]
                table_policy['bindings'].append({'role': role,
                                                 'members': access_json[role]})
            print('new table_policy:', table_policy, data_viewer_flag)
            return_table_policy = service.tables().setIamPolicy(
                resource='projects/{project}/datasets/{dataset}/tables/{table}'.format(
                    project=project_id, dataset=dataset_id, table=table_id),
                body={'policy': table_policy}
            ).execute()

            return return_table_policy
        except:
            lg.error(traceback.format_exc())
            return None


if __name__ == '__main__':
    x = GrantRoleForBQTable({"tag_template_display_name": 'Create Tag Templates Api',
                             "description": 'testing api tasks',
                             "field_list": [
                                 {
                                     "style": 1,
                                     "label": "CheckBox",
                                     "default": "true,false",
                                     "options": [
                                         {
                                             "label": "true"
                                         },
                                         {
                                             "label": "false"
                                         }
                                     ],
                                     "des": "",
                                     "edit": 1,
                                     "placeholder": ""
                                 },
                                 {
                                     "style": 2,
                                     "label": "Dropdown",
                                     "default": "Option1",
                                     "options": [
                                         {
                                             "label": "Option1",
                                             "value": "Option1"
                                         },
                                         {
                                             "label": "Option2",
                                             "value": "Option2"
                                         }
                                     ],
                                     "des": "",
                                     "edit": 1,
                                     "required": True,
                                     "placeholder": ""
                                 },
                                 {
                                     "style": 3,
                                     "label": "Text",
                                     "default": "",
                                     "options": [],
                                     "des": "",
                                     "edit": 1,
                                     "maxLength": 25,
                                     "required": True,
                                     "placeholder": "",
                                     "rule": 0
                                 },
                                 {
                                     "style": 5,
                                     "label": "Switch",
                                     "default": True,
                                     "placeholder": "",
                                     "options": [],
                                     "des": "",
                                     "edit": 1
                                 },
                                 {
                                     "style": 6,
                                     "label": "DatePicker",
                                     "placeholder": "",
                                     "default": "",
                                     "options": [],
                                     "des": "",
                                     "required": True,
                                     "edit": 1
                                 }
                             ]
                             })
    x.execute()

    # get policy api
