#!/usr/bin/python
# -*- coding: UTF-8 -*

from core.gcp_singleton import gcpSingleton_singleton
from utils.log_helper import lg
from utils.status_code import response_code
from flask import request
from common.common_request_process import req
# from core.governance_singleton import governance_singleton
from common.common_model_enum import modelEnum
from common.common_response_process import response_result_process
from common.common_login_helper import login_required
from db.gcp.db_gcp_parameter import gcpApiPara
from flask_restful import Resource
import traceback
class interfaceTableSchema(Resource):

    @login_required
    def post(self,):

        """Get table schema

        @@@
        ### args
        |  args | nullable | request type | type |  remarks |
        |-------|----------|--------------|------|----------|
        | projectId |  false   |    body      | str  | project id    |
        | datasetName |  false   |    body      | str  | dataset id  |
        | tableName |  false   |    body      | str  | table id    |

        ### request
        ```json
        {"projectId": "geometric-ocean-333410", "datasetName": "testing1", "tableName": "table1"}
        ```

        ### return
        ```json
        {
            "code": 200,
            "msg": "request successfully",
            "data": {
                "kind": "bigquery#table",
                "etag": "s0eXcEXHm+NEVHzocRX81g==",
                "id": "geometric-ocean-333410:testing1.table1",
                "selfLink": "https://bigquery.googleapis.com/bigquery/v2/projects/geometric-ocean-333410/datasets/testing1/tables/table1",
                "tableReference": {
                    "projectId": "geometric-ocean-333410",
                    "datasetId": "testing1",
                    "tableId": "table1"
                },
                "description": "Updated Policy Tags.",
                "schema": {
                    "fields": [
                        {
                            "name": "a",
                            "type": "STRING",
                            "mode": "NULLABLE",
                            "policyTags": {
                                "names": [
                                    "projects/geometric-ocean-333410/locations/asia-east2/taxonomies/1346075789958397800/policyTags/8605754121758499097"
                                ]
                            },
                            "tags": [
                                {
                                    "tag_template_form_id": 401,
                                    "data": {
                                        "u1": "b",
                                        "u2": "a"
                                    }
                                }
                            ]
                        },
                        {
                            "name": "b",
                            "type": "STRING",
                            "mode": "NULLABLE",
                            "policyTags": {
                                "names": [
                                    "projects/geometric-ocean-333410/locations/asia-east2/taxonomies/1346075789958397800/policyTags/8605754121758499097"
                                ]
                            }
                        }
                    ]
                },
                "numBytes": "0",
                "numLongTermBytes": "0",
                "numRows": "0",
                "creationTime": "1638080195395",
                "lastModifiedTime": "1638613188170",
                "type": "TABLE",
                "location": "asia-east2",
                "tags": [
                    {}
                ]
            }
        }
        ```
        @@@
        """


        try:

            user_key = req.get_user_key()
            account_id = req.get_user_account_id()
            workspace_id = req.get_workspace_id()

            xml = request.args.get('format')

            request_data = req.request_process(request, xml, modelEnum.department.value)
            if isinstance(request_data, bool):
                request_data = response_code.REQUEST_PARAM_FORMAT_ERROR
                return response_result_process(request_data, xml=xml)

            # request_data = req.verify_all_param(request_data, gcpApiPara.execute_gcp_tasks_POST_request)
            data = gcpSingleton_singleton.get_table_schema(request_data, user_key, workspace_id)
            return data
        except Exception as e:
            lg.error(traceback.format_exc())
            error_data = response_code.GET_DATA_FAIL
            return error_data

    @login_required
    def put(self,):

        """Get table schema

        @@@
        ### args
        |  args | nullable | request type | type |  remarks |
        |-------|----------|--------------|------|----------|
        | projectId |  false   |    body      | str  | project id    |
        | datasetName |  true   |    body      | str  | dataset id  |
        | tableName |  true   |    body      | str  | table id    |

        ### request
        ```json
        {"projectId": "geometric-ocean-333410"}
        ```
        or
        ```json
        {"projectId": "geometric-ocean-333410", "datasetName": "testing1"}
        ```
        ### return
        if only pass project id, will return the dataset list
        ```json
        {
            "code": 200,
            "msg": "request successfully",
            "data": [
                "testing1"
            ]
        }
        ```
        if pass project id & dataset id, will return the table list
        ```json
        {
            "code": 200,
            "msg": "request successfully",
            "data": [
                "table1"
            ]
        }
        ```
        @@@
        """
        try:

            user_key = req.get_user_key()
            account_id = req.get_user_account_id()
            workspace_id = req.get_workspace_id()

            xml = request.args.get('format')

            request_data = req.request_process(request, xml, modelEnum.department.value)
            if isinstance(request_data, bool):
                request_data = response_code.REQUEST_PARAM_FORMAT_ERROR
                return response_result_process(request_data, xml=xml)

            # request_data = req.verify_all_param(request_data, gcpApiPara.execute_gcp_tasks_POST_request)
            data = gcpSingleton_singleton.list_table(request_data, user_key, workspace_id)
            return data
        except Exception as e:
            lg.error(traceback.format_exc())
            error_data = response_code.GET_DATA_FAIL
            return error_data



