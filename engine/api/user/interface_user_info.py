#!/usr/bin/python
# -*- coding: UTF-8 -*

from utils.api_version_verify import api_version
import traceback
from flask import request
from flask_restful import Resource
from core.user_singleton import userSingleton_singleton
from utils.status_code import response_code
from common.common_model_enum import modelEnum
from common.common_response_process import response_result_process
from common.common_login_helper import login_required
from common.common_request_process import req
from db.user.db_user_parameter import userApiPara
import traceback
import logging

logger = logging.getLogger("main." + __name__)

class interfaceUserInfo(Resource):

    # @api_version
    @login_required
    def get(self):
        xml = request.args.get('format')
        try:

            # if not request_data:
            #     data = response_code.REQUEST_PARAM_MISSED
            #     return response_result_process(data, xml=xml)
            try:
                user_key = req.get_user_key()
                workspace_id = req.get_workspace_id()
                # print('user id:', user_key)
            except:
                data = response_code.GET_DATA_FAIL
                # print(traceback.format_exc())
                data['msg'] = 'Token error or expired, please login again.'
                return response_result_process(data, xml=xml)
            # exit(0)
            data = userSingleton_singleton.fetch_user_info(user_key, workspace_id)
            if data['code'] == 200:
                response_data = data['data']
                data['data'] = req.verify_all_param(response_data, userApiPara.fetchUserInfo_GET_response)
            return response_result_process(data, xml=xml)
            
        except Exception as e:
            logger.error("FN:interfaceUserInfo_get error:{}".format(traceback.format_exc()))
            error_data = response_code.GET_DATA_FAIL
            return response_result_process(error_data, xml=xml)


class testingDetailUser():

    # @api_version
    # @login_required
    # def get(self, ):
    #     xml = request.args.get('userat')
    #     try:
    #         data = userSingleton_singleton.get_all_fields()
    #         body = modelEnum.user.value.get('body')
    #         return response_result_process(data, xml_structure_str=body, xml=xml)
    #     except Exception as e:
    #         lg.error(e)
    #         error_data = response_code.GET_DATA_FAIL
    #         return response_result_process(error_data, xml=xml)

    def post(self, request_data):
        xml = None
        try:
            # request_data = req.request_process(request, xml, modelEnum.department.value)
            if isinstance(request_data, bool):
                request_data = response_code.REQUEST_PARAM_FORMAT_ERROR
                return response_result_process(request_data, xml=xml)
            if not request_data:
                data = response_code.REQUEST_PARAM_MISSED
                return response_result_process(data, xml=xml)
            fields = ['id']
            must = req.verify_all_param_must(request_data, fields)
            if must:
                return response_result_process(must, xml=xml)
            par_type = {'id': int}
            param_type = req.verify_all_param_type(request_data, par_type)
            if param_type:
                return response_result_process(param_type, xml=xml)
            user_id = request_data.get('id')
            data = userSingleton_singleton.get_details_user_by_id(user_id)
            return response_result_process(data, xml=xml)

        except Exception as e:
            logger.error("FN:testingDetailUser_post error:{}".format(traceback.format_exc()))
            error_data = response_code.GET_DATA_FAIL
            return response_result_process(error_data, xml=xml)
