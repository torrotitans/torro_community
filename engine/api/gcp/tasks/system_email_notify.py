from api.gcp.tasks.baseTask import baseTask
from utils.smtp_helper import notify_approvers
from utils.ldap_helper import Ldap
from db.connection_pool import MysqlConn
from config import configuration
import traceback
import logging

logger = logging.getLogger("main." + __name__)

class system_email_notify(baseTask):
    api_type = 'system'
    api_name = 'system_email_notify'
    arguments = {
        "groups": {"type": str, "default": ''},
        "emails": {"type": str, "default": ''},
        'email_msg': {"type": str, "default": ''}}

    def __init__(self, stage_dict):
        super(system_email_notify, self).__init__(stage_dict)
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
                logger.debug("FN:system_email_notify_execute inputFormTable_sql:{}".format(sql))
                input_form_infos = self.execute_fetch_all(conn, sql)
                
                if not input_form_infos:
                    raise Exception('input form not found: {}'.format(str(input_form_id)))
                # get history id
                history_id = input_form_infos[0]['history_id']
                # get requestor email
                # print('self.stage_dict:', self.stage_dict)
                emails = self.stage_dict['emails']
                email_msg = str(self.stage_dict['email_msg'])

                if not isinstance(emails, list):
                    emails = emails.split(',')

                groups = self.stage_dict['groups']
                if not isinstance(groups, list):
                    groups = groups.split(',')

                logger.debug("FN:system_email_notify_execute groups:{}".format(groups))
                for group in groups:
                    mail_list, _ = Ldap.get_ad_group_member(group)
                    logger.debug("FN:system_email_notify_execute mail_list:{}".format(mail_list))
                    
                    if mail_list:
                        emails.extend(mail_list)

                data = notify_approvers(history_id, emails, text=email_msg)

                if data['code'] == 200:
                    return 'create successfully.'
                else:
                    return data['msg']
            except Exception as e:
                logger.error("FN:system_email_notify_execute error:{}".format(traceback.format_exc()))

            finally:
                conn.close()
