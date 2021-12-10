#!/usr/bin/python
# -*- coding: UTF-8 -*
"""

"""
from utils.smtp_helper import notify_approvers

from utils.api_version_verify import api_version
import traceback
from flask import request
from flask_restful import Resource
from core.governance_singleton import governance_singleton
from utils.log_helper import lg
from utils.status_code import response_code
from common.common_model_enum import modelEnum
from common.common_response_process import response_result_process
from common.common_login_helper import login_required
from common.common_request_process import req
from db.governance.db_governance_parameter import governanceApiPara
from db.gcp.task_operator import taskOperator

class interfaceGovernance(Resource):
    # @api_version

    @login_required
    def post(self,):
        xml = request.args.get('format')
        try:
            request_data = req.request_process(request, xml, modelEnum.department.value)
            if isinstance(request_data, bool):
                request_data = response_code.REQUEST_PARAM_FORMAT_ERROR
                return response_result_process(request_data, xml=xml)


            request_data = req.verify_all_param(request_data, governanceApiPara.changeStatus_POST_request)

            # try:
            try:
                user_key = req.get_user_key()
                account_id = req.get_user_account_id()
                workspace_id = req.get_workspace_id()
                # print('user id:', user_key)
                # print('account_id:', account_id)
                # print('12334 user workspace_id:', workspace_id)
            except:
                data = response_code.GET_DATA_FAIL
                # print(traceback.format_exc())
                data['msg'] = 'Token error or expired, please login again.'
                return response_result_process(data, xml=xml)
            # exit(0)
            form_id = request_data['form_id']
            input_form_id = request_data['id']
            # # print('user id:', user_key)
            # change status
            data = governance_singleton.change_status(user_key, account_id, request_data)
            # print('change status data: ', data)
            # if begin to execute task
            data1 = response_code.BAD_REQUEST
            # system form operations
            # if data['code'] == 200 and form_id == 2 and data['msg'] == 'request successfully':
            #     data1 = governance_singleton.add_new_usecase(input_form_id, form_id, user_key, workspace_id)
            # if data['code'] == 200 and form_id == 3 and data['msg'] == 'request successfully':
            #     data1 = governance_singleton.add_new_policy_tags(input_form_id, form_id, user_key, workspace_id)
            # trigger gcp task
            if data['code'] == 200 and 'data' in data and 'is_approved' in data['data'] and data['data']['is_approved'] == 1:
            # if data['code'] == 200 and 'data' in data and data['data']['is_approved'] == 1 and data['data']['tasks']\
            #     and data['data']['gcp_tasks']:
                gcp_tasks = data['data'].get('gcp_tasks', [])
                tasks = data['data'].get('tasks', [])
                # gcp_tasks = []
                # miss_role_list = []
                # # print('tasks: ', tasks)
                # for task in tasks:
                #     task_name = task['name']
                #     stage_dict = task['stages']
                #     task = taskFetcher.build_task_object(task_name, stage_dict)
                #     access_flag, role_list = taskOperator.check_roles(task)
                #     miss_role_list.extend(role_list)
                #     gcp_tasks.append(task)
                # if len(miss_role_list) != 0:
                #
                #     data1 = governance_singleton.change_status(user_key, account_id, request_data)
                # else:
                #     return_msg_list = taskOperator.execute_tasks(gcp_tasks)
                return_msg_list = taskOperator.execute_tasks(gcp_tasks, workspace_id, form_id,input_form_id, user_key)
                data1 = governance_singleton.updateTask(user_key, account_id, input_form_id, tasks, return_msg_list)
            else:
                return response_result_process(data, xml=xml)

            return response_result_process(data1, xml=xml)

            # email notification
            if data['code'] == 200 and data1['code'] == 200:
                notice_ids = data['data']['notice_ids']
                data2 = notify_approvers(data1['data']['history_id'], notice_ids)
                if data2['code'] == 200:
                    data['data'] = req.verify_all_param(data['data'], governanceApiPara.changeStatus_POST_response)
                else:
                    data = response_code.UPDATE_DATA_FAIL
                    data['msg'] = 'Create new form success, fail to send email to approves'

            return response_result_process(data, xml=xml)
        except Exception as e:
            lg.error(traceback.format_exc())
            error_data = response_code.GET_DATA_FAIL
            return response_result_process(error_data, xml=xml)
