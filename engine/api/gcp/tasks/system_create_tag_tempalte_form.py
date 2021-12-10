from api.gcp.tasks.baseTask import baseTask
from db.base import DbBase
import json
from utils.log_helper import lg
from core.form_singleton import formSingleton_singleton
from core.workflow_singleton import workflowSingleton_singleton
from db.connection_pool import MysqlConn
from config import configuration

class system_create_tag_template_form(baseTask, DbBase):
    api_type = 'system'
    api_name = 'system_create_tag_template_form'
    arguments = {
        "form_name": {"type": str, "default": ''},
        'description': {"type": str, "default": ''},
        "field_list": {"type": list, "default": []},
                 }

    def __init__(self, stage_dict):
        super(system_create_tag_template_form, self).__init__(stage_dict)
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
                form_name = self.stage_dict['form_name']
                description = self.stage_dict['description']
                field_list = self.stage_dict['field_list']
                form = {'title': form_name, 'des': description, 'fieldList': field_list, 'hide': 1}
                # print('form:', form)
                data = formSingleton_singleton.add_new_form(form, workspace_id)
                print('tags table data:', data)
                if data['code'] == 200:
                    # workflow = {}
                    # workflowSingleton_singleton.add_new_workflow(workflow)
                    tag_tempalte_form_id = data['data']['id']
                    fields = ('tag_template_form_id',)
                    values = (tag_tempalte_form_id,)
                    condition = "workspace_id='%s' and input_form_id='%s' and creator_id='%s'" % (workspace_id, input_form_id, user_id)
                    sql = self.create_update_sql(db_name, 'tagTemplatesTable', fields, values, condition=condition)
                    print('tagTemplatesTable create_update_sql:', sql)
                    return_count = self.updete_exec(conn, sql)
                    print('return_count:', return_count)
                    return 'create successfully.'
                else:
                    return data['msg']
        except Exception as e:

            import traceback
            lg.error(traceback.format_exc())
        finally:
            conn.close()
if __name__ == '__main__':
    x = system_create_tag_template_form({"form_name": 'Create from 2',
                            "description": 'Create from 2',
                            "field_list": '[{"default": "", "des": "", "edit": 1, "id": "u1", "label": "Form Name", "options": [], "placeholder": "", "style": 3}, {"default": "", "des": "", "edit": 1, "id": "u2", "label": "Form Description", "options": [], "placeholder": "", "style": 3}, {"default": "", "des": "", "edit": 1, "id": "u3", "label": "fieldList", "options": [], "placeholder": "", "style": 3}]',
                            })
    x.execute()

