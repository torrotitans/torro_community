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

class interfaceDetailsWorkflow(Resource):

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

            request_data = req.verify_all_param(request_data, workflowApiPara.getDetailsWorkflowDataById_POST_request)

            workflow_id = request_data.get('id')
            data = workflowSingleton_singleton.get_details_workflow(workflow_id)
            if data['code'] == 200:
                response_data = data['data']
                data['data'] = req.verify_all_param(response_data, workflowApiPara.getDetailsWorkflowDataById_POST_response)
            
            return response_result_process(data, xml=xml)

        except Exception as e:
            logger.error("FN:interfaceDetailsWorkflow_post error:{}".format(traceback.format_exc()))
            error_data = response_code.GET_DATA_FAIL
            return response_result_process(error_data, xml=xml)



