
class formApiPara:

    getFormList_GET = {}

    getFormData_POST_request = {"id": {"type": int, "default": 355}}
    getFormData_POST_response = {"id": {"type": int, "default": 355},
                                 "title": {"type": str, "default": ''},
                                 "fields_num": {"type": int, "default": 0},
                                 "u_max_id": {"type": int, "default": 0},
                                 "creator_id": {"type": str, "default": ''},
                                 "fields_list": {"type": list(), "default": []},
                                 "des": {"type": str, "default": ''},}

    postFormData_POST_request = {"title": {"type": str, "default": ""},
                         "fieldList": {"type": list(), "default": []},
                         "des": {"type": str, "default": ""},
                         "creator_id": {"type": str, "default": ""}
                         }
    postFormData_POST_response = {"title": {"type": str, "default": ""},
                         "fieldList": {"type": list(), "default": []},
                         "des": {"type": str, "default": ""},
                         "creator_id": {"type": str, "default": ""}
                         }

    postFormData_PULL_response = {"id": {"type": int, "default": -1},
                         "title": {"type": str, "default": ""},
                         "fieldList": {"type": list(), "default": []},
                         "des": {"type": str, "default": ""},
                         "creator_id": {"type": str, "default": ""}
                         }

    postFormData_PULL_request = {"id": {"type": int, "default": -1},
                         "title": {"type": str, "default": ""},
                         "fieldList": {"type": list(), "default": []},
                         "des": {"type": str, "default": ""},
                         "creator_id": {"type": str, "default": ""}
                         }

    postFormData_DELETE_request = {"id": {"type": int, "default": -1}}
    postFormData_DELETE_response = {"id": {"type": int, "default": -1}}

    getFieldTemplate_POST_request = {"style": {"type": int, "default": 3}}
    getFieldTemplate_POST_response = {"style": {"type": int, "default": 3}}





