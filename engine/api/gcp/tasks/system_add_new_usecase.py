from api.gcp.tasks.baseTask import baseTask
from db.base import DbBase
from db.usecase.db_usecase_mgr import usecase_mgr
import json
import datetime
class system_add_new_usecase(baseTask, DbBase):
    api_type = 'system'
    api_name = 'system_add_new_usecase'
    arguments = {
        'usecase_name': {"type": str, "default": ''},
        "region_country": {"type": str, "default": ''},
        'validity_date': {"type": str, "default": ''},
        "uc_des": {"type": str, "default": ''},
        'admin_sa': {"type": str, "default": ''},
        "budget": {"type": str, "default": ''},
        'allow_cross_region': {"type": str, "default": ''},
        "resources_access": {"type": str, "default": ''},
        "uc_team_group": {"type": str, "default": ''},
        "uc_owner_group": {"type": str, "default": ''},
    }

    def __init__(self, stage_dict):
        super(system_add_new_usecase, self).__init__(stage_dict)
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
            # print('self.stage_dict:', self.stage_dict)
            usecase_info = {'workspace_id': workspace_id}
            usecase_info['region_country'] = self.stage_dict['region_country']
            usecase_info['validity_date'] = self.stage_dict['validity_date']
            usecase_info['uc_des'] = self.stage_dict['uc_des']
            usecase_info['admin_sa'] = self.stage_dict['admin_sa']
            usecase_info['budget'] = self.stage_dict['budget']
            usecase_info['allow_cross_region'] = self.stage_dict['allow_cross_region']
            usecase_info['usecase_name'] = self.stage_dict['usecase_name']
            usecase_info['resources_access'] = self.stage_dict['resources_access']
            usecase_info['uc_team_group'] = self.stage_dict['uc_team_group']
            uc_owner_group = self.stage_dict['uc_owner_group']
            usecase_info['uc_owner_group'] = uc_owner_group
            usecase_info['uc_input_form'] = input_form_id

            data = usecase_mgr.add_new_usecase_setting(usecase_info)

            if data['code'] == 200:
                usecase_id = data['data']['usecase_id']
                data1 = usecase_mgr.update_usecase_resource(workspace_id, usecase_id, uc_owner_group)

                return 'create new usecase successfully.'
            else:
                return data['msg']

if __name__ == '__main__':
    x = system_add_new_usecase({"form_name": 'Create from 2',
                            "description": 'Create from 2',
                            "field_list": '[{"default": "", "des": "", "edit": 1, "id": "u1", "label": "Form Name", "options": [], "placeholder": "", "style": 3}, {"default": "", "des": "", "edit": 1, "id": "u2", "label": "Form Description", "options": [], "placeholder": "", "style": 3}, {"default": "", "des": "", "edit": 1, "id": "u3", "label": "fieldList", "options": [], "placeholder": "", "style": 3}]',
                            })
    x.execute()

