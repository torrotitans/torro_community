#!/usr/bin/python
# -*- coding: UTF-8 -*

import traceback
from flask import request
from flask_restful import Resource
from core.workflow_singleton import workflowSingleton_singleton
from utils.log_helper import lg
from utils.status_code import response_code
from common.common_model_enum import modelEnum
from common.common_response_process import response_result_process
from common.common_request_process import req
from db.workflow.db_stages_parameter import stageBase
from db.workflow.db_workflow_parameter import workflowApiPara
from common.common_login_helper import login_required
class interfaceEditWorkflow(Resource):

    # add
    # @api_version
    @login_required
    def post(self,):
        xml = request.args.get('format')
        try:
            request_data = req.request_process(request, xml, modelEnum.department.value)
            # print('request_data', request.data)
            if isinstance(request_data, bool):
                request_data = response_code.REQUEST_PARAM_FORMAT_ERROR
                return response_result_process(request_data, xml=xml)

            # if not request_data:
            #     data = response_code.REQUEST_PARAM_MISSED
            #     return response_result_process(data, xml=xml)
            request_data = req.verify_all_param(request_data, workflowApiPara.postWorkflowData_POST_request)
            for index, stage in enumerate(request_data['stages']):
                print("request_data['stages'][index] 1111:", stage)
                request_data['stages'][index] = stageBase.verify_all_param(req.verify_all_param, stage)
                print("request_data['stages'][index] 2222:", request_data['stages'][index])
            workflow = request_data
            data = workflowSingleton_singleton.add_new_workflow(workflow)

            if data['code'] == 200:
                response_data = data['data']
                data['data'] = req.verify_all_param(response_data, workflowApiPara.postWorkflowData_POST_response)
            return response_result_process(data, xml=xml)
        except Exception as e:
            lg.error(e)
            # print(traceback.format_exc())
            error_data = response_code.ADD_DATA_FAIL
            return response_result_process(error_data, xml=xml)

    # delete
    # @api_version
    @login_required
    def delete(self, ):
        xml = request.args.get('format')
        try:
            request_data = req.request_process(request, xml, modelEnum.department.value)
            if isinstance(request_data, bool):
                request_data = response_code.REQUEST_PARAM_FORMAT_ERROR
                return response_result_process(request_data, xml=xml)
            # if not request_data:
            #     data = response_code.REQUEST_PARAM_MISSED
            #     return response_result_process(data, xml=xml)
            request_data = req.verify_all_param(request_data, workflowApiPara.postWorkflowData_DELETE_request)
            # request_data = stageBase.verify_all_param(req.verify_all_param, request_data)
            workflow = request_data
            # print(workflow)
            data = workflowSingleton_singleton.delete_workflow(workflow)

            if data['code'] == 200:
                response_data = data['data']
                data['data'] = req.verify_all_param(response_data, workflowApiPara.postWorkflowData_DELETE_response)

            return response_result_process(data, xml=xml)
        except Exception as e:
            lg.error(e)
            error_data = response_code.DELETE_DATA_FAIL
            return response_result_process(error_data, xml=xml)

    # update
    # @api_version
    # @login_required
    def put(self,):
        xml = request.args.get('format')
        try:
            request_data = req.request_process(request, xml, modelEnum.department.value)
            # # print('request_data:', request_data)
            if isinstance(request_data, bool):
                request_data = response_code.REQUEST_PARAM_FORMAT_ERROR
                return response_result_process(request_data, xml=xml)
            # if not request_data:
            #     data = response_code.REQUEST_PARAM_MISSED
            #     return response_result_process(data, xml=xml)
            request_data = req.verify_all_param(request_data, workflowApiPara.postWorkflowData_PULL_request)
            for index, stage in enumerate(request_data['stages']):
                print("request_data['stages'][index] 1111:", stage)
                request_data['stages'][index] = stageBase.verify_all_param(req.verify_all_param, stage)
            print("request_data['stages'][index] 2222:", request_data['stages'])
            # request_data = stageBase.verify_all_param(req.verify_all_param, request_data)
            workflow = request_data
            data = workflowSingleton_singleton.update_workflow(workflow)

            if data['code'] == 200:
                response_data = data['data']
                data['data'] = req.verify_all_param(response_data, workflowApiPara.postWorkflowData_PULL_response)

            return response_result_process(data, xml=xml)
        except Exception as e:
            lg.error(e)
            # print(traceback.format_exc())
            error_data = response_code.ADD_DATA_FAIL
            return response_result_process(error_data, xml=xml)
