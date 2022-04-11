#!/usr/bin/python
# -*- coding: UTF-8 -*

from flask import request, g, make_response
from flask_restful import Resource
from common.common_input_form_status import status as Status
# from common.common_log import operation_log
from common.common_model_enum import modelEnum
from common.common_request_process import req
from common.common_response_process import response_result_process, DateEncoder
from db.user.db_user_parameter import userApiPara
from common.common_login_helper import login_required
from utils.auth_helper import Auth
from utils.status_code import response_code
import json
from config import config
import os
import logging
import traceback

# Get the logger specified in the file
logger = logging.getLogger("main." + __name__)
config_name = os.getenv('FLASK_CONFIG') or 'default'
Config = config[config_name]


class interfaceLogin(Resource):

    allow_origins = [Config.FRONTEND_URL, 'http://localhost:8080']

    @login_required
    def get(self):

        xml = request.args.get('format')
        try:

            new_token, role_name, role_list, workspace_id, workspace_list = Auth.refresh_token(request, None, None)
            # print('user_token:', new_token)
            # operation_log(description='login')
            if new_token:
                data = response_code.SUCCESS
                data['data'] = {'role_list': role_list, 'role_name': role_name,
                                'workspace_list': workspace_list, 'workspace_id': workspace_id}
                resp = make_response(json.dumps(data, cls=DateEncoder))
                # resp.headers['Access-Control-Allow-Origin'] = 'http://34.96.134.183:9000,http://localhost:8080'
                # resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:8080'
                origin = request.headers.get('Origin')
                # print('request.headers:', request.headers.get('Origin'))
                if origin in interfaceLogin.allow_origins:
                    resp.headers['Access-Control-Allow-Origin'] = origin

                resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
                resp.headers['Access-Control-Allow-Credentials'] = 'true'
                resp.headers['Access-Control-Allow-Methods'] = "GET,POST,PUT,DELETE,OPTIONS"
                if config_name == 'production':
                    resp.headers.add('Set-Cookie', 'token={}; SameSite=None; Secure'.format(new_token))
                else:
                    resp.set_cookie("token", new_token, max_age=Config.PERMANENT_SESSION_LIFETIME)
                    resp.set_cookie("SameSite", 'None', samesite=None, secure=None,
                                    max_age=Config.PERMANENT_SESSION_LIFETIME)
                    resp.set_cookie("Secure", samesite=None, secure=None, max_age=Config.PERMANENT_SESSION_LIFETIME)
                return resp
            else:
                data = response_code.UPDATE_DATA_FAIL
                return response_result_process(data, xml=xml)

        except Exception as e:
            logger.error("FN:interfaceLogin_get error:{}".format(traceback.format_exc()))
            # print(traceback.format_exc())
            error_data = response_code.ADD_DATA_FAIL
            return response_result_process(error_data, xml=xml)

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
            
            # Disable if the login ID is numeric 
            # request_data = req.verify_all_param(request_data, userApiPara.login_POST_request)

            login_name, login_password = request_data.get('login_name'), request_data.get('login_password')
            offline_flag = request_data.get('is_offline', Status.offline_flag)

            # AuthN User
            dict_user = Auth.authenticate(login_name, login_password, offline_flag)
            logger.debug('FN:post dict_user:{}'.format(dict_user))
            
            if 'token' not in dict_user:
                return response_code.LOGIN_FAIL

            # Populate user data
            user_key = dict_user.get('ID')
            account_id = dict_user.get('ACCOUNT_ID')
            token = dict_user['token']
            dict_user.pop('token')
            # print('user_token:', token)
            # operation_log(description='login')
            if user_key:
                g.user_key = user_key # torro User ID
                g.account_id = account_id
                g.account_cn = dict_user.get('ACCOUNT_CN')
                data = response_code.SUCCESS
                data['data'] = dict_user
                logger.info('FN:post user:{} login:True'.format(g.account_cn))
            else:
                data = dict_user
            
            resp = make_response(json.dumps(data, cls=DateEncoder))
            origin = request.headers.get('Origin')
            # print('request.headers:', request.headers.get('Origin'))
            
            if origin in self.allow_origins:
                resp.headers['Access-Control-Allow-Origin'] = origin
            # resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:8080'
            resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
            resp.headers['Access-Control-Allow-Credentials'] = 'true'
            resp.headers['Access-Control-Allow-Methods'] = "GET,POST,PUT,DELETE,OPTIONS"
            
            if config_name == 'production':
                resp.headers.add('Set-Cookie', 'token={}; SameSite=None; Secure'.format(token))
            else:
                resp.set_cookie("token", token, max_age=Config.PERMANENT_SESSION_LIFETIME)
                resp.set_cookie("SameSite", 'None', samesite=None, secure=None, max_age=Config.PERMANENT_SESSION_LIFETIME)
                resp.set_cookie("Secure", samesite=None, secure=None, max_age=Config.PERMANENT_SESSION_LIFETIME)
                
            return resp
        
        except Exception as e:

            logger.error("FN:interfaceLogin_post error:{}".format(traceback.format_exc()))
            error_data = response_code.LOGIN_FAIL
            
            return response_result_process(error_data, xml=xml)
        
    def put(self):
        xml = request.args.get('format')
        try:
            request_data = req.request_process(request, xml, modelEnum.login.value)
            # if isinstance(request_data, bool):
            #     request_data = response_code.REQUEST_PARAM_FORMAT_ERROR
            #     return response_result_process(request_data, xml=xml)
            # if not request_data:
            #     data = response_code.REQUEST_PARAM_MISSED
            #     return response_result_process(data, xml=xml)
            request_data = req.verify_all_param(request_data, userApiPara.login_PUT_request)
            role_name = request_data.get('role_name', None)
            workspace_id = request_data.get('workspace_id', None)

            new_token, role_name, role_list, workspace_id, workspace_list = Auth.refresh_token(request, role_name, workspace_id)
            # print('user_token:', new_token)
            # operation_log(description='login')
            if new_token:
                data = response_code.SUCCESS
                data['data'] = {'role_list': role_list, 'role_name': role_name,
                                'workspace_list': workspace_list, 'workspace_id': workspace_id}
                resp = make_response(json.dumps(data, cls=DateEncoder))

                origin = request.headers.get('Origin')
                if origin in self.allow_origins:
                    resp.headers['Access-Control-Allow-Origin'] = origin
                # resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:8080'
                resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
                resp.headers['Access-Control-Allow-Credentials'] = 'true'
                resp.headers['Access-Control-Allow-Methods'] = "GET,POST,PUT,DELETE,OPTIONS"
                if config_name == 'production':
                    resp.headers.add('Set-Cookie', 'token={}; SameSite=None; Secure'.format(new_token))
                else:
                    resp.set_cookie("token", new_token, max_age=Config.PERMANENT_SESSION_LIFETIME)
                    resp.set_cookie("SameSite", 'None', samesite=None, secure=None, max_age=Config.PERMANENT_SESSION_LIFETIME)
                    resp.set_cookie("Secure", samesite=None, secure=None, max_age=Config.PERMANENT_SESSION_LIFETIME)
                return resp

            else:
                data = response_code.UPDATE_DATA_FAIL
                resp = make_response(json.dumps(data, cls=DateEncoder))
                resp.set_cookie("token", '')
                return resp
            
        except Exception as e:

            logger.error("FN:interfaceLogin_put error:{}".format(traceback.format_exc()))
            error_data = response_code.LOGIN_FAIL
            
            return response_result_process(error_data, xml=xml)
