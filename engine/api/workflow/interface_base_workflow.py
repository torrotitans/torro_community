#!/usr/bin/python
# -*- coding: UTF-8 -*

from utils.api_version_verify import api_version
from flask import request
from flask_restful import Resource
from core.workflow_singleton import workflowSingleton_singleton
from utils.status_code import response_code
from common.common_model_enum import modelEnum
from common.common_response_process import response_result_process
from common.common_login_helper import login_required
from common.common_request_process import req
from db.workflow.db_workflow_parameter import workflowApiPara
import traceback
import logging

logger = logging.getLogger("main." + __name__)

class interfaceBaseWorkflow(Resource):

    @login_required
    def get(self, ):
        """Get workflow list

        @@@

        ### return
        ```json
        {
            "code": 200,
            "data": [
                {
                    "available": 0,
                    "create_time": "Mon, 03 May 2021 00:00:00 GMT",
                    "creator_id": "",
                    "des": "testing",
                    "form_id": 2,
                    "id": 417,
                    "last_modify_id": "",
                    "stage_hash": "ipdv0zl4bcfpTS0rcEFGgy0vYPmT0nIB1KplcvGmvWQ=",
                    "stage_num": 3,
                    "updated_time": "Mon, 03 May 2021 00:00:00 GMT",
                    "workflow_name": "workflow1"
                }
            ],
            "msg": "request successfully"
        }
        ```
        @@@
        """
        xml = request.args.get('format')
        try:
            user_key = req.get_user_key()
            workspace_id = req.get_workspace_id()
            # print('user id:', user_key)
            data = workflowSingleton_singleton.get_all_base_workflow_v2(workspace_id)
            # print(data)
            body = modelEnum.department.value.get('body')
            return response_result_process(data, xml_structure_str=body, xml=xml)

        except Exception as e:
            logger.error("FN:interfaceBaseWorkflow_get error:{}".format(traceback.format_exc()))
            error_data = response_code.GET_DATA_FAIL
            return response_result_process(error_data, xml=xml)

    @login_required
    def post(self,):

        """Get workflow list by form id

        @@@
        ### args
        |  args | nullable | request type | type |  remarks |
        |-------|----------|--------------|------|----------|
        | form_id |  false   |    body      | int  | form id    |

        ### request
        ```json
        {"form_id": 2}
        ```

        ### return
        ```json
        {
            "code": 200,
            "data": [
                {
                    "available": 0,
                    "create_time": "2021-05-03",
                    "creator_id": "",
                    "des": "testing",
                    "form_id": 2,
                    "id": 417,
                    "last_modify_id": "",
                    "stage_hash": "ipdv0zl4bcfpTS0rcEFGgy0vYPmT0nIB1KplcvGmvWQ=",
                    "stage_num": 3,
                    "updated_time": "2021-05-03",
                    "workflow_name": "workflow1"
                }
            ],
            "msg": "request successfully"
        }
        ```
        @@@
        """

        xml = request.args.get('format')
        try:
            request_data = req.request_process(request, xml, modelEnum.department.value)
            if isinstance(request_data, bool):
                request_data = response_code.REQUEST_PARAM_FORMAT_ERROR
                return response_result_process(request_data, xml=xml)
            # if not request_data:
            #     data = response_code.REQUEST_PARAM_MISSED
            #     return response_result_process(data, xml=xml)
            request_data = req.verify_all_param(request_data, workflowApiPara.getBaseWorkflowListByFormId_POST_request)

            form_id = request_data.get('form_id')
            data = workflowSingleton_singleton.get_all_base_workflow(form_id)
            if data['code'] == 200:
                response_data = data['data']
                # # print('request_data', request_data)
                for index in range(len(response_data)):
                    data['data'][index] = req.verify_all_param(response_data[index], workflowApiPara.getBaseWorkflowListByFormId_POST_response)
            # # print(data)
            return response_result_process(data, xml=xml)

        except Exception as e:
            logger.error("FN:interfaceBaseWorkflow_post error:{}".format(traceback.format_exc()))
            error_data = response_code.GET_DATA_FAIL
            return response_result_process(error_data, xml=xml)



