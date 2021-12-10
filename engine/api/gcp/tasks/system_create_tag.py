from api.gcp.tasks.baseTask import baseTask
from db.base import DbBase
import json
import datetime
from core.input_form_singleton import input_form_singleton
from core.form_singleton import formSingleton_singleton
from db.connection_pool import MysqlConn
from utils.log_helper import lg
from utils.status_code import response_code
from config import configuration

class system_create_tag(baseTask, DbBase):
    api_type = 'system'
    api_name = 'system_create_tag'
    arguments = {}

    def __init__(self, stage_dict):
        super(system_create_tag, self).__init__(stage_dict)
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
                # get tag template id
                sql = self.create_select_sql(db_name, 'tagTemplatesTable', 'id,tag_template_form_id', condition="tag_template_form_id='%s' order by id desc" % form_id)
                print('tagTemplatesTable create_select_sql:', sql)
                tag_template_info = self.execute_fetch_all(conn, sql)
                tag_tempalte_local_id = tag_template_info[0]['id']
                input_form_data = input_form_singleton.get_input_form_data(user_id, input_form_id)
                form_data = formSingleton_singleton.get_details_form_by_id(form_id, workspace_id)
                print('input_form_data:', input_form_data)
                print('form_data:', form_data)
                if input_form_data['code'] == 200 and form_data['code'] == 200:
                    input_form_info = input_form_data['data'][0]
                    form_info = form_data['data']
                    form_field_values_dict = input_form_info['form_field_values_dict']
                    field_list = form_info['fieldList']
                    # get tag fields data
                    tag_fields_dict = {}
                    for field_info in field_list:
                        id = str(field_info['id'])
                        label = field_info['label']
                        tag_field_id = label.replace(' ', '_').lower().strip()
                        if id in form_field_values_dict:
                            value = form_field_values_dict[id]
                        else:
                            value = None
                        field = {'displayName': label,
                                 'field_id': tag_field_id,
                                 'value': value}
                        tag_fields_dict[id] = field
                    create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    fields = ('form_id', 'input_form_id', 'creator_id', 'tag_template_local_id', 'field_list', 'create_time')
                    values = (form_id, input_form_id, user_id, tag_tempalte_local_id, json.dumps(tag_fields_dict), create_time)
                    sql = self.create_insert_sql(db_name, 'tagTemplatesValueTable', '({})'.format(', '.join(fields)), values)
                    print('tagTemplatesValueTable create_insert_sql:', sql)
                    _ = self.insert_exec(conn, sql)
                    return 'create successfully.'
                else:
                    return 'get form failed, input_form_data_code:{}, input_form_id:{}, user_id:{};  ' \
                           'form_data_code:{}, form_id:{}, workspace_id:{}'.format(
                        str(input_form_data['code']),
                        str(input_form_id),
                        str(user_id),
                        str(form_data['code']),
                        str(form_id),
                        str(workspace_id))
        except Exception as e:
            lg.error(e)
            import traceback
            # print(traceback.format_exc())
            return response_code.ADD_DATA_FAIL
        finally:
            conn.close()

if __name__ == '__main__':
    x = system_create_tag({"form_name": 'Create from 2',
                           "description": 'Create from 2',
                           "field_list": '[{"default": "", "des": "", "edit": 1, "id": "u1", "label": "Form Name", "options": [], "placeholder": "", "style": 3}, {"default": "", "des": "", "edit": 1, "id": "u2", "label": "Form Description", "options": [], "placeholder": "", "style": 3}, {"default": "", "des": "", "edit": 1, "id": "u3", "label": "fieldList", "options": [], "placeholder": "", "style": 3}]',
                           })
    x.execute()
