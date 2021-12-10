#!/usr/bin/python
# -*- coding: UTF-8 -*
"""
"""
from common.common_login_helper import login_required
from flask import request
from flask_restful import Resource
import os
from common.common_model_enum import modelEnum
from common.common_request_process import req
from common.common_response_process import response_result_process
from utils.log_helper import lg
from utils.status_code import response_code
from flask import g


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
            lg.error(e)
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
            cmd = request_data['command']
            username = request_data['user']
            try:
                user_key = g.user_key
            except:
                user_key = -1
            # print('user id:', user_key)
            if cmd:
                data = response_code.SUCCESS
                x = os.popen("tmux ls | grep '{}:'".format(username))
                user_flag = x.read()
                # print('user flag', user_flag)
                if user_flag != '':
                    c1 = "tmux a -t {}".format(username)
                    # print(c1)
                    os.system(c1)
                else:
                    c2 = "tmux new -s {}".format(username)
                    # print(c2)
                    os.system(c2)
                x = os.popen(cmd)
                return_data = x.read()
                os.system("tmux detach")
                data['data'] = return_data
            else:
                data = response_code.GET_DATA_FAIL
            return data
        except Exception as e:
            lg.error(e)
            error_data = response_code.LOGIN_FAIL
            return response_result_process(error_data, xml=xml)