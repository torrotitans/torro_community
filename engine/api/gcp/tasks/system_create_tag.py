from api.gcp.tasks.baseTask import baseTask
import json
import datetime
from core.input_form_singleton import input_form_singleton
from core.form_singleton import formSingleton_singleton
from db.connection_pool import MysqlConn
from utils.status_code import response_code
from config import configuration
import traceback
import logging
from googleapiclient.errors import HttpError
from utils.status_code import response_code
logger = logging.getLogger("main." + __name__)

class system_create_tag(baseTask):
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
                data = response_code.BAD_REQUEST
                data['msg'] = 'Missing parameters: {}'.format(', '.join(missing_set))
                return data
            else:
                # get tag template id
                sql = self.create_select_sql(db_name, 'tagTemplatesTable', 'id,tag_template_form_id', condition="tag_template_form_id='%s' order by id desc" % form_id)
                logger.debug("FN:system_create_tag_execute tagTemplatesTable_sql:{}".format(sql))
                tag_template_info = self.execute_fetch_all(conn, sql)
                tag_tempalte_local_id = tag_template_info[0]['id']
                input_form_data = input_form_singleton.get_input_form_data(user_id, input_form_id)
                form_data = formSingleton_singleton.get_details_form_by_id(form_id, workspace_id)
                logger.debug("FN:system_create_tag_execute input_form_data:{} form_data:{}".format(input_form_data, form_data))
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
                    logger.debug("FN:system_create_tag_execute insert_tagTemplatesValueTable_sql:{}".format(sql))
                    _ = self.insert_exec(conn, sql)
                    data = response_code.SUCCESS
                    data['data'] = 'create successfully.'
                    return data
                else:
                    data = response_code.BAD_REQUEST
                    data['msg'] = 'get form failed, input_form_data_code:{}, input_form_id:{}, user_id:{};  ' \
                           'form_data_code:{}, form_id:{}, workspace_id:{}'.format(
                        str(input_form_data['code']),
                        str(input_form_id),
                        str(user_id),
                        str(form_data['code']),
                        str(form_id),
                        str(workspace_id))

                    return data
        except HttpError as e:
            error_json = json.loads(e.content)
            data = error_json['error']
            data["msg"] = data.pop("message")
            logger.error("FN:system_create_tag_execute error:{}".format(traceback.format_exc()))
            return data
        except Exception as e:
            logger.error("FN:system_create_tag_execute error:{}".format(traceback.format_exc()))
            data = response_code.BAD_REQUEST
            data['msg'] = str(e)
            return data

        finally:
            conn.close()
