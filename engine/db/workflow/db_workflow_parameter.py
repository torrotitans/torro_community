
class workflowApiPara:

    getAllStages_GET = {}

    getBaseWorkflowListByFormId_POST_request = {"form_id": {"type": int, "default": 351}}
    getBaseWorkflowListByFormId_POST_response = {"id": {"type": int, "default": -1},
                                                 "form_id": {"type": int, "default": '-1'},
                                                 "workflow_name": {"type": str, "default": ''},
                                                 # "stage_hash": {"type": str, "default": ''},
                                                 "stage_num": {"type": int, "default": 0},
                                                 "creator_id": {"type": str, "default": ''},
                                                 "last_modify_id": {"type": str, "default": ''},
                                                 "create_time": {"type": str, "default": '2021-05-03'},
                                                 "updated_time": {"type": str, "default": '2021-05-03'},
                                                 "des": {"type": str, "default": ''},}
    getDetailsWorkflowDataById_POST_request = {"id": {"type": int, "default": -1}}
    getDetailsWorkflowDataById_POST_response = {"id": {"type": int, "default": -1},
                                                 "form_id": {"type": int, "default": '-1'},
                                                 "workflow_name": {"type": str, "default": ''},
                                                 # "stage_hash": {"type": str, "default": ''},
                                                 "stage_num": {"type": int, "default": 0},
                                                 "creator_id": {"type": str, "default": ''},
                                                 "last_modify_id": {"type": str, "default": ''},
                                                 "stages": {"type": list, "default": []},
                                                "field_id_list": {"type": list, "default": []},
                                                 "create_time": {"type": str, "default": '2021-05-03'},
                                                 "updated_time": {"type": str, "default": '2021-05-03'},
                                                 "des": {"type": str, "default": ''}}


    postWorkflowData_POST_request = {"id": {"type": int, "default": -1},
                                     "form_id": {"type": int, "default": '-1'},
                                     "workflow_name": {"type": str, "default": ''},
                                     # "stage_hash": {"type": str, "default": ''},
                                     "stage_num": {"type": int, "default": 0},
                                     "creator_id": {"type": str, "default": ''},
                                     "last_modify_id": {"type": str, "default": ''},
                                     "stages": {"type": list, "default": []},
                                     "field_id_list": {"type": list, "default": []},
                                     "create_time": {"type": str, "default": '2021-05-03'},
                                     "updated_time": {"type": str, "default": '2021-05-03'},
                                     "des": {"type": str, "default": ''}}
    postWorkflowData_POST_response = {"id": {"type": int, "default": -1},
                                     "form_id": {"type": int, "default": '-1'},
                                     "workflow_name": {"type": str, "default": ''},
                                     # "stage_hash": {"type": str, "default": ''},
                                     "stage_num": {"type": int, "default": 0},
                                     "creator_id": {"type": str, "default": ''},
                                     "last_modify_id": {"type": str, "default": ''},
                                     "stages": {"type": list, "default": []},
                                      "field_id_list": {"type": list, "default": []},
                                     "create_time": {"type": str, "default": '2021-05-03'},
                                     "updated_time": {"type": str, "default": '2021-05-03'},
                                     "des": {"type": str, "default": ''}}

    postWorkflowData_PULL_response = {"id": {"type": int, "default": -1},
                                      "stage_hash": {"type": str, "default": ""}
                                      }

    postWorkflowData_PULL_request = {"id": {"type": int, "default": -1},
                                    "form_id": {"type": int, "default": '-1'},
                                    "workflow_name": {"type": str, "default": ''},
                                    "stage_hash": {"type": str, "default": ''},
                                    "stage_num": {"type": int, "default": 0},
                                    "creator_id": {"type": str, "default": ''},
                                    "last_modify_id": {"type": str, "default": ''},
                                    "stages": {"type": list, "default": []},
                                     "field_id_list": {"type": list, "default": []},
                                    "create_time": {"type": str, "default": '2021-05-03'},
                                    "updated_time": {"type": str, "default": '2021-05-03'},
                                    "des": {"type": str, "default": ''}}

    postWorkflowData_DELETE_request = {"id": {"type": int, "default": -1},
                                      "stage_hash": {"type": str, "default": ""}
                                       }
    postWorkflowData_DELETE_response = {"id": {"type": int, "default": -1},
                                        "form_id": {"type": int, "default": '-1'},
                                        "workflow_name": {"type": str, "default": ''},
                                        "stage_hash": {"type": str, "default": ''},
                                        "stage_num": {"type": int, "default": 0},
                                        "creator_id": {"type": str, "default": ''},
                                        "last_modify_id": {"type": str, "default": ''},
                                        "stages": {"type": list, "default": []},
                                        "field_id_list": {"type": list, "default": []},
                                        "create_time": {"type": str, "default": '2021-05-03'},
                                        "updated_time": {"type": str, "default": '2021-05-03'},
                                        "des": {"type": str, "default": ''}}

