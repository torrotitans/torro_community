#!/usr/bin/python
# -*- coding: UTF-8 -*

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
from core.input_form_singleton import input_form_singleton

class interfaceEditForm(Resource):

    # add
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

            request_data = req.verify_all_param(request_data, formApiPara.postFormData_POST_request)

            workspace_id = req.get_workspace_id()
            try:
                user_key = req.get_user_key()
                # print('user id:', user_key)
            except:
                data = response_code.GET_DATA_FAIL
                # print(traceback.format_exc())
                data['msg'] = 'Token error or expired, please login again.'
                return response_result_process(data, xml=xml)
            if 'tag_template' in request_data:
                form_id = 104
            else:
                form_id = 101
            form_data = formSingleton_singleton.get_details_form_by_id(form_id)
            field_ids = {}
            request_data['form_id'] = form_id
            request_data['form_field_values_dict'] = {'u1': request_data['title'], 'u3': request_data['fieldList'],
                                                      'u2': request_data['des']}
            del request_data['title']
            del request_data['des']
            del request_data['fieldList']
            # print('request_data:', request_data)
            if form_data['code'] == 200:
                for field in form_data["data"]["fieldList"]:
                    field_id = field['id']
                    field_style = field['style']
                    field_ids[field_id] = field_style

            request_data['field_ids'] = field_ids
            # print('request_data: ', request_data)
            # exit(0)
            data = input_form_singleton.input_form_data(user_key, request_data, workspace_id)
            # workspace_id = req.get_workspace_id()
            # form = request_data
            # data = formSingleton_singleton.add_new_form(form, workspace_id)
            if data['code'] == 200:
                response_data = data['data']
                data['data'] = req.verify_all_param(response_data, formApiPara.postFormData_POST_response)
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
            workspace_id = req.get_workspace_id()
            try:
                user_key = req.get_user_key()
                # print('user id:', user_key)
            except:
                data = response_code.GET_DATA_FAIL
                # print(traceback.format_exc())
                data['msg'] = 'Token error or expired, please login again.'
                return response_result_process(data, xml=xml)
            if 'tag_template' in request_data:
                form_id = 106
            else:
                form_id = 102

            # form_id = 102
            form_data = formSingleton_singleton.get_details_form_by_id(form_id)
            field_ids = {}
            request_data['form_id'] = form_id
            request_data['form_field_values_dict'] = {'u1': request_data['id']}
            del request_data['id']
            if form_data['code'] == 200:
                for field in form_data["data"]["fieldList"]:
                    field_id = field['id']
                    field_style = field['style']
                    field_ids[field_id] = field_style

            request_data['field_ids'] = field_ids
            # print('request_data: ', request_data)
            # exit(0)
            data = input_form_singleton.input_form_data(user_key, request_data, workspace_id)

            # request_data = req.verify_all_param(request_data, formApiPara.postFormData_DELETE_request)
            # form = request_data
            # data = formSingleton_singleton.delete_form(form)
            if data['code'] == 200:
                response_data = data['data']
                data['data'] = req.verify_all_param(response_data, formApiPara.postFormData_DELETE_response)

            return response_result_process(data, xml=xml)
        except Exception as e:
            lg.error(e)
            error_data = response_code.DELETE_DATA_FAIL
            return response_result_process(error_data, xml=xml)

    # update
    # @api_version
    @login_required
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
            request_data = req.verify_all_param(request_data, formApiPara.postFormData_PULL_request)
            workspace_id = req.get_workspace_id()
            try:
                user_key = req.get_user_key()
                # print('user id:', user_key)
            except:
                data = response_code.GET_DATA_FAIL
                # print(traceback.format_exc())
                data['msg'] = 'Token error or expired, please login again.'
                return response_result_process(data, xml=xml)
            if 'tag_template' in request_data:
                form_id = 105
            else:
                form_id = 103
            # form_id = 103
            form_data = formSingleton_singleton.get_details_form_by_id(form_id)
            field_ids = {}
            request_data['form_id'] = form_id
            request_data['form_field_values_dict'] = {'u1': request_data['id'], 'u2': request_data['title'], 'u4': request_data['fieldList'],
                                                      'u3': request_data['des']}
            del request_data['id']
            del request_data['title']
            del request_data['des']
            del request_data['fieldList']
            if form_data['code'] == 200:
                for field in form_data["data"]["fieldList"]:
                    field_id = field['id']
                    field_style = field['style']
                    field_ids[field_id] = field_style

            request_data['field_ids'] = field_ids
            # print('request_data: ', request_data)

            data = input_form_singleton.input_form_data(user_key, request_data, workspace_id)

            # form = request_data
            # workspace_id = req.get_workspace_id()
            # account_id = req.get_user_account_id()
            # data = formSingleton_singleton.update_form(form, account_id, workspace_id)

            if data['code'] == 200:
                response_data = data['data']
                data['data'] = req.verify_all_param(response_data, formApiPara.postFormData_PULL_response)

            return response_result_process(data, xml=xml)
        except Exception as e:
            lg.error(e)
            # # print(traceback.format_exc())
            error_data = response_code.ADD_DATA_FAIL
            return response_result_process(error_data, xml=xml)
