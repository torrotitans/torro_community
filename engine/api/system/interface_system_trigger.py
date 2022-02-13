#!/usr/bin/python
# -*- coding: UTF-8 -*

from utils.smtp_helper import notify_approvers
import traceback
from flask import request
from flask_restful import Resource
from core.governance_singleton import governance_singleton
from utils.log_helper import lg
from utils.status_code import response_code
from common.common_model_enum import modelEnum
from common.common_response_process import response_result_process
from common.common_request_process import req
from db.gcp.task_operator import taskOperator

class interfaceSystemTrigger(Resource):


    def post(self,):
        xml = request.args.get('format')
        try:
            request_data = req.request_process(request, xml, modelEnum.department.value)
            if isinstance(request_data, bool):
                request_data = response_code.REQUEST_PARAM_FORMAT_ERROR
                return response_result_process(request_data, xml=xml)


            # request_data = req.verify_all_param(request_data, governanceApiPara.changeStatus_POST_request)
            print('request_data:', request_data)
            admin_info = governance_singleton.get_admin_user_info()
            user_key = admin_info.get('ACCOUNT_NAME')
            account_id = admin_info.get('ID')
            # exit(0)
            form_id = request_data['form_id']
            input_form_id = request_data['input_form_id']
            workspace_id = request_data['workspace_id']
            token = request_data.get('token', '')
            # # print('user id:', user_key)
            # change status
            data = governance_singleton.system_approval_trigger(user_key, account_id, request_data)
            # print('change status data: ', data)
            # if begin to execute task
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
                return_msg_list = taskOperator.execute_tasks(gcp_tasks, workspace_id, form_id,input_form_id, user_key)
                data1 = governance_singleton.updateTask(user_key, account_id, input_form_id, workspace_id, tasks, return_msg_list)
                data = response_code.SUCCESS



            # email notification
            if 'data' in data and 'notice_ids' in data['data']:
                notice_ids = data['data']['notice_ids']
                text = ''
                if 'msg' in data:
                    text = data['msg']
                data2 = notify_approvers(data['data']['history_id'], notice_ids, text=text)
                if data2['code'] == 200:
                    data = response_code.SUCCESS
                else:
                    data = response_code.UPDATE_DATA_FAIL
                    data['msg'] = 'Create new form success, fail to send email to approves'

            return response_result_process(data, xml=xml)
        except Exception as e:
            lg.error(traceback.format_exc())
            error_data = response_code.GET_DATA_FAIL
            return response_result_process(error_data, xml=xml)
