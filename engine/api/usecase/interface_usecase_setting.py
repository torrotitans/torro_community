#!/usr/bin/python
# -*- coding: UTF-8 -*

from utils.api_version_verify import api_version
import os
import traceback
from flask import request
from flask_restful import Resource
from core.usecase_singleton import usecaseSingleton_singleton
from utils.status_code import response_code
from common.common_model_enum import modelEnum
from common.common_response_process import response_result_process
from common.common_login_helper import login_required
from common.common_request_process import req
from db.usecase.db_usecase_parameter import usecaseApiPara
import traceback
import logging

logger = logging.getLogger("main." + __name__)

class interfaceUseCaseSetting(Resource):

    @login_required
    def post(self,):
        xml = request.args.get('format')
        try:
            request_data = req.request_process(request, xml, modelEnum.department.value)
            if isinstance(request_data, bool):
                request_data = response_code.REQUEST_PARAM_FORMAT_ERROR
                return response_result_process(request_data, xml=xml)
            # if not request_data:
            #     data = response_code.REQUEST_PARAM_MISSED
            #     return response_result_process(data, xml=xml)
            # # print(request_data)
            # # print('usecaseApiPara.setUseCase_POST_request', usecaseApiPara.setUseCase_POST_request)

            request_data = req.verify_all_param(request_data, usecaseApiPara.setUseCase_POST_request)
            data = usecaseSingleton_singleton.add_new_usecase_setting(request_data)
            if data['code'] == 200:
                response_data = data['data']
                data['data'] = req.verify_all_param(response_data, usecaseApiPara.setUseCase_POST_response)
            # # print(data)
            return response_result_process(data, xml=xml)

        except Exception as e:
            logger.error("FN:interfaceUseCaseSetting_post error:{}".format(traceback.format_exc()))
            error_data = response_code.ADD_DATA_FAIL
            return response_result_process(error_data, xml=xml)


    # update the usecase info
    @login_required

    def put(self,):
        xml = request.args.get('format')
        try:
            request_data = req.request_process(request, xml, modelEnum.department.value)
            # # print('request_data:', request_data)
            if isinstance(request_data, bool):
                request_data = response_code.REQUEST_PARAM_FORMAT_ERROR
                return response_result_process(request_data, xml=xml)
            try:
                f = request.files['admin_sa_path']
                upload_path = './data/usecase/'
                if not os.path.exists(upload_path):
                    os.makedirs(upload_path)
                upload_path += f.filename
                f.save(upload_path)
                request_data['admin_sa_path'] = upload_path
            except:
                pass
            request_data = req.verify_all_param(request_data, usecaseApiPara.updateUseCase_POST_request)

            data = usecaseSingleton_singleton.update_usecase(request_data)
            if data['code'] == 200:
                response_data = data['data']
                data['data'] = req.verify_all_param(response_data, usecaseApiPara.updateUseCase_POST_response)
            # # print(data)
            return response_result_process(data, xml=xml)

        except Exception as e:
            logger.error("FN:interfaceUseCaseSetting_put error:{}".format(traceback.format_exc()))
            error_data = response_code.ADD_DATA_FAIL
            return response_result_process(error_data, xml=xml)
