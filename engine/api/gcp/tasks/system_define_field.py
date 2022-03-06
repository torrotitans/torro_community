from api.gcp.tasks.baseTask import baseTask
from db.base import DbBase
from db.connection_pool import MysqlConn
from config import configuration
import datetime

class system_define_field(baseTask, DbBase):
    api_type = 'system'
    api_name = 'system_define_field'
    arguments = {
        "FieldLabel": {"type": str, "default": ''},
        "optionLabel": {"type": str, "default": ''},
        "optionsValue": {"type": str, "default": ''},
                 }

    def __init__(self, stage_dict):
        super(system_define_field, self).__init__(stage_dict)
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
            field_name = self.stage_dict['FieldLabel']
            option_label = self.stage_dict['optionLabel']
            options_value = self.stage_dict['optionsValue']
            now = str(datetime.datetime.today())
            # print('stage_dict:', self.stage_dict)
            # print('workspace_id:', workspace_id)
            conn = MysqlConn()
            db_name = configuration.get_database_name()
            condition = "label='%s' and form_id!='-1'" % (field_name)
            sql = self.create_select_sql(db_name, 'dynamicFieldTable', 'id', condition)
            dynamic_field_info = self.execute_fetch_one(conn, sql)
            # print('dynamicFieldTable1:',sql)
            if not dynamic_field_info:

                field_fields = ('style', 'form_id', 'label', 'default_value', 'placeholder',
                                   'value_num', 'create_time')
                values = ('2', form_id, field_name, '', '', 1, now)
                sql = self.create_insert_sql(db_name, 'dynamicFieldTable', '({})'.format(', '.join(field_fields)), values)
                # print('dynamicFieldTable2 sql:', sql)
                dynamic_field_id = self.insert_exec(conn, sql, return_insert_id=True)
            else:
                dynamic_field_id = dynamic_field_info['id']
                condition = "workspace_id='%s' and dynamic_field_id=%s and option_label='%s'" % (workspace_id, dynamic_field_id, option_label)
                sql = self.create_select_sql(db_name, 'dynamicFieldValueTable', 'id', condition)
                dynamic_field_value_info = self.execute_fetch_one(conn, sql)
                if dynamic_field_value_info:
                    return 'Label:{} has already in Field:{}'.format(option_label, field_name)

            field_fields = ('workspace_id', 'dynamic_field_id', 'input_form_id', 'option_label', 'option_value', 'create_time')
            values = (workspace_id, dynamic_field_id, input_form_id, option_label, options_value, now)
            sql = self.create_insert_sql(db_name, 'dynamicFieldValueTable', '({})'.format(', '.join(field_fields)),
                                         values)
            # print('dynamicFieldValueTable2 sql:', sql)
            self.insert_exec(conn, sql, return_insert_id=True)
            return "Created field: {}".format(field_name)