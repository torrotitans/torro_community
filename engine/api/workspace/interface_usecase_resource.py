#!/usr/bin/python
# -*- coding: UTF-8 -*

import traceback
from flask import request, g
from flask_restful import Resource
from core.workspace_singleton import workspace_singleton
from utils.status_code import response_code
from common.common_response_process import response_result_process
from common.common_login_helper import login_required
from common.common_request_process import req
from db.workspace.db_workspace_parameter import workspaceApiPara
import traceback
import logging

logger = logging.getLogger("main." + __name__)

class interfaceUsecaseResource(Resource):

    @login_required
    def get(self, ):
        xml = request.args.get('format')

        try:
            try:
                user_key = req.get_user_key()
                account_id = req.get_user_account_id()
                workspace_id = req.get_workspace_id()
                print('FN:getTagTemplateList user_key:', user_key)
                print('FN:getTagTemplateList account_id:', account_id)
                print('FN:getTagTemplateList workspace_id:', workspace_id)
            except:
                data = response_code.GET_DATA_FAIL
                data['msg'] = 'Token error or expired, please login again.'
                logger.error("FN:interfaceUsecaseResource_get error:{}".format(traceback.format_exc()))
                return response_result_process(data, xml=xml)

            # ad_group_list = ['Engineer@torro.ai', 'ws_owner_group']
            data = workspace_singleton.get_usecase_resource(workspace_id)
            # if data['code'] == 200:
            #     response_data = data['data']
            #     # data['data'] = req.verify_all_param(response_data, workspace_singleton.getTagTemplate_GET_response)
            # # # print(data)
            return response_result_process(data, xml=xml)
        except Exception as e:
            logger.error("FN:interfaceUsecaseResource_get error:{}".format(traceback.format_exc()))
            error_data = response_code.GET_DATA_FAIL
            return response_result_process(error_data, xml=xml)
