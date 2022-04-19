from api.gcp.tasks.baseTask import baseTask
# from google.cloud import datacatalog_v1beta1
from db.connection_pool import MysqlConn
from utils.log_helper import lg
from utils.status_code import response_code
from config import configuration
from googleapiclient.errors import HttpError
import json
import os
import traceback
from config import config
from google.cloud import bigquery
import traceback
import logging

logger = logging.getLogger("main.api.gcp.tasks" + __name__)
config_name = os.getenv('FLASK_CONFIG') or 'default'
Config = config[config_name]


# class GrantRoleForBQDataset(baseTask):
class GrantRoleForBQDataset(baseTask):
    api_type = 'gcp'
    api_name = 'GrantRoleForBQDataset'
    arguments = {
        "project_id": {"type": str, "default": ''},
        "usecase_name": {"type": str, "default": ''},
        "location": {"type": str, "default": ''},
        'dataset_id_list': {"type": str, "default": ''},
    }
    role_list = ['roles/bigquery.dataOwner', 'roles/bigquery.admin']

    def __init__(self, stage_dict):
        super(GrantRoleForBQDataset, self).__init__(stage_dict)
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
                dataset_id_list = self.stage_dict.get('dataset_id_list', [])
                table_id = '*'
                # get usecase service account & ad group
                data = self.__get_adgroup_service_accout(workspace_id, usecase_name, db_name, conn)
                if data['code'] != 200:
                    return data['msg']
                service_account = data['data']['sa']
                ad_group_list = data['data'].get('ad_group_list', [])
                logger.debug("FN:GrantRoleForBQDataset_execute data:{}".format(data))
                # ad_group_list = []
                # check if already get the table access
                for dataset_id in dataset_id_list:
                    _ = self.__grand_access_roles(service_account, ad_group_list, project_id, dataset_id)

                return 'Get the table access successfully: {}'.format(
                    '.'.join([str(workspace_id), project_id, ','.join(dataset_id_list)]))

        except HttpError as e:
            return (json.loads(e.content))
        except Exception as e:
            logger.error("FN:GrantRoleForBQDataset_execute error:{}".format(traceback.format_exc()))
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

    def __grand_access_roles(self, service_account, ad_group_list, project_id, dataset_id):
        try:
            # # default access json
            if service_account:
                access_json = {'roles/bigquery.dataViewer': ['serviceAccount:{}'.format(service_account)]}
            else:
                access_json = {'roles/bigquery.dataViewer': []}
            for ad_group in ad_group_list:
                # access_json['roles/bigquery.jobUser'].append(('groupByEmail', ad_group))
                access_json['roles/bigquery.dataViewer'].append(('groupByEmail', ad_group))

            logger.debug("FN:GrantRoleForBQDataset__grand_access_roles access_json:{}".format(access_json))


            client = bigquery.Client(project_id)
            dataset = client.get_dataset(dataset_id)
            entries = list(dataset.access_entries)
            new_entries = []
            for role in access_json:
                access_item = access_json[role]
                for entity_type, entity_id in access_item:
                    entry = bigquery.AccessEntry(
                        role=role,
                        entity_type=entity_type,
                        entity_id=entity_id
                    )
                    new_entries.append(entry)
            entries.extend(new_entries)
            dataset.access_entries = entries
            _ = client.update_dataset(dataset, ['access_entries'])


            logger.debug("FN:GrantRoleForBQDataset__grand_access_roles dataset_id_with_modified_permission:{}".format(dataset_id))
            data = response_code.SUCCESS
            data['data'] = "Successful."
            return data
        except HttpError as e:
            error_json = json.loads(e.content)
            data = error_json['error']
            data["msg"] = data.pop("message")
            logger.error("FN:GrantRoleForBQDataset__grand_access_roles error:{}".format(traceback.format_exc()))
            return data
        except Exception as e:
            logger.error("FN:GrantRoleForBQDataset__grand_access_roles error:{}".format(traceback.format_exc()))
            data = response_code.BAD_REQUEST
            data['msg'] = str(e)
            return data



if __name__ == '__main__':
    x = GrantRoleForBQDataset({"tag_template_display_name": 'Create Tag Templates Api',
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
