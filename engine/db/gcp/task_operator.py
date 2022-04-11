import os
import platform
import google.auth
import googleapiclient.discovery
from config import config
from common.common_input_form_status import status as Status
import traceback
import logging
import time
logger = logging.getLogger("main." + __name__)
config_name = os.getenv('FLASK_CONFIG') or 'default'
Config = config[config_name]

task_packages_prefix = 'api.gcp.tasks.'
sys = platform.system()
if sys == 'Windows':
    task_path = os.getcwd()+'\\api\\gcp\\tasks'
else:
    task_path = os.getcwd()+'/api/gcp/tasks'
for task_name in os.listdir(task_path):
    if '__' not in task_name and '.py' in task_name:
        modname = task_packages_prefix+task_name.replace('.py', '')
        import_file = 'from ' + modname + ' import *'
        # # print(import_file)
        exec(import_file)

class taskOperator:

    db_operation = Status.db_operation_tasks

    @staticmethod
    def execute_tasks(task_object_list, workspace_id=None, form_id=None, input_form_id=None, user_id=None):
        try:
            return_msg_list = []
            for index, task_object in enumerate(task_object_list):
                api_name = task_object.api_name
                logger.debug('execute task:', index, api_name)
                # task_object.verify_all_param()
                return_msg = task_object.execute(workspace_id, form_id, input_form_id, user_id)
                # time.sleep(1)
                # if api_name in taskOperator.db_operation:
                #     # print('1234task {} will update db'.format(api_name))
                #     return_msg = task_object.execute(workspace_id, form_id, input_form_id, user_id)
                # else:
                #     return_msg = task_object.execute()
                comment = task_object.message_tranfer(return_msg)
                return_msg_list.append((return_msg, comment))
            return return_msg_list

        except:
            logger.error("FN:taskOperator_execute_tasks error:{}".format(traceback.format_exc()))

        

class taskFetcher:

    credentials, project_id = google.auth.default(scopes=("https://www.googleapis.com/auth/cloud-platform",))
    service = googleapiclient.discovery.build(
        'cloudasset', 'v1p1beta1', credentials=credentials)
    project_resource_name_tamplate = '//cloudresourcemanager.googleapis.com/projects/{}'
    service_account = Config.DEFAULT_SA

    @staticmethod
    def get_service_account_roles(project_id, service_account):
        return None
        roles = taskFetcher.service.iamPolicies().searchAll(
            scope='projects/{}'.format(project_id),
            query='policy:{}'.format(service_account)
        ).execute()
        return roles
    @staticmethod
    def view_grantable_roles(project_id, full_resource_name, resource_role_list=[], service_account=None, sa_roles=None):
        if not service_account:
            service_account = taskFetcher.service_account

        if not sa_roles:
            sa_roles = taskFetcher.get_service_account_roles(project_id, service_account)

        project_resource_name = taskFetcher.project_resource_name_tamplate.format(project_id)

        access_flag = 0
        # print('sa_roles:', sa_roles)
        for role_obj in sa_roles['results']:
            resource_name = role_obj['resource']
            # check project level roles
            if resource_name == project_resource_name:
                for policy_obj in role_obj['policy']['bindings']:
                    if policy_obj['role'] in resource_role_list:
                        # # print("project policy_obj['role']:", policy_obj['role'], resource_role_list)
                        access_flag = 1
                        break
            # if project level roles already enough, break
            if access_flag == 1:
                break
            if resource_name == full_resource_name:
                for policy_obj in role_obj['policy']['bindings']:
                    if policy_obj['role'] in resource_role_list:
                        # # print("resource policy_obj['role']:", policy_obj['role'], resource_role_list)
                        access_flag = 1
                        break
            if access_flag == 1:
                break
        return access_flag

    @staticmethod
    def check_roles(task_object, default_service_account, default_project_sa_roles):
        return 1
        role_list = task_object.role_list
        full_resource_name = task_object.full_resource_name
        project_id = task_object.target_project
        return taskFetcher.view_grantable_roles(project_id, full_resource_name, role_list,
                                                service_account=default_service_account,
                                                sa_roles=default_project_sa_roles)

    @staticmethod
    def build_task_object(apiTaskName, data):
        return globals()[apiTaskName](data)
if __name__ == '__main__':
    # # print(dir())
    x = taskFetcher.build_task_object('CreateGCSBucket', {})
    # print(x)

'''
how to execute:

# 1. init a pools and record user input formInfo & workflowInfo
db_insert
# 2. init the task objects list: stages:list()
task_object_list = []
for stage in stages:
    taskObj = taskFetcher.build_task_object(stage['apiTaskName'], stage['arguments'])
    task_object_list.append(taskObj)
# 3. execute the task queue
return_msg_list = execute_tasks(task_object_list)
# 4. update logs & status
db_update


'''