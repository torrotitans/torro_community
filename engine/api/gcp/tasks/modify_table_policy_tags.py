from api.gcp.tasks.baseTask import baseTask
from google.cloud import bigquery
# from google.cloud.bigquery import Table
from google.cloud.bigquery.schema import SchemaField
from db.connection_pool import MysqlConn
from config import configuration
from db.base import DbBase
import json
import datetime
import traceback
import logging

logger = logging.getLogger("main." + __name__)

class ModifyTablePolicyTags(baseTask, DbBase):
    api_type = 'gcp'

    api_name = 'ModifyTablePolicyTags'
    arguments = {"project_id": {"type": str, "default": ''},
                 "dataset_id": {"type": str, "default": ''},
                 "location": {"type": str, "default": ''},
                 "table_id": {"type": str, "default": ''},
                 "fields": {"type": list, "default": []}}
    role_list = ['roles/datacatalog.categoryAdmin', 'roles/datacatalog.admin', 'roles/bigquery.dataOwner', 'roles/bigquery.admin']

    def __init__(self, stage_dict):
        super(ModifyTablePolicyTags, self).__init__(stage_dict)
        self.full_resource_name = ''
        self.target_project = stage_dict['project_id']

    def execute(self, workspace_id=None, form_id=None, input_form_id=None, user_id=None):

        conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            logger.debug("FN:ModifyTablePolicyTags_execute stage_dict:{}".format(self.stage_dict))
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
                client = bigquery.Client(self.stage_dict['project_id'])
                dataset_id = self.stage_dict['dataset_id']
                table_id = self.stage_dict['table_id']
                location = self.stage_dict.get('location', '')
                project = client.project
                dataset_ref = bigquery.DatasetReference(project, dataset_id)
                table_ref = dataset_ref.table(table_id)
                table = client.get_table(table_ref)  # API request
                logger.debug("FN:ModifyTablePolicyTags_execute table_to_api_repr:{}".format(table.to_api_repr()))
                # table_schema = table.schema.copy()
                new_schema = []
                fields = self.stage_dict['fields']
                for index in range(len(fields)):
                    if 'tags' in fields[index]:
                        del fields[index]['tags']
                    if 'policyTags' in fields[index] and 'names' in fields[index]['policyTags']:
                        policy_tags_length = len(fields[index]['policyTags']['names'])
                        for pt_index in range(policy_tags_length):
                            # for now, every column can just have one policy tags
                            if pt_index != 0:
                                break
                            policy_tag_id = fields[index]['policyTags']['names'][pt_index]
                            condition = "id=%s" % policy_tag_id
                            sql = self.create_select_sql(db_name, 'policyTagsTable', 'gcp_policy_tag_id', condition=condition)
                            gcp_policy_tag_id = self.execute_fetch_one(conn, sql)['gcp_policy_tag_id']
                            fields[index]['policyTags']['names'][pt_index] = gcp_policy_tag_id
                            # if 'policyTags' not in fields[index]['policyTags']['names'][pt_index]:
                            #     fields[index]['policyTags']['names'][
                            #         pt_index] = "projects/geometric-ocean-333410/locations/asia-east2/taxonomies/1346075789958397800/policyTags/8605754121758499097"

                    new_field = SchemaField.from_api_repr(fields[index])
                    new_schema.append(new_field)

                table.schema = new_schema
                table.description = "Updated Policy Tags."

                table = client.update_table(table, ["description", "schema"])  # API request

                assert table.description == "Updated Policy Tags."

                condition = "workspace_id='%s' and project_id='%s' and location='%s' and dataset_id='%s' and table_id='%s'" % \
                            (workspace_id, project, location, dataset_id, table_id)
                sql = self.create_select_sql(db_name, 'dataOnboardTable', '*', condition=condition)
                logger.debug("FN:ModifyTablePolicyTags_execute dataOnboardTable_sql:{}".format(sql))
                data_info = self.execute_fetch_one(conn, sql)
                now = str(datetime.datetime.today())

                if data_info:
                    column_fields = ('workspace_id', 'project_id', 'dataset_id', 'location', 'table_id', 'fields', 'create_time')
                    values = (workspace_id, project, dataset_id, location, table_id, json.dumps(fields), now)
                    sql = self.create_update_sql(db_name, 'dataOnboardTable', column_fields, values, condition)
                    logger.debug("FN:ModifyTablePolicyTags_execute update_dataOnboardTable_sql:{}".format(sql))
                    return_count = self.updete_exec(conn, sql)

                else:
                    column_fields = ('input_form_id', 'workspace_id', 'project_id', 'dataset_id', 'location', 'table_id', 'fields', 'create_time')
                    values = (input_form_id, workspace_id, project, dataset_id, location, table_id, json.dumps(fields), now)
                    sql = self.create_insert_sql(db_name, 'dataOnboardTable', '({})'.format(', '.join(column_fields)), values)
                    logger.debug("FN:ModifyTablePolicyTags_execute insert_dataOnboardTable_sql:{}".format(sql))
                    return_count = self.insert_exec(conn, sql)

            return 'update successfully'

        except Exception as e:
            logger.error("FN:ModifyTablePolicyTags_execute error:{}".format(traceback.format_exc()))

        finally:
            conn.close()

