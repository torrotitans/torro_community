#!/usr/bin/python
# -*- coding: UTF-8 -*

from flask import request, g, make_response
from flask_restful import Resource
# from common.common_log import operation_log
from common.common_model_enum import modelEnum
from common.common_request_process import req
from common.common_response_process import response_result_process, DateEncoder
from db.user.db_user_parameter import userApiPara
from utils.api_version_verify import api_version
from utils.auth_helper import Auth
from utils.log_helper import lg
from utils.status_code import response_code
import json

class interfaceOffine(Resource):

    # @api_version
    def post(self):
        xml = request.args.get('format')
        try:
            request_data = req.request_process(request, xml, modelEnum.login.value)
            if isinstance(request_data, bool):
                request_data = response_code.REQUEST_PARAM_FORMAT_ERROR
                return response_result_process(request_data, xml=xml)
            if not request_data:
                data = response_code.REQUEST_PARAM_MISSED
                return response_result_process(data, xml=xml)
            request_data = req.verify_all_param(request_data, userApiPara.login_POST_request)

            login_name = request_data.get('login_name')
            # # print('login: ', login_name, login_password)
            # 对登录情况进行验证
            success_flag = Auth.get_offline_password(login_name)
            if success_flag:
                data = response_code.SUCCESS
                data['msg'] = 'Your offine login info has sent to your e-mail.'
            else:
                data = response_code.GET_DATA_FAIL
            return response_result_process(data, xml=xml)
        except Exception as e:
            lg.error(e)
            error_data = response_code.GET_DATA_FAIL
            return response_result_process(error_data, xml=xml)
