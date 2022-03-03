from api.gcp.tasks.baseTask import baseTask
# from google.cloud import datacatalog_v1beta1
import google
from db.base import DbBase
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
import traceback
import logging

logger = logging.getLogger("main." + __name__)
config_name = os.getenv('FLASK_CONFIG') or 'default'
Config = config[config_name]


# class DeleteTagTemplate(baseTask):
class DeleteTagTemplate(baseTask, DbBase):
    api_type = 'gcp'
    api_name = 'DeleteTagTemplate'
    arguments = {
        "tag_template_form_id": {"type": int, "default": -1},
    }
    role_list = ['roles/datacatalog.categoryAdmin', 'roles/datacatalog.tagTemplateCreator',
                 'roles/datacatalog.tagTemplateOwner', 'roles/datacatalog.admin']

    def __init__(self, stage_dict):
        super(DeleteTagTemplate, self).__init__(stage_dict)
        logger.debug('FN:DeleteTagTemplate_init stage_dict:{}'.format(self.stage_dict))

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

            if len(missing_set) != 0:
                return 'Missing parameters: {}'.format(', '.join(missing_set))
            else:
                credentials, project = google.auth.default()
                location = Config.DEFAULT_REGION
                service = googleapiclient.discovery.build(
                    'datacatalog', 'v1beta1', credentials=credentials)
                tag_template_form_id = self.stage_dict['tag_template_form_id']
                condition = "(workspace_id='%s' or workspace_id=0) and tag_template_form_id='%s'" % (workspace_id, tag_template_form_id)
                sql = self.create_select_sql(db_name, 'tagTemplatesTable', '*', condition=condition)
                print('tagTemplatesTable sql:', sql)
                tag_template_info = self.execute_fetch_one(conn, sql)
                if not tag_template_info:
                    return 'Update failed, cannot found the tag template: %s in workspace: %id' % (tag_template_form_id, workspace_id)
                tag_template_id = tag_template_info['tag_template_id']
                # print('tag_template_body:', tag_template_body)
                # tag_template = service.projects().locations().tagTemplates().delete(
                #     name='projects/{project}/locations/{location}/tagTemplates/{tagtemplate}'.format(project=project, location=location, tagtemplate=tag_template_id),
                #     force=False
                # ).execute()

                sql = self.create_delete_sql(db_name, 'tagTemplatesTable', condition=condition)
                tag_template_id = self.delete_exec(conn, sql)

                _ = self.__delete_tag_template_form()

                return 'delete successfully.: {}'.format(str(tag_template_id))

        except HttpError as e:
            return (json.loads(e.content))

        except Exception as e:
            logger.error("FN:DeleteTagTemplate_execute error:{}".format(traceback.format_exc()))
            return response_code.ADD_DATA_FAIL

        finally:
            conn.close()

    def __delete_tag_template_form(self, ):

        # create form
        form_id = self.stage_dict['tag_template_form_id']
        form = {'id': form_id}

        data = formSingleton_singleton.delete_form(form)
        logger.debug('FN:DeleteTagTemplate__delete_tag_template_form tags_table_data:{}'.format(data))
        
        if data['code'] == 200:
            return 'Delete successfully.'
        else:
            return data['msg']

