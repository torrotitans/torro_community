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

class interfacePolicyTagsList(Resource):

    @login_required
    def get(self, ):
        """Get policy tags list

        @@@

        ### return
        ```json
        {
            "code": 200,
            "data": [
                {
                    "ad_group": "",
                    "create_time": "Sun, 31 Oct 2021 03:52:58 GMT",
                    "creator_id": "354",
                    "description": "PILL2_text",
                    "gcp_taxonomy_id": "projects/principal-yen-328302/locations/asia-east2/taxonomies/8762507136456973809",
                    "id": 15,
                    "input_form_id": 414,
                    "policy_tags_list": [],
                    "project_id": null,
                    "taxonomy_display_name": "PILL2_text",
                    "workspace_id": 362
                },
                {
                    "ad_group": "",
                    "create_time": "Sun, 31 Oct 2021 03:54:35 GMT",
                    "creator_id": "354",
                    "description": "PILL2_text",
                    "gcp_taxonomy_id": "projects/principal-yen-328302/locations/asia-east2/taxonomies/3834660398677188499",
                    "id": 16,
                    "input_form_id": 414,
                    "policy_tags_list": [
                        {
                            "ad_group": "Engineer@torro.ai",
                            "create_time": "Sun, 31 Oct 2021 03:54:35 GMT",
                            "description": "PILL2",
                            "display_name": "PILL2",
                            "gcp_policy_tag_id": "projects/principal-yen-328302/locations/asia-east2/taxonomies/3834660398677188499/policyTags/5937536117245753521",
                            "id": 14,
                            "sub_tags": [
                                {
                                    "ad_group": "Engineer@torro.ai",
                                    "create_time": "Sun, 31 Oct 2021 03:54:35 GMT",
                                    "description": "PILL2_1",
                                    "display_name": "PILL2_1",
                                    "gcp_policy_tag_id": "projects/principal-yen-328302/locations/asia-east2/taxonomies/3834660398677188499/policyTags/212879785092982789",
                                    "id": 15,
                                    "sub_tags": [],
                                    "taxonomy_display_name": "PILL2_text"
                                }
                            ],
                            "taxonomy_display_name": "PILL2_text"
                        }
                    ],
                    "project_id": "principal-yen-328302",
                    "taxonomy_display_name": "PILL2_text",
                    "workspace_id": 362
                },
                {
                    "ad_group": "Engineer@torro.ai",
                    "create_time": "Sun, 31 Oct 2021 06:28:42 GMT",
                    "creator_id": "354",
                    "description": "PILL3_text",
                    "gcp_taxonomy_id": "projects/principal-yen-328302/locations/asia-east2/taxonomies/3537752682611072695",
                    "id": 17,
                    "input_form_id": 415,
                    "policy_tags_list": [
                        {
                            "ad_group": "Engineer@torro.ai",
                            "create_time": "Sun, 31 Oct 2021 06:28:42 GMT",
                            "description": "PILL3",
                            "display_name": "PILL3",
                            "gcp_policy_tag_id": "projects/principal-yen-328302/locations/asia-east2/taxonomies/3537752682611072695/policyTags/5664003869018489173",
                            "id": 16,
                            "sub_tags": [
                                {
                                    "ad_group": "Engineer@torro.ai",
                                    "create_time": "Sun, 31 Oct 2021 06:28:43 GMT",
                                    "description": "PILL3_1",
                                    "display_name": "PILL3_1",
                                    "gcp_policy_tag_id": "projects/principal-yen-328302/locations/asia-east2/taxonomies/3537752682611072695/policyTags/3024644269548744207",
                                    "id": 17,
                                    "sub_tags": [],
                                    "taxonomy_display_name": "PILL3_text"
                                }
                            ],
                            "taxonomy_display_name": "PILL3_text"
                        }
                    ],
                    "project_id": "principal-yen-328302",
                    "taxonomy_display_name": "PILL3_text",
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
            data = workspace_singleton.get_policy_tags_info(workspace_id)
            if data['code'] == 200:
                response_data = data['data']
                # data['data'] = req.verify_all_param(response_data, workspace_singleton.getPolicyTags_GET_response)
            # # print(data)
            return response_result_process(data, xml=xml)
        except Exception as e:
            lg.error(e)
            error_data = response_code.GET_DATA_FAIL
            return response_result_process(error_data, xml=xml)

    # @login_required
    # def post(self,):
    #     xml = request.args.get('format')
    #     try:
    #         request_data = req.request_process(request, xml, modelEnum.department.value)
    #         if isinstance(request_data, bool):
    #             request_data = response_code.REQUEST_PARAM_FORMAT_ERROR
    #             return response_result_process(request_data, xml=xml)
    #         # if not request_data:
    #         #     data = response_code.REQUEST_PARAM_MISSED
    #         #     return response_result_process(data, xml=xml)
    #         # # print(request_data)
    #         # # print('policy_tagsApiPara.setPolicyTags_POST_request', policy_tagsApiPara.setPolicyTags_POST_request)
    #         request_data = req.verify_all_param(request_data, workspace_singleton.getPolicyTags_POST_request)
    #         policy_tags_id = request_data['id']
    #         data = workspace_singleton.get_policy_tags_details_info_by_id(policy_tags_id)
    #         if data['code'] == 200:
    #             response_data = data['data']
    #             data['data'] = req.verify_all_param(response_data, workspace_singleton.setPolicyTags_POST_request)
    #         # # print(data)
    #         return response_result_process(data, xml=xml)
    #     except Exception as e:
    #         lg.error(e)
    #         # print(traceback.format_exc())
    #         error_data = response_code.ADD_DATA_FAIL
    #         return response_result_process(error_data, xml=xml)
    #
