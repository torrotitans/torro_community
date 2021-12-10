import abc
from common.common_request_process import req
from common.common_response_code import response_code
import json
class baseTask(metaclass=abc.ABCMeta):
    api_type = 'system'
    api_name = 'baseTask'
    arguments = {}
    role_list = []
    target_project = None
    full_resource_name = None
    def __init__(self, stage_dict):
        self.stage_dict = stage_dict

    def verify_all_param(self):
        self.stage_dict = req.verify_all_param(self.stage_dict, self.arguments)

    @abc.abstractmethod
    def execute(self, *args, **kwargs):
        pass

    # @abc.abstractmethod
    def message_tranfer(self, log):
        data = response_code.SUCCESS
        if isinstance(log, dict):
            data['data'] = json.dumps(log)
        elif isinstance(log, list):
            data['data'] = json.dumps(log)
        else:
            data['data'] = str(log).replace('\'', '"')
        return data
