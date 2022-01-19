#!/usr/bin/python
# -*- coding: UTF-8 -*
"""
@author：li-boss
@file_name: interface_login.py
@create date: 2019-10-27 14:36 
@blog https://leezhonglin.github.io
@csdn https://blog.csdn.net/qq_33196814
@file_description：
"""
from common.common_login_helper import login_required
from flask import request
from flask_restful import Resource
import os
from common.common_response_process import response_result_process
from utils.log_helper import lg
from utils.status_code import response_code
import json
import traceback


class interfaceTorroConfig(Resource):
    base_dir = 'torroConfig/'
    @login_required
    def get(self, configName=None):

        """Get config json (just support getting json file)

        @@@

        ### return
        Call ./api/torroConfig/folderName.fileName; split every folder using '.' not '/'.
        Such as getting json: torroConfig/testing/sub1/t2.json, you should call api /api/torroConfig/testing.sub1.t2 or /api/torroConfig/testing.sub1.t2.json.
        ```json
        {
            "code": 200,
            "msg": "request successfully",
            "data": {
                "gcp": [
                    {
                        "default": "GCP",
                        "des": "Resource type",
                        "edit": 1,
                        "id": "resourceType",
                        "label": "Resource type",
                        "options": [
                            {
                                "label": "GCP"
                            },
                            {
                                "label": "Hive"
                            }
                        ],
                        "placeholder": "Resource type",
                        "style": 8,
                        "required": true,
                        "width": 100
                    },
                    {
                        "default": "",
                        "des": "GCP Project",
                        "edit": 1,
                        "id": "projectId",
                        "label": "GCP Project",
                        "options": [],
                        "placeholder": "GCP Project",
                        "style": 3,
                        "required": true
                    },
                    {
                        "default": "",
                        "des": "Dataset",
                        "edit": 1,
                        "id": "datasetName",
                        "label": "Dataset",
                        "options": [],
                        "placeholder": "Dataset",
                        "style": 3,
                        "required": true
                    },
                    {
                        "default": "",
                        "des": "Table",
                        "edit": 1,
                        "id": "tableName",
                        "label": "Table name",
                        "options": [],
                        "placeholder": "Table",
                        "style": 3,
                        "required": true
                    }
                ],
                "hive": [
                    {
                        "default": "GCP",
                        "des": "Resource type",
                        "edit": 1,
                        "id": "resourceType",
                        "label": "Resource type",
                        "options": [
                            {
                                "label": "GCP"
                            },
                            {
                                "label": "Hive"
                            }
                        ],
                        "placeholder": "Resource type",
                        "style": 8,
                        "required": true,
                        "width": 100
                    },
                    {
                        "default": "",
                        "des": "Service path",
                        "edit": 1,
                        "id": "projectId",
                        "label": "Service path",
                        "options": [],
                        "placeholder": "Service path",
                        "style": 3,
                        "required": true
                    },
                    {
                        "default": "",
                        "des": "Database",
                        "edit": 1,
                        "id": "datasetName",
                        "label": "Database",
                        "options": [],
                        "placeholder": "Database",
                        "style": 3,
                        "required": true
                    },
                    {
                        "default": "",
                        "des": "Table",
                        "edit": 1,
                        "id": "tableName",
                        "label": "Table",
                        "options": [],
                        "placeholder": "Table name",
                        "style": 3,
                        "required": true
                    }
                ]
            }
        }
        ```
        @@@
        """
        xml = request.args.get('format')

        try:

            if not configName:
                data = response_code.GET_DATA_FAIL
                data['msg'] = 'please input your config file name.'
                return data
            print('configName:', configName)
            configName = configName.replace('.json', '')
            file_name = configName.replace('.', '/')
            full_name = self.base_dir+file_name+'.json'
            if not os.path.exists(full_name):
                data = response_code.GET_DATA_FAIL
                data['msg'] = 'can not find file:'+full_name
                return data
            else:
                file = open(full_name, 'r')
                json_data = json.load(file)
                file.close()
                data = response_code.SUCCESS
                data['data'] = json_data
                return data

        except Exception as e:
            lg.error(traceback.format_exc())
            error_data = response_code.GET_DATA_FAIL
            return response_result_process(error_data, xml=xml)