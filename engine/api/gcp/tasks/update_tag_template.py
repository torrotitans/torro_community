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
import copy
from config import config
from core.form_singleton import formSingleton_singleton
from core.workflow_singleton import workflowSingleton_singleton
import random
import traceback
import logging

logger = logging.getLogger("main." + __name__)
config_name = os.getenv('FLASK_CONFIG') or 'default'
Config = config[config_name]

# class UpdateTagTemplate(baseTask):
class UpdateTagTemplate(baseTask):
    api_type = 'gcp'
    api_name = 'UpdateTagTemplate'
    arguments = {
        "tag_template_form_id": {"type": int, "default": -1},
        "tag_template_display_name": {"type": str, "default": ''},
        'description': {"type": str, "default": ''},
        "field_list": {"type": list, "default": []},
    }
    role_list = ['roles/datacatalog.categoryAdmin', 'roles/datacatalog.tagTemplateCreator',
                 'roles/datacatalog.tagTemplateOwner', 'roles/datacatalog.admin']

    def __init__(self, stage_dict):
        super(UpdateTagTemplate, self).__init__(stage_dict)
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
                data = response_code.BAD_REQUEST
                data['msg'] = 'Missing parameters: {}'.format(', '.join(missing_set))
                return data
            else:
                credentials, project = google.auth.default()
                location = Config.DEFAULT_REGION
                service = googleapiclient.discovery.build(
                    'datacatalog', 'v1beta1', credentials=credentials)
                tag_template_name = self.stage_dict['tag_template_display_name']
                tag_template_id = tag_template_name.replace(' ', '_').lower().strip()
                description = self.stage_dict['description']
                field_list = self.stage_dict['field_list']
                new_tag_template_id = tag_template_id +'_'+str(random.randint(1,100))
                response = self.__get_tag_templates(new_tag_template_id, location, project, service)
                retry = 0
                while retry < 3:
                    # print('response field_list:', field_list)
                    if 'error' not in response and 'code' not in response['error']:
                        new_tag_template_id = tag_template_id +'_'+str(random.randint(1,100))
                        response = self.__get_tag_templates(new_tag_template_id, location, project, service)
                        retry += 1
                    else:
                        break
                if 'error' not in response and 'code' not in response['error']:
                    data = response_code.BAD_REQUEST
                    data['msg'] = 'data catalog exist.'
                    return data
                
                tag_template_body = {'displayName': tag_template_name, 'fields': {}}
                fields = {}
                field_tamplate = {'displayName': '', 'type': {'primitiveType': ''},
                                  'description': '', 'order': 1}
                create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                for index, field_info in enumerate(field_list):
                    style = int(field_info['style'])
                    label = field_info['label']
                    field_id = label.replace(' ', '_').lower().strip()
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
                    tagTemplateId=new_tag_template_id,
                    body=tag_template_body
                ).execute()
                # print('tag_template', tag_template)
                # create form and get the form id
                old_tag_template_form_id = self.stage_dict['tag_template_form_id']
                tag_tempalte_form_id = self.__update_tag_template_form(user_id, workspace_id)
                # self.__create_tag_template_workflow(tag_tempalte_form_id, user_id)
                tag_template_fields = (
                    'project_id', 'location', 'display_name',
                    'tag_template_form_id',
                    'tag_template_id', 'field_list', 'description', 'create_time')
                values = (
                    project, location, tag_template_name, tag_tempalte_form_id,
                    new_tag_template_id,
                    json.dumps(tag_template_body), description, create_time)
                condition = "(workspace_id='%s' or workspace_id=0) and tag_template_form_id='%s'" % (
                workspace_id, old_tag_template_form_id)
                sql = self.create_update_sql(db_name, 'tagTemplatesTable',
                                             tag_template_fields, values, condition=condition)
                logger.debug("FN:UpdateTagTemplate_execute update_tagTemplatesTable_sql:{}".format(sql))
                tag_template_id = self.updete_exec(conn, sql)
                # print('tagTemplatesTable insert sql:', sql)

                data = response_code.SUCCESS
                data['data'] = 'update successfully.: {}'.format(str(tag_template_id))
                return data
            # self.
        except HttpError as e:
            error_json = json.loads(e.content, strict=False)
            data = error_json['error']
            data["msg"] = data.pop("message")
            logger.error("FN:UpdateTagTemplate_execute error:{}".format(traceback.format_exc()))
            return data
        except Exception as e:
            logger.error("FN:UpdateTagTemplate_execute error:{}".format(traceback.format_exc()))
            data = response_code.BAD_REQUEST
            data['msg'] = str(e)
            return data

        finally:
            conn.close()

    def __update_tag_template_form(self, user_id, workspace_id):

        # create form
        id = self.stage_dict['tag_template_form_id']
        form_name = self.stage_dict['tag_template_display_name']
        description = self.stage_dict['description']
        field_list = self.stage_dict['field_list']
        form = {'title': form_name, 'des': description, 'fieldList': field_list, 'id': id}
        # print('form:', form)
        data = formSingleton_singleton.update_form(form, user_id, workspace_id)
        logger.debug("FN:UpdateTagTemplate__update_tag_template_form tag_table_data:{}".format(data))
        
        if data['code'] == 200:
            tag_tempalte_form_id = data['data']['id']

        else:
            tag_tempalte_form_id = None

        return tag_tempalte_form_id

    def __create_tag_template_workflow(self, form_id, creator_id):
        workflow = {'form_id': form_id, 'workflow_name': 'default workflow', 'stages': [
            {"apiTaskName": "", "condition": [], "flowType": "Trigger", "id": 100, "label": "Form | data tags188"},
            {"apiTaskName": "", "condition": [{"id": 1, "label": "workspace owner approval", "style": 6, "value": ""}],
             "flowType": "Approval", "id": 101, "label": "Approval Process"},
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
            return (json.loads(e.content, strict=False))

        except Exception as e:
            logger.error("FN:UpdateTagTemplate__get_tag_templates error:{}".format(traceback.format_exc()))
            return {'error': {'code': 500, 'message': str(e), 'status': 'ERROR'}}
