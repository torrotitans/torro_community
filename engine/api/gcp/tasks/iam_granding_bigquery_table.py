from api.gcp.tasks.baseTask import baseTask
# from google.cloud import datacatalog_v1beta1
import google
from db.connection_pool import MysqlConn
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
import traceback
import logging

logger = logging.getLogger("main." + __name__)
config_name = os.getenv('FLASK_CONFIG') or 'default'
Config = config[config_name]


# class GrantRoleForBQTable(baseTask):
class GrantRoleForBQTable(baseTask):
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
                data = response_code.BAD_REQUEST
                data['msg'] = 'Missing parameters: {}'.format(', '.join(missing_set))
                return data
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
                service_account = data['data'].get('sa', None)
                ad_group_list = data['data'].get('ad_group_list', [])
                logger.debug("FN:GrantRoleForBQTable_execute data:{}".format(data))
                # ad_group_list = []
                # check if already get the table access
                table_policy = self.__grand_access_roles(service_account, ad_group_list, project_id, dataset_id,
                                                         table_id)
                if not table_policy:
                    return 'Failed to grand access to table: {} for usercase: {}'.format(
                        '.'.join([workspace_id, str(project_id), str(dataset_id), str(table_id)]), usecase_name)

                cond = "workspace_id='%s' and project_id='%s' and location='%s' and dataset_id='%s' and table_id='%s'" % (
                    workspace_id, project_id, location, dataset_id, table_id)
                # check table is onaboarded or not
                sql = self.create_select_sql(db_name, 'dataOnboardTable', 'input_form_id, fields', cond)
                logger.debug("FN:GrantRoleForBQTable_execute dataOnboardTable_sql:{}".format(sql))
                table_info = self.execute_fetch_one(conn, sql)

                if not table_info:
                    return 'Table is not onboard: {}'.format(
                        '.'.join([str(workspace_id), str(project_id), str(dataset_id), str(table_id)]))

                logger.debug("FN:GrantRoleForBQTable_execute table_info:{}".format(table_info))
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
                logger.debug("FN:GrantRoleForBQTable_execute dataAccessTable_sql:{}".format(sql))
                table_access_info = self.execute_fetch_one(conn, sql)

                # check if usecase exist
                condition = 'USECASE_NAME="%s" and WORKSPACE_ID="%s"' % (usecase_name, workspace_id)
                sql = self.create_select_sql(db_name, 'usecaseTable', 'ID,CREATE_TIME', condition)
                # print('usecaseTable: ', sql)
                usecase_info = self.execute_fetch_one(conn, sql)
                if not usecase_info:
                    return 'Cannot find usecase: {} in workspace: {}'.format(usecase_name, str(workspace_id))
                usecase_id = usecase_info['ID']

                if table_access_info:
                    now = str(datetime.datetime.today())
                    column_fields = ('data_access_input_form_id','usecase_id', 'fields', 'create_time')
                    values = (input_form_id, usecase_id, json.dumps(access_fields), now)
                    sql = self.create_update_sql(db_name, 'dataAccessTable', column_fields, values, cond)
                    logger.debug("FN:GrantRoleForBQTable_execute update_dataAccessTable_sql:{}".format(sql))
                    return_count = self.updete_exec(conn, sql)

                    # return 'Already get the table access: {}'.format(
                    #     '.'.join([str(workspace_id), str(project_id), str(dataset_id), str(table_id)]))
                else:
                    fields = (
                        'data_input_form_id', 'data_access_input_form_id','usecase_id', 'fields', 'create_time')
                    now = str(datetime.datetime.today())
                    values = (
                        data_input_form_id, input_form_id, usecase_id, json.dumps(access_fields),now)
                    sql = self.create_insert_sql(db_name, 'dataAccessTable',
                                                 '({})'.format(', '.join(fields)), values)
                    logger.debug("FN:GrantRoleForBQTable_execute insert_dataAccessTable_sql:{}".format(sql))
                    _ = self.insert_exec(conn, sql, return_insert_id=True)
                # logger.debug('tagTemplatesTable insert sql:', sql)
                data = response_code.SUCCESS
                data['data'] = 'Get the table access successfully: {}'.format(
                    '.'.join([str(workspace_id), str(project_id), str(dataset_id), str(table_id)]))
                return data
        except HttpError as e:
            error_json = json.loads(e.content)
            data = error_json['error']
            data["msg"] = data.pop("message")
            logger.error("FN:GrantRoleForBQTable_execute error:{}".format(traceback.format_exc()))
            return data
        except Exception as e:
            logger.error("FN:GrantRoleForBQTable_execute error:{}".format(traceback.format_exc()))
            data = response_code.BAD_REQUEST
            data['msg'] = str(e)
            return data
        finally:
            conn.close()
            # pass

    def __get_adgroup_service_accout(self, workspace_id, usecase_name, db_name, conn):

        service_account = None
        ad_group_list = []

        cond = "WORKSPACE_ID='%s' and USECASE_NAME='%s'" % (
            workspace_id, usecase_name)
        sql = self.create_select_sql(db_name, 'usecaseTable', 'ID,SERVICE_ACCOUNT', cond)
        logger.debug('FN:GrantRoleForBQTable__get_adgroup_service_accout usecaseTable_sql:{} '.format(sql))
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
        logger.debug('FN:GrantRoleForBQTable__get_adgroup_service_accout get_adGroup_id_sql:{} '.format(sql))
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
            if service_account:
                access_json = {'roles/bigquery.dataViewer': ['serviceAccount:{}'.format(service_account)]}
            else:
                access_json = {'roles/bigquery.dataViewer': []}
            for ad_group in ad_group_list:
                # access_json['roles/bigquery.jobUser'].append('group:{}'.format(ad_group))
                access_json['roles/bigquery.dataViewer'].append('group:{}'.format(ad_group))
            logger.debug('FN:GrantRoleForBQTable__grand_access_roles access_json:{} '.format(access_json))
            credentials, project = google.auth.default()
            service = googleapiclient.discovery.build(
                'bigquery', 'v2', credentials=credentials)

            table_policy = service.tables().getIamPolicy(
                resource='projects/{project}/datasets/{dataset}/tables/{table}'.format(
                    project=project_id, dataset=dataset_id, table=table_id),
            ).execute()

            logger.debug('FN:GrantRoleForBQTable__grand_access_roles table_policy:{} '.format(table_policy))
            if 'bindings' not in table_policy and 'etag' in table_policy:
                table_policy['bindings'] = []
            elif 'bindings' not in table_policy:
                return 'Get table policy failed for: {}'.format(
                    '.'.join([project_id, str(dataset_id), str(table_id)]))
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
            logger.debug('FN:GrantRoleForBQTable__grand_access_roles new_table_policy:{} data_viewer_flag:{}'.format(table_policy, data_viewer_flag))
            return_table_policy = service.tables().setIamPolicy(
                resource='projects/{project}/datasets/{dataset}/tables/{table}'.format(
                    project=project_id, dataset=dataset_id, table=table_id),
                body={'policy': table_policy}
            ).execute()

            return return_table_policy
        except:
            logger.error("FN:GrantRoleForBQTable__grand_access_roles error:{}".format(traceback.format_exc()))
            return None
