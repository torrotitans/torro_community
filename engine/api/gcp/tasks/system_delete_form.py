from api.gcp.tasks.baseTask import baseTask
from core.form_singleton import formSingleton_singleton
import logging
from googleapiclient.errors import HttpError
from utils.status_code import response_code
import traceback
import json
logger = logging.getLogger("main.api.gcp.tasks" + __name__)
class system_delete_form(baseTask):
    api_type = 'system'
    api_name = 'system_delete_form'
    arguments = {
        "id": {"type": int, "default": -1},
                 }

    def __init__(self, stage_dict):
        super(system_delete_form, self).__init__(stage_dict)
        # print('stage_dict:', stage_dict)
    def execute(self, workspace_id=None, form_id=None, input_form_id=None, user_id=None):
        try:
            missing_set = set()
            for key in self.arguments:
                check_key = self.stage_dict.get(key, 'NotFound')
                if check_key == 'NotFound':
                    missing_set.add(key)
                # # print('{}: {}'.format(key, self.stage_dict[key]))
            if len(missing_set) != 0:
                data = response_code.BAD_REQUEST
                data['msg'] = 'Missing parameters: {}'.format(', '.join(missing_set))
                return data
            else:
                form_id = self.stage_dict['id']
                form = {'id': form_id}

                data = formSingleton_singleton.delete_form(form)
                return data
        except HttpError as e:
            error_json = json.loads(e.content)
            data = error_json['error']
            data["msg"] = data.pop("message")
            logger.error("FN:system_delete_form error:{}".format(traceback.format_exc()))
            return data
        except Exception as e:
            logger.error("FN:system_delete_form error:{}".format(traceback.format_exc()))
            data = response_code.BAD_REQUEST
            data['msg'] = str(e)
            return data