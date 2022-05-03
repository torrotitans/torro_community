#!/usr/bin/python
# -*- coding: UTF-8 -*

import json
from common.common_response_process import DateEncoder
from flask import make_response
import traceback
from flask import request
from flask_restful import Resource
from core.workspace_singleton import workspace_singleton
from utils.status_code import response_code
from common.common_model_enum import modelEnum
from common.common_response_process import response_result_process
from common.common_login_helper import login_required
from common.common_request_process import req
from db.workspace.db_workspace_parameter import workspaceApiPara
from utils.auth_helper import Auth
from api.login.interface_login import interfaceLogin
import os
import traceback
import logging
from config import config

logger = logging.getLogger("main." + __name__)
config_name = os.getenv('FLASK_CONFIG') or 'default'
Config = config[config_name]

class interfaceWorkspaceSetting(Resource):

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
                data['msg'] = 'Token error or expired, please login again.'
                logger.error("FN:interfaceWorkspaceSetting_get error:{}".format(traceback.format_exc()))
                return response_result_process(data, xml=xml)
            # ad_group_list = ['Engineer@torro.ai', 'ws_owner_group']
            data = workspace_singleton.get_workspace_info_by_ad_group(account_id)
            if data['code'] == 200:
                response_data = data['data']
                data['data'] = req.verify_all_param(response_data, workspaceApiPara.getWorkspace_GET_response)
            # # print(data)
            return response_result_process(data, xml=xml)

        except Exception as e:
            logger.error("FN:interfaceWorkspaceSetting_get error:{}".format(traceback.format_exc()))
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
            # if not request_data:
            #     data = response_code.REQUEST_PARAM_MISSED
            #     return response_result_process(data, xml=xml)
            # # print(request_data)
            # # print('workspaceApiPara.setWorkspace_POST_request', workspaceApiPara.setWorkspace_POST_request)
            # try:
            #     f = request.files['admin_sa_path']
            #     upload_path = './data/workspace/'
            #     if not os.path.exists(upload_path):
            #         os.makedirs(upload_path)
            #     upload_path += f.filename
            #     f.save(upload_path)
            #     request_data['admin_sa_path'] = upload_path
            # except:
            #     pass
            request_data = req.verify_all_param(request_data, workspaceApiPara.setWorkspace_POST_request)
            data = workspace_singleton.add_new_workspace_setting(request_data)
            if data['code'] == 200:
                workspace_name = data['data']['ws_name']
                workspace_id = data['data']['ws_id']
                new_token, role_name, role_list, workspace_id, workspace_list =Auth.refresh_token(request, None, None, new_workspace_id_dict={'label': workspace_name, 'value': workspace_id})
                # print('user_token:', new_token)
                # operation_log(description='login')
                if new_token:
                    data = response_code.SUCCESS
                    data['data'] = {'role_list': role_list, 'role_name': role_name,
                                    'workspace_list': workspace_list, 'workspace_id': workspace_id}
                    resp = make_response(json.dumps(data, cls=DateEncoder).replace('\\', '\\\\'))
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
                        resp.set_cookie("SameSite", 'None', samesite=None, secure=None, max_age=Config.PERMANENT_SESSION_LIFETIME)
                        resp.set_cookie("Secure", samesite=None, secure=None, max_age=Config.PERMANENT_SESSION_LIFETIME)
                    return resp
                response_data = data['data']
                data['data'] = req.verify_all_param(response_data, workspaceApiPara.setWorkspace_POST_response)
            # # print(data)
            return response_result_process(data, xml=xml)
        except Exception as e:
            logger.error("FN:interfaceWorkspaceSetting_post error:{}".format(traceback.format_exc()))
            # print(traceback.format_exc())
            error_data = response_code.ADD_DATA_FAIL
            return response_result_process(error_data, xml=xml)

    @login_required
    # update the workspace info
    def put(self,):
        xml = request.args.get('format')
        try:
            request_data = req.request_process(request, xml, modelEnum.department.value)
            # # print('request_data:', request_data)
            if isinstance(request_data, bool):
                request_data = response_code.REQUEST_PARAM_FORMAT_ERROR
                return response_result_process(request_data, xml=xml)
            # try:
            #     f = request.files['admin_sa_path']
            #     upload_path = './data/workspace/'
            #     if not os.path.exists(upload_path):
            #         os.makedirs(upload_path)
            #     upload_path += f.filename
            #     f.save(upload_path)
            #     request_data['admin_sa_path'] = upload_path
            # except:
            #     pass
            request_data = req.verify_all_param(request_data, workspaceApiPara.updateWorkspace_POST_request)

            data = workspace_singleton.update_workspace(request_data)
            if data['code'] == 200:
                response_data = data['data']
                data['data'] = req.verify_all_param(response_data, workspaceApiPara.updateWorkspace_POST_response)
            # # print(data)
            return response_result_process(data, xml=xml)

        except Exception as e:
            logger.error("FN:interfaceWorkspaceSetting_put error:{}".format(traceback.format_exc()))
            # # print(traceback.format_exc())
            error_data = response_code.ADD_DATA_FAIL
            return response_result_process(error_data, xml=xml)


    @login_required
    # delete the workspace info
    def delete(self,):
        xml = request.args.get('format')
        try:
            request_data = req.request_process(request, xml, modelEnum.department.value)
            # # print('request_data:', request_data)
            if isinstance(request_data, bool):
                request_data = response_code.REQUEST_PARAM_FORMAT_ERROR
                return response_result_process(request_data, xml=xml)

            request_data = req.verify_all_param(request_data, workspaceApiPara.updateWorkspace_POST_request)

            data = workspace_singleton.delete_workspace(request_data)
            if data['code'] == 200:
                workspace_name = data['data']['ws_name']
                workspace_id = data['data']['id']
                new_token, role_name, role_list, workspace_id, workspace_list =Auth.refresh_token(request, None, None, remove_workspace_id_dict={'label': workspace_name, 'value': workspace_id})
                # print('user_token:', new_token)
                # operation_log(description='login')
                if new_token:
                    data = response_code.SUCCESS
                    data['data'] = {'role_list': role_list, 'role_name': role_name,
                                    'workspace_list': workspace_list, 'workspace_id': workspace_id}
                    resp = make_response(json.dumps(data, cls=DateEncoder).replace('\\', '\\\\'))
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
                        resp.set_cookie("SameSite", 'None', samesite=None, secure=None, max_age=Config.PERMANENT_SESSION_LIFETIME)
                        resp.set_cookie("Secure", samesite=None, secure=None, max_age=Config.PERMANENT_SESSION_LIFETIME)
                    return resp

                response_data = data['data']
                data['data'] = req.verify_all_param(response_data, workspaceApiPara.updateWorkspace_POST_response)
                
            return response_result_process(data, xml=xml)

        except Exception as e:
            logger.error("FN:interfaceWorkspaceSetting_delete error:{}".format(traceback.format_exc()))
            error_data = response_code.DELETE_DATA_FAIL
            return response_result_process(error_data, xml=xml)
