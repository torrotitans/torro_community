#!/usr/bin/python
# -*- coding: UTF-8 -*

import traceback
from flask import request
from flask_restful import Resource
from core.workspace_singleton import workspace_singleton
from utils.log_helper import lg
from utils.status_code import response_code
from common.common_response_process import response_result_process
from common.common_login_helper import login_required
from common.common_request_process import req
from db.workspace.db_workspace_parameter import workspaceApiPara

class interfaceTagTemplateList(Resource):

    @login_required
    def get(self, ):
        """Get tag template list

        @@@

        ### return
        ```json
{
    "code": 200,
    "data": [
        {
            "create_time": "Wed, 17 Nov 2021 10:22:58 GMT",
            "creator_id": "354",
            "description": "data tags",
            "display_name": "data tags1688",
            "id": 26,
            "input_form_id": 470,
            "location": "asia-east2",
            "project_id": "principal-yen-328302",
            "tag_template_form_id": 408,
            "tag_template_id": "data_tags1688",
            "workspace_id": 362
        },
        {
            "create_time": "Sun, 21 Nov 2021 02:42:37 GMT",
            "creator_id": "354",
            "description": "data tags",
            "display_name": "tag template  1031",
            "id": 27,
            "input_form_id": 472,
            "location": "asia-east2",
            "project_id": "principal-yen-328302",
            "tag_template_form_id": 409,
            "tag_template_id": "tag_template__1031",
            "workspace_id": 362
        },
        {
            "create_time": "Sun, 21 Nov 2021 07:33:32 GMT",
            "creator_id": "354",
            "description": "Tag template description",
            "display_name": "Tag template name",
            "id": 28,
            "input_form_id": 478,
            "location": "asia-east2",
            "project_id": "principal-yen-328302",
            "tag_template_form_id": 410,
            "tag_template_id": "tag_template_name",
            "workspace_id": 362
        }
    ],
    "msg": "request successfully"
}
        ```
        @@@
        """
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

            # ad_group_list = ['Engineer@torro.ai', 'ws_head_group']
            data = workspace_singleton.get_tag_template_info(workspace_id)
            if data['code'] == 200:
                response_data = data['data']
                # data['data'] = req.verify_all_param(response_data, workspace_singleton.getTagTemplate_GET_response)
            # # print(data)
            return response_result_process(data, xml=xml)
        except Exception as e:
            lg.error(e)
            error_data = response_code.GET_DATA_FAIL
            return response_result_process(error_data, xml=xml)
