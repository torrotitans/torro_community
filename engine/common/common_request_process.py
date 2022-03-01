#!/usr/bin/python
# -*- coding: UTF-8 -*

import json
from json import JSONDecodeError
from common.common_api_version import apiVersion
from common.common_response_code import response_code
from common.common_response_log import ResponseLog
from common.common_response_process import response_result_process
from utils.xml_json_process import xml_to_json, is_none
from flask import g
import logging

logger = logging.getLogger("main." + __name__)

class requestProcess(object):

    def get_user_key(self):
        try:
            user_key = g.user_key
        except:
            user_key = 1
        return user_key
    
    def get_user_account_id(self,):
        try:
            user_key = g.user_key
            # # print(user_key)
            account_id = g.account_id
        except:
            account_id = 'TorroAdmin'
        return account_id

    def get_workspace_id(self,):
        try:
            user_key = g.user_key
            # # print(user_key)
            workspace_id = g.workspace_id
            
            # if not isinstance(workspace_id, (int, str)):
            #     workspace_id = 0
            workspace_id = int(workspace_id)

        except:
            workspace_id = 0
        return workspace_id

    def _xml_request(self, request, model_json=None):
        try:
            data = request.data
            temp = data.decode('utf-8')
            
            if temp == '':
                return {}
            
            try:
                param_temp = xml_to_json(temp)
            except Exception as e:
                return response_code.REQUEST_PARAM_FORMAT_ERROR
            
            param = json.loads(param_temp)

            root = model_json.get('root')
            body = model_json.get('body')
            root_data = param.get(root)
            request_param = None
            
            if root_data:
                body_data = root_data.get(body)
                if body_data:
                    if isinstance(body_data,list):
                        request_param = is_none(root_data)
                    else:
                        request_param = is_none(body_data)
                        
            if root_data is None:
                s_body_data = param.get(body)
                if s_body_data:
                    if isinstance(is_none(s_body_data), dict):
                        request_param = s_body_data

            if isinstance(request_param, list) or request_param is None:
                return False
            return request_param
        
        except Exception as e:
            logger.error("FN:_xml_request error:{}".format(e))
            return False

    def _json_request(self, request):
        try:
            request_data = request.data
            req_str = request_data.decode()
            
            if req_str == '':
                form_data = request.form
                data = {}
                
                for key in form_data:
                    try:
                        data[key] = json.loads(form_data[key])
                    except:
                        data[key] = form_data[key]
                        
                return data
            
            data = json.loads(req_str)
            
            if isinstance(data, list):
                return False
            return data
        
        except JSONDecodeError as e:
            logger.error("FN:_json_request error:{}".format(e))
            return False

    def verify_one_param_type(self, param_name, value, type=None):
        try:
            
            if type == float:
                v = None
                if isinstance(value,str):
                    v = eval(value)
                if isinstance(value,int):
                    v = value
                if isinstance(value,float):
                    v = value
                if isinstance(v, float):
                    pass
                else:
                    code = response_code.BAD_REQUEST
                    code['msg'] = ResponseLog.wrong_param_type(param_name, type.__name__)
                    return code
            if type == int:
                v = None
                if isinstance(value, str):
                    v = eval(value)
                if isinstance(value, float):
                    v = value
                if isinstance(value, int):
                    v = value
                if isinstance(v, int):
                    pass
                else:
                    code = response_code.BAD_REQUEST
                    code['msg'] = ResponseLog.wrong_param_type(param_name, type.__name__)
                    return code
            if type == str:
                if isinstance(value, str):
                    pass
                else:
                    code = response_code.BAD_REQUEST
                    code['msg'] = ResponseLog.wrong_param_type(param_name, type.__name__)
                    return code

            if type == list:
                v = None
                if isinstance(value, list):
                    pass
                elif isinstance(value, str):
                    try:
                        v = list(value)
                    except:
                        code = response_code.BAD_REQUEST
                        code['msg'] = ResponseLog.wrong_param_type(param_name, type.__name__)
                        return code
                else:
                    code = response_code.BAD_REQUEST
                    code['msg'] = ResponseLog.wrong_param_type(param_name, type.__name__)
                    return code
            if type == dict:
                if isinstance(value, dict):
                    pass
                elif isinstance(value, str):
                    try:
                        v = dict(value)
                    except:
                        code = response_code.BAD_REQUEST
                        code['msg'] = ResponseLog.wrong_param_type(param_name, type.__name__)
                        return code
                else:
                    code = response_code.BAD_REQUEST
                    code['msg'] = ResponseLog.wrong_param_type(param_name, type.__name__)
                    return code
        except Exception as e:
            logger.error("FN:verify_one_param_type error:{}".format(e))
            code = response_code.BAD_REQUEST
            code['msg'] = ResponseLog.wrong_param_type(param_name, type.__name__)
            return code

    def verify_one_param_must(self, request_data: dict, param):

        if request_data.get(param) is None:
            code = response_code.BAD_REQUEST
            code['msg'] = ResponseLog.wrong_param_must(param)
            return code
        else:
            pass

    def verify_one_param(self, request_data: dict, param):

        if request_data.get(param) is None:
            return True
        else:
            return False


    def verify_param_page(self, data, param):

        page_data = data.get(param)
        if page_data.get('page_size') is not None:
            if page_data.get('current_page') is None:
                code = response_code.BAD_REQUEST
                code['msg'] = ResponseLog.wrong_param_must('current_page')
                return code
        if page_data.get('current_page') is not None:
            if page_data.get('page_size') is None:
                code = response_code.BAD_REQUEST
                code['msg'] = ResponseLog.wrong_param_must('page_size')
                return code

    def request_process(self, request, xml=None, model_json=None):
        """
        :param request: request
        :param xml:  Check return as or xml?  Default is json
        :return:
        """
        if xml is None:
            return self._json_request(request)
        if xml == 'xml':
            return self._xml_request(request, model_json)

    def verify_all_param_must(self, request_data: dict, fields: list):
        """
        :param request_data: request param data
        :param fields: ['a','b']
        :return:
        """
        for i in fields:
            must = self.verify_one_param_must(request_data, i)
            if must:
                return must
            else:
                pass

    def verify_all_param(self, request_data: dict, fields: dict):
        """
        :param request_data: request param data
        :param fields: ['a','b']
        :return:
        """
        if type(fields) == tuple:
            fields = fields[0]
        for i in fields:
            must = self.verify_one_param(request_data, i)
            if must:
                request_data[i] = fields[i]['default']
            else:
                logger.debug("FN:verify_all_param field:{} request_data:{} field_type:{}".format(i, request_data, fields[i]['type']))
                param_type = self.verify_one_param_type(i, request_data[i], fields[i]['type'])
                if param_type:
                    request_data[i] = fields[i]['default']
        return request_data

    def verify_all_param_type(self, request_data: dict, fields: dict):
        """
        :param request_data: request param data
        :param fields: {'a':str,'b':int}
        :return:
        """

        for k, v in request_data.items():
            # logger.debug("FN:verify_all_param_type k:{} v:{} field_get:{}".format(k, v, fields.get(k)))
            param_type = self.verify_one_param_type(k, v, fields.get(k))
            if param_type:
                return param_type
            else:
                pass

    def verify_version(self, version, xml=None):
        """
        :param version:
        :param xml: Check xml
        :return:
        """
        if version == apiVersion.version1.value:
            return True, True
        else:  # 版本信息不存在给的提示
            result = response_code.REQUEST_VERSION_ISEXISTENCE
            return False, response_result_process(result, xml=xml)


req = requestProcess()
