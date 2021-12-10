
class usecaseApiPara:
    getUsecase_GET_response = {}
    getUseCase_POST_request = {"ad_group_list": {"type": list, "default": []}}
    setUseCase_POST_request = {"usecase_name": {"type": str, "default": ''},
                           "group_dict": {"type": dict, "default": []},
                           "gcp_project": {"type": str, "default": ''},
                           "admin_sa": {"type": str, "default": ''},
                            "admin_sa_path": {"type": str, "default": ''},
                            "des": {"type": str, "default": ''}},
    updateUseCase_POST_request = {"usecase_id": {"type": int, "default": -1},
                            "usecase_name": {"type": str, "default": ''},
                           "group_dict": {"type": dict, "default": []},
                           "gcp_project": {"type": str, "default": ''},
                           "admin_sa": {"type": str, "default": ''},
                                    "admin_sa_path": {"type": str, "default": ''},
                                    "des": {"type": str, "default": ''}},


    getUseCase_POST_response = {"usecase_infos": {"type": list, "default": []}},
    setUseCase_POST_response = {"usecase_id": {"type": int, "default": -1},
                            "usecase_name": {"type": str, "default": ''},
                           "group_dict": {"type": dict, "default": []},
                           "gcp_project": {"type": str, "default": ''},
                           "admin_sa": {"type": str, "default": ''},
                                  "admin_sa_path": {"type": str, "default": ''},
                                  "des": {"type": str, "default": ''}}
    updateUseCase_POST_response = {"usecase_id": {"type": int, "default": -1},
                            "usecase_name": {"type": str, "default": ''},
                           "group_dict": {"type": dict, "default": []},
                           "gcp_project": {"type": str, "default": ''},
                           "admin_sa": {"type": str, "default": ''},
                                  "admin_sa_path": {"type": str, "default": ''},
                                  "des": {"type": str, "default": ''}}