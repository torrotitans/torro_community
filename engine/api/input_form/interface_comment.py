#!/usr/bin/python
# -*- coding: UTF-8 -*

from utils.api_version_verify import api_version
import traceback
from flask import request
from flask_restful import Resource
from core.comment_singleton import comment_singleton
from utils.log_helper import lg
from utils.status_code import response_code
from common.common_model_enum import modelEnum
from common.common_response_process import response_result_process
from common.common_login_helper import login_required
from common.common_request_process import req
from db.input_form.db_input_form_parameter import inputFormApiPara

class interfaceComment(Resource):

    # add
    # @api_version
    @login_required
    def post(self,):
        xml = request.args.get('commentat')
        try:
            request_data = req.request_process(request, xml, modelEnum.department.value)
            if isinstance(request_data, bool):
                request_data = response_code.REQUEST_PARAM_FORMAT_ERROR
                return response_result_process(request_data, xml=xml)

            # if not request_data:
            #     data = response_code.REQUEST_PARAM_MISSED
            #     return response_result_process(data, xml=xml)
            user_id = req.get_user_key()
            account_id = req.get_user_account_id()
            request_data = req.verify_all_param(request_data, inputFormApiPara.comment_POST_request)
            data = comment_singleton.add_new_comment(user_id, account_id, request_data)

            if data['code'] == 200:
                response_data = data['data']
                data['data'] = req.verify_all_param(response_data, inputFormApiPara.comment_POST_response)
            return response_result_process(data, xml=xml)
        except Exception as e:
            # lg.error(e)
            lg.error(traceback.format_exc())
            error_data = response_code.ADD_DATA_FAIL
            return response_result_process(error_data, xml=xml)

    # delete
    # @api_version
    @login_required
    def delete(self, ):
        xml = request.args.get('commentat')
        try:
            request_data = req.request_process(request, xml, modelEnum.department.value)
            if isinstance(request_data, bool):
                request_data = response_code.REQUEST_PARAM_FORMAT_ERROR
                return response_result_process(request_data, xml=xml)
            # if not request_data:
            #     data = response_code.REQUEST_PARAM_MISSED
            #     return response_result_process(data, xml=xml)
            user_id = req.get_user_key()
            request_data = req.verify_all_param(request_data, inputFormApiPara.comment_DELETE_request)
            data = comment_singleton.delete_comment(user_id, request_data)
            if data['code'] == 200:
                response_data = data['data']
                data['data'] = req.verify_all_param(response_data, inputFormApiPara.comment_DELETE_response)

            return response_result_process(data, xml=xml)
        except Exception as e:
            lg.error(e)
            error_data = response_code.DELETE_DATA_FAIL
            return response_result_process(error_data, xml=xml)

    # update
    # @api_version
    @login_required
    def put(self,):
        xml = request.args.get('commentat')
        try:
            request_data = req.request_process(request, xml, modelEnum.department.value)
            # # print('request_data:', request_data)
            if isinstance(request_data, bool):
                request_data = response_code.REQUEST_PARAM_FORMAT_ERROR
                return response_result_process(request_data, xml=xml)
            # if not request_data:
            #     data = response_code.REQUEST_PARAM_MISSED
            #     return response_result_process(data, xml=xml)
            request_data = req.verify_all_param(request_data, inputFormApiPara.comment_PUT_request)

            comment = request_data
            workspace_id = req.get_workspace_id()
            data = comment_singleton.update_comment(comment, workspace_id)

            if data['code'] == 200:
                response_data = data['data']
                data['data'] = req.verify_all_param(response_data, inputFormApiPara.comment_PUT_response)

            return response_result_process(data, xml=xml)
        except Exception as e:
            lg.error(traceback.format_exc())
            # # print(traceback.commentat_exc())
            error_data = response_code.ADD_DATA_FAIL
            return response_result_process(error_data, xml=xml)
