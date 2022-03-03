# Import required modules.
from google.cloud import datacatalog_v1
from api.gcp.tasks.baseTask import baseTask
import json
from db.connection_pool import MysqlConn
from config import configuration
from db.base import DbBase
import datetime
from common.common_input_form_status import status
import traceback
import logging

logger = logging.getLogger("main." + __name__)

class ModifyTableTags(baseTask, DbBase):
    api_type = 'gcp'

    api_name = 'ModifyTableTags'
    arguments = {"project_id": {"type": str, "default": ''},
                 "dataset_id": {"type": str, "default": ''},
                 "location": {"type": str, "default": ''},
                 "table_id": {"type": str, "default": ''},
                 "fields": {"type": list, "default": []},
                 "table_tags": {"type": list, "default": []}
                 }
    role_list = ['roles/datacatalog.categoryAdmin', 'roles/datacatalog.admin', 'roles/bigquery.dataOwner', 'roles/bigquery.admin']

    def __init__(self, stage_dict):
        super(ModifyTableTags, self).__init__(stage_dict)
        self.full_resource_name = ''
        self.target_project = stage_dict['project_id']

    def execute(self, workspace_id=None, form_id=None, input_form_id=None, user_id=None):

        conn = MysqlConn()
        
        try:
            db_name = configuration.get_database_name()
            logger.debug("FN:ModifyTableTags_execute stage_dict:{}".format(self.stage_dict))
            missing_set = set()
            for key in self.arguments:
                # if key == 'bucket_cmek' or key == 'bucket_class' or key == 'bucket_labels':
                #     continue
                check_key = self.stage_dict.get(key, 'NotFound')
                # print(check_key, key)
                if check_key == 'NotFound':
                    missing_set.add(key)
                # # print('{}: {}'.format(key, self.stage_dict[key]))
            if len(missing_set) != 0:
                return 'Missing parameters: {}'.format(', '.join(missing_set))
            else:
                datacatalog_client = datacatalog_v1.DataCatalogClient()
                dataset_id = self.stage_dict['dataset_id']
                location = self.stage_dict.get('location', '')
                table_id = self.stage_dict['table_id']
                project_id = self.stage_dict['project_id']
                table_tags = self.stage_dict.get('table_tags', [])
                fields = self.stage_dict.get('fields', [])
                # get data owner
                tag_template_form_id = None
                ad_group = ''
                for table_tag in table_tags:
                    if 'tag_template_form_id' in table_tag and 'data' in table_tag:
                        tag_template_form_id = table_tag['tag_template_form_id']
                    if tag_template_form_id == status.system_form_id['data_approval_tag_template']:
                        for key in table_tag['data']:
                            ad_group = table_tag['data'][key]

                # Lookup Data Catalog's Entry referring to the table.
                resource_name = (
                    f"//bigquery.googleapis.com/projects/{project_id}"
                    f"/datasets/{dataset_id}/tables/{table_id}"
                )
                table_entry = datacatalog_client.lookup_entry(
                    request={"linked_resource": resource_name}
                )
                # clear the table tags
                self.__clear_tags(datacatalog_client, table_entry)
                # tags
                for table_tag in table_tags:
                    tag_template_form_id = table_tag['tag_template_form_id']
                    data = table_tag['data']
                    table_tag = self.__get_tags(data, tag_template_form_id, db_name, conn)

                    table_tag = datacatalog_client.create_tag(parent=table_entry.name, tag=table_tag)
                    logger.debug("FN:ModifyTableTags_execute table_tag_name:{}".format(table_tag.name))

                for field in fields:
                    if 'tags' in  field:
                        column_name = field['name']
                        for field_tag in field['tags']:
                            tag_template_form_id = field_tag['tag_template_form_id']
                            data = field_tag['data']
                            column_tag = self.__get_tags(data, tag_template_form_id, db_name, conn, column=column_name)
                            column_tag = datacatalog_client.create_tag(parent=table_entry.name, tag=column_tag)

                condition = "workspace_id='%s' and project_id='%s' and location='%s' and dataset_id='%s' and table_id='%s'" % (workspace_id, project_id, location, dataset_id, table_id)
                sql = self.create_select_sql(db_name, 'dataOnboardTable', '*', condition=condition)
                logger.debug("FN:ModifyTableTags_execute dataOnboardTable_sql:{}".format(sql))
                data_info = self.execute_fetch_one(conn, sql)
                now = str(datetime.datetime.today())

                if data_info:
                    column_fields = ('workspace_id', 'data_owner', 'project_id', 'location', 'dataset_id', 'table_id', 'fields', 'table_tags', 'create_time')
                    values = (workspace_id, ad_group, project_id, location, dataset_id, table_id, json.dumps(fields), json.dumps(table_tags), now)
                    sql = self.create_update_sql(db_name, 'dataOnboardTable', column_fields, values, condition)
                    logger.debug("FN:ModifyTableTags_execute update_dataOnboardTable_sql:{}".format(sql))
                    return_count = self.updete_exec(conn, sql)

                else:
                    column_fields = ('input_form_id', 'workspace_id', 'data_owner', 'project_id', 'location', 'dataset_id', 'table_id', 'fields', 'table_tags', 'create_time')
                    values = (input_form_id, workspace_id, ad_group, project_id, location, dataset_id, table_id, json.dumps(fields), json.dumps(table_tags), now)
                    sql = self.create_insert_sql(db_name, 'dataOnboardTable', '({})'.format(', '.join(column_fields)), values)
                    logger.debug("FN:ModifyTableTags_execute insert_dataOnboardTable_sql:{}".format(sql))
                    return_count = self.insert_exec(conn, sql)

            return 'update successfully'

        except Exception as e:
            logger.error("FN:ModifyTableTags_execute error:{}".format(traceback.format_exc()))

        finally:
            conn.close()
    def __clear_tags(self, datacatalog_client, table_entry):

        tags = datacatalog_client.list_tags(parent=table_entry.name)
        for tag in tags:
            # print(type(tag), tag.name)
            datacatalog_client.delete_tag({'name': tag.name})

    def __get_tags(self, data, form_id, db_name, conn, column=None):
        # get tag template info
        condition = "tag_template_form_id=%s" % form_id
        sql = self.create_select_sql(db_name, 'tagTemplatesTable',
                                     'display_name,project_id,location,tag_template_id,field_list', condition=condition)
        tag_template_info = self.execute_fetch_one(conn, sql)
        tag_template_name = 'projects/{}/locations/{}/tagTemplates/{}'.format(tag_template_info['project_id'],
                                                                              tag_template_info['location'],
                                                                              tag_template_info['tag_template_id'])
        tag_template_field_list = json.loads(tag_template_info['field_list'])
        display_name = tag_template_info['display_name']
        # get form info
        condition = "id=%s" % form_id
        sql = self.create_select_sql(db_name, 'formTable',
                                     'fields_list', condition=condition)
        form_info = self.execute_fetch_one(conn, sql)
        if not form_info:
            return None
        form_field_list = json.loads(form_info['fields_list'])
        # Attach a Tag to the table.
        tag = datacatalog_v1.types.Tag()

        tag.template = tag_template_name
        tag.name = display_name
        if column:
            tag.column = column
        for field in form_field_list:
            label = field['label']
            field_id = label.replace(' ', '_').lower().strip()
            style = field['style']
            id = field['id']
            value = ''
            if id in data:
                value = data[id]
            tag.fields[field_id] = datacatalog_v1.types.TagField()

            if style == 5:
                tag.fields[field_id].bool_value = bool(value)
            elif style == 2:
                tag.fields[field_id].enum_value.display_name = value
            elif style == 1 or style == 3:
                tag.fields[field_id].string_value = value
            elif style == 6:
                tag.fields[field_id].timestamp_value = value
            else:
                continue
        return tag
