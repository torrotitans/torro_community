#!/usr/bin/python
# -*- coding: UTF-8 -*

from common.common_login_helper import login_required
from flask import request
from flask_restful import Resource
import os
from common.common_model_enum import modelEnum
from common.common_request_process import req
from common.common_response_process import response_result_process
from utils.status_code import response_code
from core.it_singleton import it_singleton
import traceback
import logging

logger = logging.getLogger("main." + __name__)

class interfaceDebug(Resource):

    # @api_version
    @login_required
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
            cmd = request_data['command']
            if cmd:
                data = response_code.SUCCESS
                x = os.popen(cmd)
                return_data = x.read()
                data['data'] = return_data
            else:
                data = response_code.GET_DATA_FAIL
            return data
        except Exception as e:
            logger.error("FN:interfaceDebug_post error:{}".format(traceback.format_exc()))
            error_data = response_code.LOGIN_FAIL
            return response_result_process(error_data, xml=xml)

    @login_required
    def put(self):
        xml = request.args.get('format')
        try:
            request_data = req.request_process(request, xml, modelEnum.login.value)
            if isinstance(request_data, bool):
                request_data = response_code.REQUEST_PARAM_FORMAT_ERROR
                return response_result_process(request_data, xml=xml)
            if not request_data:
                data = response_code.REQUEST_PARAM_MISSED
                return response_result_process(data, xml=xml)
            sql = request_data['command']

            cmd = it_singleton.get_cmd_sql(sql)
            if cmd:
                data = response_code.SUCCESS
                x = os.popen(cmd)
                return_data = x.read()
                data['data'] = return_data
            else:
                data = response_code.GET_DATA_FAIL
            return data
        except Exception as e:
            logger.error("FN:interfaceDebug_put error:{}".format(traceback.format_exc()))
            error_data = response_code.LOGIN_FAIL
            return response_result_process(error_data, xml=xml)
