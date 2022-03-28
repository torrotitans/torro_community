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
from config import config
import traceback
import logging

logger = logging.getLogger("main." + __name__)

config_name = os.getenv('FLASK_CONFIG') or 'default'
Config = config[config_name]

# class GrantRoleForPolicyTags(baseTask):
class GrantRoleForPolicyTags(baseTask):
    api_type = 'gcp'
    api_name = 'GrantRoleForPolicyTags'
    arguments = {
        "project_id": {"type": str, "default": ''},
        "usecase_name": {"type": str, "default": ''},
        "location": {"type": str, "default": ''},
        'dataset_id': {"type": str, "default": ''},
        "table_id": {"type": str, "default": ''},
        "fields": {"type": list, "default": []},
    }
    role_list = ['roles/datacatalog.categoryFineGrainedReader', 'roles/iam.securityReviewer', 'roles/dlp.serviceAgent']

    def __init__(self, stage_dict):
        super(GrantRoleForPolicyTags, self).__init__(stage_dict)
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
                fields = self.stage_dict['fields']

                # get usecase service account & ad group
                data = self.__get_adgroup_service_accout(workspace_id, usecase_name, db_name, conn)
                if data['code'] != 200:
                    return data['msg']
                service_account = data['data']['sa']
                ad_group_list = data['data']['ad_group_list']
                logger.debug("FN:GrantRoleForPolicyTags__get_adgroup_service_accout data:{}".format(data))
                # ad_group_list = []
                # check if already get the table access
                success_tag_policy_list, failed_policy_list = self.__grand_access_roles(service_account, ad_group_list, project_id, dataset_id, table_id, fields, db_name, conn)
                if failed_policy_list:
                    return 'Failed to grand access to policy tag: {} for usercase: {}'.format(
                        ', '.join(failed_policy_list), usecase_name)

                cond = "workspace_id='%s' and project_id='%s' and location='%s' and dataset_id='%s' and table_id='%s'" % (
                    workspace_id, project_id, location, dataset_id, table_id)
                # check table is onaboarded or not
                sql = self.create_select_sql(db_name, 'dataOnboardTable', 'input_form_id, fields', cond)
                table_info = self.execute_fetch_one(conn, sql)
                if not table_info:
                    return 'Table is not onboard: {}'.format(
                        '.'.join([str(workspace_id), str(project_id), str(dataset_id), str(table_id)]))
                data_input_form_id = table_info['input_form_id']
                # check if usecase exist
                condition = 'USECASE_NAME="%s" and WORKSPACE_ID="%s"' % (usecase_name, workspace_id)
                sql = self.create_select_sql(db_name, 'usecaseTable', 'ID,CREATE_TIME', condition)
                # print('usecaseTable: ', sql)
                usecase_info = self.execute_fetch_one(conn, sql)
                if not usecase_info:
                    return 'Cannot find usecase: {} in workspace: {}'.format(usecase_name, str(workspace_id))
                usecase_id = usecase_info['ID']
                # get data info
                data_input_form_id = table_info['input_form_id']
                cond = "data_input_form_id='%s' and usecase_id='%s'" % (data_input_form_id, usecase_id)
                sql = self.create_select_sql(db_name, 'dataAccessTable', 'data_access_input_form_id,fields', cond)
                table_access_info = self.execute_fetch_one(conn, sql)

                if not table_access_info:
                    column_fields = (
                        'data_input_form_id', 'data_access_input_form_id', 'usecase_id', 'fields', 'create_time')
                    now = str(datetime.datetime.today())
                    values = (
                        data_input_form_id, input_form_id, usecase_id, json.dumps(fields), now)
                    sql = self.create_insert_sql(db_name, 'dataAccessTable',
                                                 '({})'.format(', '.join(column_fields)), values)
                    logger.debug("FN:GrantRoleForPolicyTags__get_adgroup_service_accout insert_dataAccessTable_sql:{}".format(sql))
                    _ = self.insert_exec(conn, sql, return_insert_id=True)
                else:
                    new_fields = json.loads(table_access_info['fields'])
                    name_list = []
                    for field in new_fields:
                        field_name = field['name']
                        if field_name not in name_list:
                            name_list.append(field_name)
                    for field in fields:
                        field_name = field['name']
                        if field_name not in name_list:
                            new_fields.append(field)
                    column_fields = ('data_access_input_form_id', 'fields', 'create_time')
                    now = str(datetime.datetime.today())
                    values = (input_form_id, json.dumps(new_fields), now)
                    sql = self.create_update_sql(db_name, 'dataAccessTable', column_fields, values, cond)
                    logger.debug("FN:GrantRoleForPolicyTags__get_adgroup_service_accout update_dataAccessTable_sql:{}".format(sql))
                    return_count = self.updete_exec(conn, sql)

                return 'Get the table policy tags access successfully: {}'.format(
                    ', '.join(success_tag_policy_list))

        except HttpError as e:
            return (json.loads(e.content))

        except Exception as e:
            logger.error("FN:GrantRoleForPolicyTags_execute error:{}".format(traceback.format_exc()))
            return response_code.ADD_DATA_FAIL
        finally:
            conn.close()

    def __get_adgroup_service_accout(self, workspace_id, usecase_name, db_name, conn):

        service_account = None
        ad_group_list = []

        cond = "WORKSPACE_ID='%s' and USECASE_NAME='%s'" % (
            workspace_id, usecase_name)
        sql = self.create_select_sql(db_name, 'usecaseTable', 'ID,SERVICE_ACCOUNT', cond)
        logger.debug("FN:GrantRoleForPolicyTags__get_adgroup_service_accout usecaseTable_sql:{}".format(sql))
        usecase_info = self.execute_fetch_one(conn, sql)

        if not usecase_info:
            data = response_code.GET_DATA_FAIL
            data['msg'] = 'Cannot find usecase: {}'.format(
                '.'.join([str(workspace_id), str(usecase_name)]))
            return data

        service_account = usecase_info['SERVICE_ACCOUNT']
        # get ad group
        condition = 'USECASE_ID="%s"' % usecase_info['ID']
        relation_tables = [
            {'table_name': 'adgroupTable', 'join_condition': 'adgroupTable.ID=usecase_to_adgroupTable.AD_GROUP_ID'}
        ]
        sql = self.create_get_relation_sql(db_name, 'usecase_to_adgroupTable', 'GROUP_MAIL', relations=relation_tables,
                                           condition=condition)
        logger.debug("FN:GrantRoleForPolicyTags__get_adgroup_service_accout usecase_to_adgroupTable_sql:{}".format(sql))
        ad_group_infos = self.execute_fetch_all(conn, sql)

        for ad_group in ad_group_infos:
            ad_group_list.append(ad_group['GROUP_MAIL'])

        data = response_code.SUCCESS
        data['data'] = {'sa': service_account, 'ad_group_list': ad_group_list}
        return data

    def __grand_access_roles(self, service_account, ad_group_list, project_id, dataset_id, table_id, fields, db_name, conn):
        try:
            access_roles = ['roles/datacatalog.categoryFineGrainedReader']
            # # default access json
            if service_account:
                access_json = {'roles/datacatalog.categoryFineGrainedReader': ['serviceAccount:{}'.format(service_account)]}
            else:
                access_json = {'roles/datacatalog.categoryFineGrainedReader': []}
            for ad_group in ad_group_list:
                access_json['roles/datacatalog.categoryFineGrainedReader'].append('group:{}'.format(ad_group))

            logger.debug("FN:GrantRoleForPolicyTags__grand_access_roles access_json:{} fields:{}".format(access_json, fields))
            credentials, project = google.auth.default()
            service = googleapiclient.discovery.build(
                'datacatalog', 'v1beta1', credentials=credentials)
            success_tag_policy_list = []
            failed_policy_tag_policy_list = []
            for field_info in fields:
                if 'policyTags' not in field_info or 'names' not in field_info['policyTags']:
                    continue
                field_policy_tags = field_info['policyTags']['names']
                for policy_tag_id in field_policy_tags:

                    condition = "id=%s" % policy_tag_id
                    sql = self.create_select_sql(db_name, 'policyTagsTable', 'gcp_policy_tag_id', condition=condition)
                    logger.debug("FN:GrantRoleForPolicyTags__grand_access_roles policyTagsTable_sql:{}".format(sql))
                    gcp_policy_tag_id = self.execute_fetch_one(conn, sql)['gcp_policy_tag_id']
                    logger.debug("FN:GrantRoleForPolicyTags__grand_access_roles gcp_policy_tag_id:{}".format(gcp_policy_tag_id))

                    try:
                        policy_tag_policy = service.projects().locations().taxonomies().policyTags().getIamPolicy(
                            resource=gcp_policy_tag_id
                        ).execute()
                        if 'etag' not in policy_tag_policy:
                            return 'Get policy tags failed for: {}'.format(gcp_policy_tag_id)

                        if 'bindings' not in policy_tag_policy and 'etag' in policy_tag_policy:
                            policy_tag_policy['bindings'] = []

                        category_fine_grained_reader_flag = 0
                        for index, role_info in enumerate(policy_tag_policy['bindings']):
                            role = role_info['role']
                            if role == access_roles[0]:
                                category_fine_grained_reader_flag = 1
                                now_members = policy_tag_policy['bindings'][index]['members']
                                logger.debug("FN:GrantRoleForPolicyTags__grand_access_roles now_members:{} access_json_role:{}".format(now_members, access_json[role]))
                                now_members.extend(access_json[role])
                                policy_tag_policy['bindings'][index]['members'] = list(set(now_members))

                        if category_fine_grained_reader_flag == 0:
                            role = access_roles[0]
                            policy_tag_policy['bindings'].append({'role': role,
                                                             'members': access_json[role]})

                        logger.debug("FN:GrantRoleForPolicyTags__grand_access_roles policy_tag_policy:{}".format(policy_tag_policy))
                        return_policy_tag_policy = service.projects().locations().taxonomies().policyTags().setIamPolicy(
                            resource=gcp_policy_tag_id,
                            body={'policy': policy_tag_policy}
                        ).execute()
                        logger.debug("FN:GrantRoleForPolicyTags__grand_access_roles return_policy_tag_policy:{}".format(return_policy_tag_policy))
                        success_tag_policy_list.append(str(policy_tag_id))

                    except:
                        logger.error("FN:GrantRoleForPolicyTags__grand_access_roles failed_policy_tag_policy_error:{}".format(policy_tag_id))
                        logger.error("FN:GrantRoleForPolicyTags__grand_access_roles error:{}".format(traceback.format_exc()))
                        failed_policy_tag_policy_list.append(str(policy_tag_id))

            return success_tag_policy_list, failed_policy_tag_policy_list

        except:
            logger.error("FN:GrantRoleForPolicyTags__grand_access_roles error:{}".format(traceback.format_exc()))
            return None
            