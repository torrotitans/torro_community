#!/usr/bin/python
# -*- coding: UTF-8 -*

from utils.api_version_verify import api_version
from utils.api_version_verify import api_version
import traceback
from flask import request
from flask_restful import Resource
from core.input_form_singleton import input_form_singleton
from utils.status_code import response_code
from common.common_model_enum import modelEnum
from common.common_response_process import response_result_process
from common.common_login_helper import login_required
from common.common_request_process import req
from db.dashboard.db_dashboard_parameter import dashboardApiPara
import traceback
import logging

logger = logging.getLogger("main." + __name__)

class interfaceInputFormDetails(Resource):
    # @api_version
    # @login_required
    @login_required
    def post(self,):
        xml = request.args.get('format')
        try:
            request_data = req.request_process(request, xml, modelEnum.department.value)
            if isinstance(request_data, bool):
                request_data = response_code.REQUEST_PARAM_FORMAT_ERROR
                return response_result_process(request_data, xml=xml)

            request_data = req.verify_all_param(request_data, dashboardApiPara.get_input_form_data_POST_request)

            try:
                user_key = req.get_user_key()
                account_id = req.get_user_account_id()
                input_form_id = request_data.get('id')
                approver_view = request_data.get('approverView', False)
                logger.debug("FN:interfaceInputFormDetails_post user_key:{} account_id:{} \
                    input_form_id:{} approver_view:{}".format(user_key,account_id,input_form_id,approver_view))
                
                data = input_form_singleton.get_input_form_data(account_id, input_form_id, approver_view)
                if data['code'] == 200:
                    response_data = data['data']
                    data['data'] = req.verify_all_param(response_data, dashboardApiPara.get_input_form_data_POST_response)

                logger.debug("FN:interfaceInputFormDetails_post data:{}".format(data))
                
            except:
                data = response_code.GET_DATA_FAIL
                data['msg'] = 'Token error or expired, please login again.'
                logger.error("FN:interfaceInputFormDetails_post data_error:{}".format(data))
                logger.error("FN:interfaceInputFormDetails_post error:{}".format(traceback.format_exc()))

            return response_result_process(data, xml=xml)

        except Exception as e:
            logger.error("FN:interfaceInputFormDetails_post error:{}".format(traceback.format_exc()))
            error_data = response_code.GET_DATA_FAIL
            return response_result_process(error_data, xml=xml)

class interfaceInputFormDetailsList(Resource):
    # @api_version
    # @login_required
    @login_required
    def post(self,):
        xml = request.args.get('format')
        try:
            request_data = req.request_process(request, xml, modelEnum.department.value)
            if isinstance(request_data, bool):
                request_data = response_code.REQUEST_PARAM_FORMAT_ERROR
                return response_result_process(request_data, xml=xml)

            request_data = req.verify_all_param(request_data, dashboardApiPara.get_input_form_data_POST_request)

            try:
                user_key = req.get_user_key()
            except:
                data = response_code.GET_DATA_FAIL
                data['msg'] = 'Token error or expired, please login again.'
                logger.error("FN:interfaceInputFormDetailsList_post data_error:{}".format(data))
                return response_result_process(data, xml=xml)

            input_form_id_list = request_data.get('idList')
            # print('user id:', user_key)
            data = response_code.SUCCESS
            data['data'] = []
            for input_form_id in input_form_id_list:
                one_data = input_form_singleton.get_input_form_data(user_key, input_form_id)
                if one_data['code'] == 200:
                    response_data = one_data['data']
                    # response_data = req.verify_all_param(response_data, dashboardApiPara.get_input_form_data_POST_response)
                    data['data'].append(response_data)
                else:
                    data['data'].append(None)

            logger.debug("FN:interfaceInputFormDetailsList_post data:{}".format(data))
            return response_result_process(data, xml=xml)

        except Exception as e:
            logger.error("FN:interfaceInputFormDetailsList_post error:{}".format(traceback.format_exc()))
            error_data = response_code.GET_DATA_FAIL
            return response_result_process(error_data, xml=xml)
