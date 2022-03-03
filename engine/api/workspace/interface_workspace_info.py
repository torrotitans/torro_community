#!/usr/bin/python
# -*- coding: UTF-8 -*

from utils.api_version_verify import api_version
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
import traceback
import logging

logger = logging.getLogger("main." + __name__)


class interfaceWorkspaceInfo(Resource):
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
                logger.error("FN:interfaceWorkspaceInfo_get error:{}".format(traceback.format_exc()))
                return response_result_process(data, xml=xml)

            # ad_group_list = ['Engineer@torro.ai', 'ws_owner_group']
            data = workspace_singleton.get_workspace_info_by_ad_group(account_id)
            if data['code'] == 200:
                response_data = data['data']
                data['data'] = req.verify_all_param(response_data, workspaceApiPara.getWorkspace_GET_response)
            # # print(data)
            return response_result_process(data, xml=xml)

        except Exception as e:
            logger.error("FN:interfaceWorkspaceInfo_get error:{}".format(traceback.format_exc()))
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
            request_data = req.verify_all_param(request_data, workspaceApiPara.getWorkspace_POST_request)
            workspace_id = request_data['id']
            data = workspace_singleton.get_workspace_details_info_by_id(workspace_id)
            if data['code'] == 200:
                response_data = data['data']
                data['data'] = req.verify_all_param(response_data, workspaceApiPara.setWorkspace_POST_request)
            # # print(data)
            return response_result_process(data, xml=xml)
        except Exception as e:
            logger.error("FN:interfaceWorkspaceInfo_post error:{}".format(traceback.format_exc()))
            error_data = response_code.ADD_DATA_FAIL
            return response_result_process(error_data, xml=xml)

