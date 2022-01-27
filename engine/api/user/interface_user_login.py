#!/usr/bin/python
# -*- coding: UTF-8 -*
"""

"""
import traceback
from flask import request
from flask_restful import Resource
from utils.log_helper import lg
from utils.status_code import response_code
from common.common_model_enum import modelEnum
from common.common_response_process import response_result_process
from common.common_request_process import req


class interfaceUserLogin(Resource):

    # get user token
    def post(self,):
        xml = request.args.get('format')
        '''
        select org_info get login type:
        
        if ldap: check password through ldap api, if true: get info and generate password, update usertable's password for api checking
        if base: check db password, get info from db.
        
        
        '''
        try:
            request_data = req.request_process(request, xml, modelEnum.department.value)
            # print('request_data', request.data)

        except Exception as e:
            lg.error(e)
            # print(traceback.format_exc())
            error_data = response_code.ADD_DATA_FAIL
            return response_result_process(error_data, xml=xml)

    # refresh role permissions to token
    def put(self,):
        xml = request.args.get('format')
        try:
            request_data = req.request_process(request, xml, modelEnum.department.value)
            # # print('request_data:', request_data)
            if isinstance(request_data, bool):
                request_data = response_code.REQUEST_PARAM_FORMAT_ERROR
                return response_result_process(request_data, xml=xml)

        except Exception as e:
            lg.error(e)
            # # print(traceback.format_exc())
            error_data = response_code.ADD_DATA_FAIL
            return response_result_process(error_data, xml=xml)
