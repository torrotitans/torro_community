#!/usr/bin/python
# -*- coding: UTF-8 -*

import os
from utils.api_version_verify import api_version
from utils.auth_helper import Auth
import traceback
from flask import request
from flask_restful import Resource
from core.org_singleton import orgSingleton_singleton
from utils.status_code import response_code
from common.common_model_enum import modelEnum
from common.common_response_process import response_result_process
from common.common_login_helper import login_required
from common.common_request_process import req
from db.org.db_org_parameter import orgApiPara
from utils.smtp_helper import Smtp
import traceback
import logging

logger = logging.getLogger("main." + __name__)

class interfaceOrgSetting(Resource):

    def get(self):
        xml = request.args.get('format')
        try:
            data = orgSingleton_singleton.get_org_info()
            body = modelEnum.department.value.get('body')
            return response_result_process(data, xml_structure_str=body, xml=xml)

        except Exception as e:
            logger.error("FN:interfaceOrgSetting_get error:{}".format(traceback.format_exc()))
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
            logger.debug("FN:interfaceOrgSetting_POST request_data:{}".format(request_data))
            # form/w/u-t-adjij+team.xeex
            logger.debug('FN:interfaceOrgSetting_POST orgApiPara.setOrg_POST_request:{}'.format(orgApiPara.setOrg_POST_request))
            request_data = req.verify_all_param(request_data, orgApiPara.setOrg_POST_request)
            # try:
            #     f = request.files['cer_path']
            #     upload_path = './data/ldap_file/'
            #     if not os.path.exists(upload_path):
            #         os.makedirs(upload_path)
            #     upload_path += f.filename
            #     f.save(upload_path)
            #     request_data['cer_path'] = upload_path
            # except:
            #     logger.error("FN:interfaceOrgSetting error:{}".format(traceback.format_exc()))
            #     pass
            use_ssl = request_data['use_ssl']
            logger.debug("FN:interfaceOrgSetting_POST use_ssl:{}".format(use_ssl))
            
            # Since the Flag is a true false, will convert them into int
            if (isinstance(use_ssl, str) and use_ssl.strip().lower() == "true") or use_ssl is True:
                use_ssl = 1
            else:
                use_ssl = 0
            # use_ssl = False
            # request_data['use_ssl'] = False
            account_dn = request_data['admin_dn']
            password = request_data['admin_pwd']

            host = request_data['host']
            port = request_data['port']

            login_flag = Auth.service_account_login(account_dn, password, host, port, use_ssl)
            if not login_flag:
                data = response_code.ADD_DATA_FAIL
                data['msg'] = 'LDAP VERIFY FAILED.'
                return data

            # check smtp connect
            smtp_host = request_data['smtp_host']
            smtp_account = request_data['smtp_account']
            smtp_pwd = request_data['smtp_pwd']
            smtp_port = request_data['smtp_port']
            smtp_tls = request_data['smtp_tls']

            if (isinstance(smtp_tls, str) and smtp_tls.strip().lower() == "true") or smtp_tls is True:
                smtp_tls = 1
            else:
                smtp_tls = 0

            # Verify the SMTP Email
            smtp_flag = Smtp.check_email_pwd(smtp_host, smtp_account, smtp_pwd, smtp_port, smtp_tls)
            if not smtp_flag:
                data = response_code.ADD_DATA_FAIL
                data['msg'] = 'SMTP VERIFY FAILED.'
                return data

            data = orgSingleton_singleton.add_new_org_setting(request_data)

            if data['code'] == 200:
                response_data = data['data']
                # logger.debug(response_data)
                data['data'] = req.verify_all_param(response_data, orgApiPara.setOrg_POST_response)
            # # logger.debug(data)
            return response_result_process(data, xml=xml)

        except Exception as e:
            logger.error("FN:interfaceOrgSetting_post error:{}".format(traceback.format_exc()))
            error_data = response_code.ADD_DATA_FAIL
            return response_result_process(error_data, xml=xml)


    # update the org info
    def put(self,):
        xml = request.args.get('format')
        try:
            request_data = req.request_process(request, xml, modelEnum.department.value)
            # # logger.debug('request_data:', request_data)
            if isinstance(request_data, bool):
                request_data = response_code.REQUEST_PARAM_FORMAT_ERROR
                return response_result_process(request_data, xml=xml)
            request_data = req.verify_all_param(request_data, orgApiPara.updateOrg_POST_request)

            use_ssl = request_data['use_ssl']
            logger.debug("FN:interfaceOrgSetting_POST use_ssl:{}".format(use_ssl)) 

            # Since the Flag is a true false, will convert them into int
            if (isinstance(use_ssl, str) and use_ssl.strip().lower() == "true") or use_ssl is True:
                use_ssl = 1
            else:
                use_ssl = 0
            account_dn = request_data['admin_dn']
            password = request_data['admin_pwd']

            host = request_data['host']
            port = request_data['port']

            login_flag = Auth.service_account_login(account_dn, password, host, port, use_ssl)
            if not login_flag:
                data = response_code.ADD_DATA_FAIL
                data['msg'] = 'LDAP VERIFY FAILED.'
                return data

            # check smtp connect
            smtp_host = request_data['smtp_host']
            smtp_account = request_data['smtp_account']
            smtp_pwd = request_data['smtp_pwd']
            smtp_port = request_data['smtp_port']
            smtp_tls = request_data['smtp_tls']
            if (isinstance(smtp_tls, str) and smtp_tls.strip().lower() == "true") or smtp_tls is True:
                smtp_tls = 1
            else:
                smtp_tls = 0
            
            smtp_flag = Smtp.check_email_pwd(smtp_host, smtp_account, smtp_pwd, smtp_port, smtp_tls)
            if not smtp_flag:
                data = response_code.ADD_DATA_FAIL
                data['msg'] = 'SMTP VERIFY FAILED.'
                return data

            data = orgSingleton_singleton.update_org(request_data)
            if data['code'] == 200:
                response_data = data['data']
                data['data'] = req.verify_all_param(response_data, orgApiPara.updateOrg_POST_response)
            # # logger.debug(data)
            return response_result_process(data, xml=xml)

        except Exception as e:
            logger.error("FN:interfaceOrgSetting_put error:{}".format(traceback.format_exc()))
            error_data = response_code.ADD_DATA_FAIL
            return response_result_process(error_data, xml=xml)
