#!/usr/bin/python
# -*- coding: UTF-8 -*

from core.gcp_singleton import gcpSingleton_singleton
from utils.status_code import response_code
from flask import request
from common.common_request_process import req
from core.governance_singleton import governance_singleton
from common.common_model_enum import modelEnum
from common.common_response_process import response_result_process
from common.common_login_helper import login_required
from db.gcp.db_gcp_parameter import gcpApiPara
from db.gcp.task_operator import taskOperator
from flask_restful import Resource
import traceback
import logging

logger = logging.getLogger("main." + __name__)

class interfaceGCPExecute(Resource):

    @login_required
    def post(self,):
        try:

            user_key = req.get_user_key()
            account_id = req.get_user_account_id()
            workspace_id = req.get_workspace_id()

            xml = request.args.get('format')

            request_data = req.request_process(request, xml, modelEnum.department.value)
            if isinstance(request_data, bool):
                request_data = response_code.REQUEST_PARAM_FORMAT_ERROR
                return response_result_process(request_data, xml=xml)

            request_data = req.verify_all_param(request_data, gcpApiPara.execute_gcp_tasks_POST_request)
            input_form_id = request_data.get('input_form_id', None)
            form_id = request_data.get('form_id', None)
            tasks_data = gcpSingleton_singleton.get_gcp_tasks(form_id, input_form_id)

            logger.info('FN:interfaceGCPExecute_post gcp_tasks_data:{}'.format(tasks_data))

            for data in tasks_data:
                if data['code'] == 200:
                    gcp_tasks = data['data']['gcp_tasks']
                    tasks = data['data']['tasks']
                    form_id = data['data']['form_id']
                    input_form_id = data['data']['input_form_id']
                    return_msg_list = taskOperator.execute_tasks(gcp_tasks, workspace_id, form_id,input_form_id, user_key)
                    _ = governance_singleton.updateTask(user_key, account_id, input_form_id,workspace_id, tasks, return_msg_list)
                else:
                    return data

            return response_code.SUCCESS

        except Exception as e:
            logger.error("FN:interfaceGCPExecute_post error:{}".format(traceback.format_exc()))
            error_data = response_code.GET_DATA_FAIL
            return error_data



