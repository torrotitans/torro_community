#!/usr/bin/python
# -*- coding: UTF-8 -*
"""

"""
import os
from utils.api_version_verify import api_version
from utils.auth_helper import Auth
import traceback
from flask import request
from flask_restful import Resource
from core.org_singleton import orgSingleton_singleton
from utils.log_helper import lg
from utils.status_code import response_code
from common.common_model_enum import modelEnum
from common.common_response_process import response_result_process
from common.common_login_helper import login_required
from common.common_request_process import req
from db.org.db_org_parameter import orgApiPara

class interfaceOrgSetting(Resource):


    def get(self):
        xml = request.args.get('format')
        try:
            data = orgSingleton_singleton.get_org_info()
            body = modelEnum.department.value.get('body')
            return response_result_process(data, xml_structure_str=body, xml=xml)
        except Exception as e:
            lg.error(e)
            error_data = response_code.GET_DATA_FAIL
            return response_result_process(error_data, xml=xml)


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
            # form/w/u-t-adjij+team.xeex
            # # print('orgApiPara.setOrg_POST_request', orgApiPara.setOrg_POST_request)
            request_data = req.verify_all_param(request_data, orgApiPara.setOrg_POST_request)
            try:
                f = request.files['cer_path']
                upload_path = './data/ldap_file/'
                if not os.path.exists(upload_path):
                    os.makedirs(upload_path)
                upload_path += f.filename
                f.save(upload_path)
                request_data['cer_path'] = upload_path
            except:
                pass

            _, ldap_usernames = Auth.ldap_auth(request_data['admin'], request_data['admin_pwd'])
            if ldap_usernames[0] is None:
                data = response_code.ADD_DATA_FAIL
                data['msg'] = 'LDAP VERIFY FAILED.'
                return data

            data = orgSingleton_singleton.add_new_org_setting(request_data)
            if data['code'] == 200:
                response_data = data['data']
                # print(response_data)
                data['data'] = req.verify_all_param(response_data, orgApiPara.setOrg_POST_response)
            # # print(data)
            return response_result_process(data, xml=xml)
        except Exception as e:
            lg.error(traceback.format_exc())
            # print(traceback.format_exc())
            error_data = response_code.ADD_DATA_FAIL
            return response_result_process(error_data, xml=xml)


    # update the org info
    def put(self,):
        xml = request.args.get('format')
        try:
            request_data = req.request_process(request, xml, modelEnum.department.value)
            # # print('request_data:', request_data)
            if isinstance(request_data, bool):
                request_data = response_code.REQUEST_PARAM_FORMAT_ERROR
                return response_result_process(request_data, xml=xml)
            request_data = req.verify_all_param(request_data, orgApiPara.updateOrg_POST_request)

            data = orgSingleton_singleton.update_org(request_data)
            if data['code'] == 200:
                response_data = data['data']
                data['data'] = req.verify_all_param(response_data, orgApiPara.updateOrg_POST_response)
            # # print(data)
            return response_result_process(data, xml=xml)

        except Exception as e:
            lg.error(e)
            # # print(traceback.format_exc())
            error_data = response_code.ADD_DATA_FAIL
            return response_result_process(error_data, xml=xml)
