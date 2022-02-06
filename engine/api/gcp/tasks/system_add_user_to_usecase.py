from api.gcp.tasks.baseTask import baseTask
from db.base import DbBase
from db.usecase.db_usecase_mgr import usecase_mgr
import json
import datetime
from db.connection_pool import MysqlConn
from utils.log_helper import lg
from utils.status_code import response_code
from config import configuration

class system_add_user_to_usecase(baseTask, DbBase):
    api_type = 'system'
    api_name = 'system_add_user_to_usecase'
    arguments = {
        'usecase_name': {"type": str, "default": ''},
        "user_name": {"type": str, "default": ''},
    }

    def __init__(self, stage_dict):
        super(system_add_user_to_usecase, self).__init__(stage_dict)
        # print('stage_dict:', stage_dict)
    def execute(self, workspace_id=None, form_id=None, input_form_id=None, user_id=None):

        conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            missing_set = set()
            for key in self.arguments:
                check_key = self.stage_dict.get(key, 'NotFound')
                if check_key == 'NotFound':
                    missing_set.add(key)
                # # print('{}: {}'.format(key, self.stage_dict[key]))
            if len(missing_set) != 0:
                return 'Missing parameters: {}'.format(', '.join(missing_set))
            else:
                # print('self.stage_dict:', self.stage_dict)
                usecase_name = self.stage_dict['usecase_name']
                user_name = self.stage_dict['user_name']
                condition = "USECASE_NAME='%s'" % usecase_name

                data = response_code
                if data['code'] == 200:
                    return 'create new usecase successfully.'
                else:
                    return data['msg']
        except Exception as e:
            lg.error(e)
            import traceback
            # print(traceback.format_exc())
            return response_code.ADD_DATA_FAIL
        finally:
            conn.close()

if __name__ == '__main__':
    x = system_add_user_to_usecase({"form_name": 'Create from 2',
                            "description": 'Create from 2',
                            "field_list": '[{"default": "", "des": "", "edit": 1, "id": "u1", "label": "Form Name", "options": [], "placeholder": "", "style": 3}, {"default": "", "des": "", "edit": 1, "id": "u2", "label": "Form Description", "options": [], "placeholder": "", "style": 3}, {"default": "", "des": "", "edit": 1, "id": "u3", "label": "fieldList", "options": [], "placeholder": "", "style": 3}]',
                            })
    x.execute()

