from api.gcp.tasks.baseTask import baseTask
from db.base import DbBase
from db.connection_pool import MysqlConn
from config import configuration
import datetime
from core.form_singleton import formSingleton_singleton

class system_delete_form(baseTask, DbBase):
    api_type = 'system'
    api_name = 'system_delete_form'
    arguments = {
        "id": {"type": int, "default": -1},
                 }

    def __init__(self, stage_dict):
        super(system_delete_form, self).__init__(stage_dict)
        # print('stage_dict:', stage_dict)
    def execute(self, workspace_id=None, form_id=None, input_form_id=None, user_id=None):
        missing_set = set()
        for key in self.arguments:
            check_key = self.stage_dict.get(key, 'NotFound')
            if check_key == 'NotFound':
                missing_set.add(key)
            # # print('{}: {}'.format(key, self.stage_dict[key]))
        if len(missing_set) != 0:
            return 'Missing parameters: {}'.format(', '.join(missing_set))
        else:
            form_id = self.stage_dict['id']
            form = {'id': form_id}

            data = formSingleton_singleton.delete_form(form)
            if data['code'] == 200:
                return 'Delete successfully.'
            else:
                return data['msg']
