#!/usr/bin/python
# -*- coding: UTF-8 -*

from utils.api_version_verify import api_version
from flask import request
from flask_restful import Resource
from core.form_singleton import formSingleton_singleton
from utils.status_code import response_code
from common.common_model_enum import modelEnum
from common.common_response_process import response_result_process
from common.common_login_helper import login_required
from common.common_request_process import req
from db.form.db_form_parameter import formApiPara
import traceback
import logging

logger = logging.getLogger("main." + __name__)

class interfaceBaseForm(Resource):

    # @api_version
    @login_required
    def get(self, system=None):

        """Get form list

        @@@

        ### return
        if call ./api/getFormList/1, get all the form
        if call ./api/getFormList/0, get user defined form
        ```json
        {
            "code": 200,
            "data": [
                {
                    "create_time": "Sun, 22 Aug 2021 00:00:00 GMT",
                    "creator_id": "",
                    "des": "try update",
                    "fields_num": 10,
                    "id": 2,
                    "title": "Create Use Case",
                    "u_max_id": "u10",
                    "updated_time": "Thu, 07 Oct 2021 09:55:04 GMT"
                }
            ],
            "msg": "request successfully"
        }
        ```
        @@@
        """
        xml = request.args.get('format')

        try:
            workspace_id = req.get_workspace_id()
            data = formSingleton_singleton.get_all_base_form(workspace_id, system=system)
            body = modelEnum.department.value.get('body')
            return response_result_process(data, xml_structure_str=body, xml=xml)
        except Exception as e:
            logger.error("FN:interfaceBaseForm error:{}".format(traceback.format_exc()))
            error_data = response_code.GET_DATA_FAIL
            return response_result_process(error_data, xml=xml)


