#!/usr/bin/python
# -*- coding: UTF-8 -*
"""

"""
from utils.api_version_verify import api_version
import traceback
from flask import request
from flask_restful import Resource
from core.form_singleton import formSingleton_singleton
from utils.log_helper import lg
from utils.status_code import response_code
from common.common_model_enum import modelEnum
from common.common_response_process import response_result_process
from common.common_login_helper import login_required
from common.common_request_process import req
from db.form.db_form_parameter import formApiPara

class interfaceDetailForm(Resource):

    # @api_version
    # @login_required
    # def get(self, ):
    #     xml = request.args.get('format')
    #     try:
    #         data = formSingleton_singleton.get_all_fields()
    #         body = modelEnum.form.value.get('body')
    #         return response_result_process(data, xml_structure_str=body, xml=xml)
    #     except Exception as e:
    #         lg.error(e)
    #         error_data = response_code.GET_DATA_FAIL
    #         return response_result_process(error_data, xml=xml)


    # @api_version
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

            request_data = req.verify_all_param(request_data, formApiPara.getFormData_POST_request)

            workspace_id = req.get_workspace_id()
            wp_id = request_data.get('workspace_id', workspace_id)
            uc_id = request_data.get('usecase_id', 0)
            form_id = request_data.get('id')
            data = formSingleton_singleton.get_details_form_by_id(form_id, workspace_id, uc_id)
            if data['code'] == 200:
                response_data = data['data']
                data['data'] = req.verify_all_param(response_data, formApiPara.getFormData_POST_response)
            # # print(data)
            return response_result_process(data, xml=xml)
        except Exception as e:
            lg.error(e)
            # print(traceback.format_exc())
            error_data = response_code.GET_DATA_FAIL
            return response_result_process(error_data, xml=xml)

class testingDetailForm():

    # @api_version
    # @login_required
    # def get(self, ):
    #     xml = request.args.get('format')
    #     try:
    #         data = formSingleton_singleton.get_all_fields()
    #         body = modelEnum.form.value.get('body')
    #         return response_result_process(data, xml_structure_str=body, xml=xml)
    #     except Exception as e:
    #         lg.error(e)
    #         error_data = response_code.GET_DATA_FAIL
    #         return response_result_process(error_data, xml=xml)

    def post(self, request_data):
        xml = None
        try:
            # request_data = req.request_process(request, xml, modelEnum.department.value)
            if isinstance(request_data, bool):
                request_data = response_code.REQUEST_PARAM_FORMAT_ERROR
                return response_result_process(request_data, xml=xml)
            if not request_data:
                data = response_code.REQUEST_PARAM_MISSED
                return response_result_process(data, xml=xml)
            fields = ['id']
            must = req.verify_all_param_must(request_data, fields)
            if must:
                return response_result_process(must, xml=xml)
            par_type = {'id': int}
            param_type = req.verify_all_param_type(request_data, par_type)
            if param_type:
                return response_result_process(param_type, xml=xml)
            form_id = request_data.get('id')
            data = formSingleton_singleton.get_details_form_by_id(form_id)
            return response_result_process(data, xml=xml)
        except Exception as e:
            lg.error(e)
            # print(traceback.format_exc())
            error_data = response_code.GET_DATA_FAIL
            return response_result_process(error_data, xml=xml)