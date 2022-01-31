#!/usr/bin/python
# -*- coding: UTF-8 -*

from utils.api_version_verify import api_version
import traceback
from flask import request
from flask_restful import Resource
from core.usecase_singleton import usecaseSingleton_singleton
from utils.log_helper import lg
from utils.status_code import response_code
from common.common_model_enum import modelEnum
from common.common_response_process import response_result_process
from common.common_login_helper import login_required
from common.common_request_process import req
from db.usecase.db_usecase_parameter import usecaseApiPara

class interfaceUseCaseInfo(Resource):

    @login_required
    def get(self,):

        xml = request.args.get('format')
        try:
            try:
                user_key = req.get_user_key()
                account_id = req.get_user_account_id()
                workspace_id = req.get_workspace_id()
                # print('user id:', user_key)
                # print('account_id:', account_id)
                # print('workspace_id:', workspace_id)
            except:
                data = response_code.GET_DATA_FAIL
                # print(traceback.format_exc())
                data['msg'] = 'Token error or expired, please login again.'
                return response_result_process(data, xml=xml)
            data = usecaseSingleton_singleton.get_usecase_info_by_ad_group(account_id)
            if data['code'] == 200:
                response_data = data['data']
                data['data'] = req.verify_all_param(response_data, usecaseApiPara.getUsecase_GET_response)
            # # print(data)
            return response_result_process(data, xml=xml)
        except Exception as e:
            lg.error(e)
            error_data = response_code.GET_DATA_FAIL
            return response_result_process(error_data, xml=xml)
    @login_required
    def post(self,):
        xml = request.args.get('format')
        try:
            request_data = req.request_process(request, xml, modelEnum.department.value)
            if isinstance(request_data, bool):
                request_data = response_code.REQUEST_PARAM_FORMAT_ERROR
                return response_result_process(request_data, xml=xml)

            user_key = req.get_user_key()
            account_id = req.get_user_account_id()
            workspace_id = req.get_workspace_id()
            # if not request_data:
            #     data = response_code.REQUEST_PARAM_MISSED
            #     return response_result_process(data, xml=xml)
            # # print(request_data)
            # # print('usecaseApiPara.setUseCase_POST_request', usecaseApiPara.setUseCase_POST_request)
            request_data = req.verify_all_param(request_data, usecaseApiPara.getUseCase_POST_request)
            usecase_id = request_data['id']
            data = usecaseSingleton_singleton.get_usecase_details_info_by_id(workspace_id, usecase_id)
            if data['code'] == 200:
                response_data = data['data']
                data['data'] = req.verify_all_param(response_data, usecaseApiPara.getUseCase_POST_response)
            # # print(data)
            return response_result_process(data, xml=xml)
        except Exception as e:
            lg.error(e)
            # print(traceback.format_exc())
            error_data = response_code.ADD_DATA_FAIL
            return response_result_process(error_data, xml=xml)

