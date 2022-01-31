#!/usr/bin/python
# -*- coding: UTF-8 -*

from utils.api_version_verify import api_version
from flask import request
from flask_restful import Resource
from core.workflow_singleton import workflowSingleton_singleton
from utils.log_helper import lg
from utils.status_code import response_code
from common.common_model_enum import modelEnum
from common.common_response_process import response_result_process
from common.common_login_helper import login_required
from common.common_request_process import req
import traceback
class interfaceStages(Resource):

    # @api_version
    @login_required
    def get(self, ):
        xml = request.args.get('format')
        try:
            data = workflowSingleton_singleton.get_all_stages()
            # print(data)
            body = modelEnum.department.value.get('body')
            return response_result_process(data, xml_structure_str=body, xml=xml)
        except Exception as e:
            lg.error(e)
            error_data = response_code.GET_DATA_FAIL
            return response_result_process(error_data, xml=xml)

    # @login_required
    def post(self,):
        xml = request.args.get('format')
        request_data = req.request_process(request, xml, modelEnum.department.value)
        # # print('request: ', request_data)

        if isinstance(request_data, bool):
            request_data = response_code.REQUEST_PARAM_FORMAT_ERROR
            return response_result_process(request_data, xml=xml)

        # request_data = req.verify_all_param(request_data, inputFormApiPara.input_form_data_POST_request)
        workspace_id = req.get_workspace_id()
        try:
            user_key = req.get_user_key()
            # print('user id:', user_key)
        except:
            data = response_code.GET_DATA_FAIL
            # print(traceback.format_exc())
            data['msg'] = 'Token error or expired, please login again.'
            return response_result_process(data, xml=xml)
        try:
            data = workflowSingleton_singleton.get_all_stages_v2(request_data['workflow_id'])
        except:
            data = response_code.GET_DATA_FAIL
            data['msg'] = 'Something went wrong. Please double check your input.'

            lg.error(traceback.format_exc())
        # # print(data)
        return response_result_process(data, xml=xml)
