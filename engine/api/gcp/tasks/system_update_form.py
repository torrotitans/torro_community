from api.gcp.tasks.baseTask import baseTask
from core.form_singleton import formSingleton_singleton
import logging
from googleapiclient.errors import HttpError
from utils.status_code import response_code
import traceback
import json

logger = logging.getLogger("main.api.gcp.tasks" + __name__)

class system_update_form(baseTask):
    api_type = 'system'
    api_name = 'system_update_form'
    arguments = {
        "id": {"type": int, "default": -1},
        "form_name": {"type": str, "default": ''},
        'description': {"type": str, "default": ''},
        "field_list": {"type": list, "default": []},
                 }

    def __init__(self, stage_dict):
        super(system_update_form, self).__init__(stage_dict)
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
                id = self.stage_dict['id']
                form_name = self.stage_dict['form_name']
                description = self.stage_dict['description']
                field_list = self.stage_dict['field_list']
                form = {'id': id, 'title': form_name, 'des': description, 'fieldList': field_list}
                # print('form:', form)
                data = formSingleton_singleton.update_form(form, user_id, workspace_id)

                return data
        except HttpError as e:
            error_json = json.loads(e.content.replace('\\', '\\\\'), strict=False)
            data = error_json['error']
            data["msg"] = data.pop("message")
            logger.error("FN:system_update_form error:{}".format(traceback.format_exc()))
            return data
        except Exception as e:
            logger.error("FN:system_update_form error:{}".format(traceback.format_exc()))
            data = response_code.BAD_REQUEST
            data['msg'] = str(e)
            return data
if __name__ == '__main__':
    x = system_update_form({"form_name": 'Create from 2',
                            "description": 'Create from 2',
                            "field_list": '[{"default": "", "des": "", "edit": 1, "id": "u1", "label": "Form Name", "options": [], "placeholder": "", "style": 3}, {"default": "", "des": "", "edit": 1, "id": "u2", "label": "Form Description", "options": [], "placeholder": "", "style": 3}, {"default": "", "des": "", "edit": 1, "id": "u3", "label": "fieldList", "options": [], "placeholder": "", "style": 3}]',
                            })
    x.execute()

