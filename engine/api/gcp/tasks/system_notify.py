from api.gcp.tasks.baseTask import baseTask
from utils.smtp_helper import notify_approvers
from db.base import DbBase
from utils.log_helper import lg
from db.connection_pool import MysqlConn
from config import configuration
import json
import datetime
class system_notify(baseTask, DbBase):
    api_type = 'system'
    api_name = 'system_notify'
    arguments = {
        "groups": {"type": str, "default": ''},
        "emails": {"type": str, "default": ''},
        'notify_msg': {"type": str, "default": ''}}

    def __init__(self, stage_dict):
        super(system_notify, self).__init__(stage_dict)
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
            conn = MysqlConn()
            try:
                db_name = configuration.get_database_name()
                # get history id
                table_name = 'inputFormTable'
                condition = "id='%s' order by history_id desc" % (input_form_id)
                fields = '*'
                sql = self.create_select_sql(db_name, table_name, fields, condition)
                input_form_infos = self.execute_fetch_all(conn, sql)
                if not input_form_infos:
                    raise Exception('input form not found: {}'.format(str(input_form_id)))
                # get history id
                history_id = input_form_infos[0]['history_id']
                # get requestor email
                # print('self.stage_dict:', self.stage_dict)
                emails = self.stage_dict['emails']
                notify_msg = str(self.stage_dict['notify_msg'])
                if not isinstance(emails, list):
                    emails = emails.split(',')
                groups = self.stage_dict['groups']
                create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if not isinstance(emails, list):
                    groups = groups.split(',')
                values = (user_id, input_form_id, history_id, json.dumps(groups), json.dumps(emails), notify_msg, 0, create_time)
                fields = ('user_id', 'input_form_id', 'history_id', 'adgroup_mail_list', 'user_mail_list', 'comment', 'is_read', 'create_time')
                sql = self.create_insert_sql(db_name, 'inputNotifyTable', '({})'.format(', '.join(fields)), values)
                notify_id = self.insert_exec(conn, sql, return_insert_id=True)
                return 'create notify successfully: id{}'.format(str(notify_id))
            except Exception as e:
                import traceback
                lg.error(traceback.format_exc())
            finally:
                conn.close()
if __name__ == '__main__':
    pass

