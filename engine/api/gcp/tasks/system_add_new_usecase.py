from api.gcp.tasks.baseTask import baseTask
from db.usecase.db_usecase_mgr import usecase_mgr


class system_add_new_usecase(baseTask):
    api_type = 'system'
    api_name = 'system_add_new_usecase'
    arguments = {
        'usecase_name': {"type": str, "default": ''},
        "region_country": {"type": str, "default": ''},
        'validity_date': {"type": str, "default": ''},
        "uc_des": {"type": str, "default": ''},
        'admin_sa': {"type": str, "default": ''},
        "budget": {"type": int, "default": 0},
        'allow_cross_region': {"type": str, "default": ''},
        "resources_access": {"type": str, "default": ''},
        "uc_team_group": {"type": str, "default": ''},
        "uc_owner_group": {"type": str, "default": ''},
        "uc_label": {"type": str, "default": ''},
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
            usecase_info = self.stage_dict
            usecase_info['workspace_id'] = workspace_id
            usecase_info['uc_input_form'] = input_form_id
            usecase_info['user_id'] = user_id
            # usecase_info = {'workspace_id': workspace_id}
            # uc_owner_group = self.stage_dict['uc_owner_group']
            # usecase_info['uc_owner_group'] = uc_owner_group
            
            data = usecase_mgr.add_new_usecase_setting(usecase_info)

            if data['code'] == 200:
                usecase_id = data['data']['usecase_id']
                data1 = usecase_mgr.update_usecase_resource(workspace_id, usecase_id, usecase_info['uc_owner_group'])

                return 'create new usecase successfully.'
            else:
                return data['msg']