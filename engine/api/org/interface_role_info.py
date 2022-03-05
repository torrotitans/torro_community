#!/usr/bin/python
# -*- coding: UTF-8 -*

import os
from utils.api_version_verify import api_version
from flask import request
from flask_restful import Resource
from core.org_singleton import orgSingleton_singleton
from utils.status_code import response_code
from common.common_model_enum import modelEnum
from common.common_response_process import response_result_process
from common.common_login_helper import login_required
from common.common_request_process import req
from db.org.db_org_parameter import orgApiPara
import traceback
import logging

logger = logging.getLogger("main." + __name__)

class interfaceRoleInfo(Resource):

    # get roles
    def get(self):
        try:
            xml = request.args.get('format')
            data = orgSingleton_singleton.get_roles_info()
            body = modelEnum.department.value.get('body')
            return response_result_process(data, xml_structure_str=body, xml=xml)

        except Exception as e:
            logger.error("FN:interfaceRoleInfo_get error:{}".format(traceback.format_exc()))
            error_data = response_code.GET_DATA_FAIL
            return response_result_process(error_data, xml=xml)

