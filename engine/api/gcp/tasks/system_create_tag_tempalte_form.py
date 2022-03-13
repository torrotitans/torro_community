from api.gcp.tasks.baseTask import baseTask

import json
from core.form_singleton import formSingleton_singleton
from core.workflow_singleton import workflowSingleton_singleton
from db.connection_pool import MysqlConn
from config import configuration
import traceback
import logging

logger = logging.getLogger("main." + __name__)

class system_create_tag_template_form(baseTask):
    api_type = 'system'
    api_name = 'system_create_tag_template_form'
    arguments = {
        "form_name": {"type": str, "default": ''},
        'description': {"type": str, "default": ''},
        "field_list": {"type": list, "default": []},
                 }

    def __init__(self, stage_dict):
        super(system_create_tag_template_form, self).__init__(stage_dict)
        logger.debug("FN:system_create_tag_template_form_init stage_dict:{}".format(stage_dict))
        
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
                logger.debug("FN:system_create_tag_template_form_execute tags_table_data:{}".format(data))
                if data['code'] == 200:
                    # workflow = {}
                    # workflowSingleton_singleton.add_new_workflow(workflow)
                    tag_tempalte_form_id = data['data']['id']
                    fields = ('tag_template_form_id',)
                    values = (tag_tempalte_form_id,)
                    condition = "(workspace_id='%s' or workspace_id=0) and input_form_id='%s' and creator_id='%s'" % (workspace_id, input_form_id, user_id)
                    sql = self.create_update_sql(db_name, 'tagTemplatesTable', fields, values, condition=condition)
                    logger.debug("FN:system_create_tag_template_form_execute update_tagTemplatesTable_sql:{}".format(sql))
                    return_count = self.updete_exec(conn, sql)
                    logger.debug("FN:system_create_tag_template_form_execute return_count:{}".format(return_count))
                    return 'create successfully.'
                else:
                    return data['msg']

        except Exception as e:
            logger.error("FN:system_create_tag_template_form_execute error:{}".format(traceback.format_exc()))

        finally:
            conn.close()
