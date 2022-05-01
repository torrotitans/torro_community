#!/usr/bin/python
# -*- coding: UTF-8 -*

from utils.api_version_verify import api_version
from utils.api_version_verify import api_version
import traceback
from flask import request
from flask_restful import Resource
from core.dashboard_singleton import dashboard_singleton
from utils.status_code import response_code
from common.common_model_enum import modelEnum
from common.common_response_process import response_result_process
from common.common_login_helper import login_required
from common.common_request_process import req
from db.dashboard.db_dashboard_parameter import dashboardApiPara
import traceback
import logging

logger = logging.getLogger("main." + __name__)

class interfaceDashboard(Resource):

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
                workspace_id = req.get_workspace_id()
                # logger.debug('FN:interfaceDashboard_postuser id:{}'.format(user_key))
                data = dashboard_singleton.get_data(user_key, request_data, workspace_id)
                # logger.debug('FN:interfaceDashboard_post data:{}'.format(data))

                if data['code'] == 200:
                    response_data = data['data']
                    data['data'] = req.verify_all_param(response_data, dashboardApiPara.get_input_form_data_POST_response)

            except:
                data = response_code.GET_DATA_FAIL
                data['msg'] = 'Token error or expired, please login again.'
                logger.error('FN:interfaceDashboard_post error_data:{}'.format(data))
                logger.error("FN:interfaceDashboard_post error:{}".format(traceback.format_exc()))

            return response_result_process(data, xml=xml)

        except Exception as e:
            logger.error("FN:interfaceDashboard_post error:{}".format(traceback.format_exc()))
            error_data = response_code.GET_DATA_FAIL
            return response_result_process(error_data, xml=xml)

# logger.error("FN: error:{}".format(traceback.format_exc()))
# logger.debug("FN: error:{}".format())