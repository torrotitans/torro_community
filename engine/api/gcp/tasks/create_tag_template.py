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
import copy
from config import config
from core.form_singleton import formSingleton_singleton
from core.workflow_singleton import workflowSingleton_singleton

config_name = os.getenv('FLASK_CONFIG') or 'default'
Config = config[config_name]


# class CreateTagTemplate(baseTask):
class CreateTagTemplate(baseTask, DbBase):
    api_type = 'gcp'
    api_name = 'CreateTagTemplate'
    arguments = {
        "tag_template_display_name": {"type": str, "default": ''},
        'description': {"type": str, "default": ''},
        "field_list": {"type": list, "default": []},
    }
    role_list = ['roles/datacatalog.categoryAdmin', 'roles/datacatalog.tagTemplateCreator',
                 'roles/datacatalog.tagTemplateOwner', 'roles/datacatalog.admin']

    def __init__(self, stage_dict):
        super(CreateTagTemplate, self).__init__(stage_dict)
        # # print('self.stage_dict:', self.stage_dict)

        self.full_resource_name = None
        self.target_project = Config.DEFAULT_PROJECT

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
                credentials, project = google.auth.default()
                location = Config.DEFAULT_REGION
                service = googleapiclient.discovery.build(
                    'datacatalog', 'v1beta1', credentials=credentials)
                tag_template_name = self.stage_dict['tag_template_display_name']
                tag_template_id = tag_template_name.replace(' ', '_').lower().strip()
                description = self.stage_dict['description']
                field_list = self.stage_dict['field_list']
                response = self.__get_tag_templates(tag_template_id, location, project, service)
                # print('response field_list:', field_list)
                if 'error' not in response and 'code' not in response['error']:
                    return 'data catalog exist.'
                tag_template_body = {'displayName': tag_template_name, 'fields': {}}
                fields = {}
                field_tamplate = {'displayName': '', 'type': {'primitiveType': ''},
                                  'description': '', 'order': 1}
                create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                for index, field_info in enumerate(field_list):
                    style = int(field_info['style'])
                    label = field_info['label']
                    label = label.replace(' ', '_').replace('/', 'or').replace('&', 'and').replace('&', 'and').replace('!', '').replace(',', '').replace('@', '').replace('$', '').replace('#', '').replace('^', '')
                    field_id = label.lower().strip()
                    des = field_info['des']

                    field = copy.deepcopy(field_tamplate)
                    field['displayName'] = label
                    field['description'] = des
                    field['order'] = index + 1
                    if style == 5:
                        field['type']['primitiveType'] = 'BOOL'
                    elif style == 2:
                        del field['type']['primitiveType']
                        options = []
                        for option in field_info['options']:
                            options.append({"displayName": option['value']})
                        field['type']['enumType'] = {'allowedValues': options}
                    elif style == 1 or style == 3:
                        field['type']['primitiveType'] = 'STRING'
                    elif style == 6:
                        field['type']['primitiveType'] = 'TIMESTAMP'
                    else:
                        continue
                    fields[field_id] = field
                tag_template_body['fields'] = fields
                # print('tag_template_body:', tag_template_body)
                tag_template = service.projects().locations().tagTemplates().create(
                    parent='projects/{project}/locations/{location}'.format(project=project, location=location),
                    tagTemplateId=tag_template_id,
                    body=tag_template_body
                ).execute()
                # print('tag_template', tag_template)
                # create form and get the form id
                tag_tempalte_form_id = self.__create_tag_template_form(workspace_id)
                # self.__create_tag_template_workflow(tag_tempalte_form_id, user_id)
                tag_template_fields = (
                    'workspace_id', 'input_form_id', 'creator_id', 'project_id', 'location', 'display_name',
                    'tag_template_form_id',
                    'tag_template_id', 'field_list', 'description', 'create_time')
                values = (
                    workspace_id, input_form_id, user_id, project, location, tag_template_name, tag_tempalte_form_id,
                    tag_template_id,
                    json.dumps(tag_template_body), description, create_time)
                sql = self.create_insert_sql(db_name, 'tagTemplatesTable',
                                             '({})'.format(', '.join(tag_template_fields)), values)
                tag_template_id = self.insert_exec(conn, sql, return_insert_id=True)
                # print('tagTemplatesTable insert sql:', sql)

                return 'create successfully.: {}'.format(str(tag_template_id))

        except HttpError as e:
            return (json.loads(e.content))
        except Exception as e:
            lg.error(e)
            import traceback
            # print(traceback.format_exc())
            return response_code.ADD_DATA_FAIL
        finally:
            conn.close()
            # pass

    def __create_tag_template_form(self, workspace_id):

        # create form
        form_name = self.stage_dict['tag_template_display_name']
        description = self.stage_dict['description']
        field_list = self.stage_dict['field_list']
        form = {'title': form_name, 'des': description, 'fieldList': field_list, 'hide': 1}
        # print('form:', form)
        data = formSingleton_singleton.add_new_form(form, workspace_id)
        print('*tags table data:', data)
        if data['code'] == 200:
            tag_tempalte_form_id = data['data']['id']


        else:
            tag_tempalte_form_id = None

        return tag_tempalte_form_id

    def __create_tag_template_workflow(self, form_id, creator_id):
        workflow = {'form_id': form_id, 'workflow_name': 'default workflow', 'stages': [
            {"apiTaskName": "", "condition": [], "flowType": "Trigger", "id": 407, "label": "Form | data tags188"},
            {"apiTaskName": "", "condition": [{"id": 1, "label": "workspace owner approval", "style": 6, "value": ""}],
             "flowType": "Approval", "id": 2, "label": "Approval Process"},
            {"apiTaskName": "system_create_tag", "condition": [], "flowType": "System", "id": 14,
             "label": "Create Tags"}],
                    'creator_id': creator_id, 'field_id_list': []}
        workflowSingleton_singleton.add_new_workflow(workflow)

    def __get_tag_templates(self, tag_template_name, location, project, service):

        try:
            tag_template = service.projects().locations().tagTemplates().get(
                name='projects/{project}/locations/{location}/tagTemplates/{tagtemplate}'.format(
                    project=project, location=location, tagtemplate=tag_template_name),
            ).execute()

            return tag_template

        except HttpError as e:
            return (json.loads(e.content))
        except Exception as e:
            return {'error': {'code': 500, 'message': str(e), 'status': 'ERROR'}}


if __name__ == '__main__':
    x = CreateTagTemplate({"tag_template_display_name": 'Create Tag Templates Api',
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
