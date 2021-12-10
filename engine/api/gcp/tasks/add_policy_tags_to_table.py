from api.gcp.tasks.baseTask import baseTask
from google.cloud import bigquery
# from google.cloud.bigquery import Table
from google.cloud.bigquery.schema import SchemaField
from db.connection_pool import MysqlConn
from config import configuration
from db.base import DbBase
from utils.log_helper import lg
import traceback


class AddPolicyTagsToTable(baseTask, DbBase):
    api_type = 'gcp'

    api_name = 'AddPolicyTagsToTable'
    arguments = {"project_id": {"type": str, "default": ''},
                 "dataset_id": {"type": str, "default": ''},
                 "table_id": {"type": str, "default": ''},
                 "fields": {"type": list, "default": []}}
    role_list = ['roles/datacatalog.categoryAdmin', 'roles/datacatalog.admin', 'roles/bigquery.dataOwner', 'roles/bigquery.admin']

    def __init__(self, stage_dict):
        super(AddPolicyTagsToTable, self).__init__(stage_dict)
        self.full_resource_name = ''

    def execute(self):

        conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            print('self.stage_dict:', self.stage_dict)
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
                project = client.project
                dataset_ref = bigquery.DatasetReference(project, dataset_id)
                table_ref = dataset_ref.table(table_id)
                table = client.get_table(table_ref)  # API request
                print(table.to_api_repr())
                # table_schema = table.schema.copy()
                new_schema = []
                fields = self.stage_dict['fields']
                for index in range(len(fields)):
                    if 'tags' in fields[index]:
                        del fields[index]['tags']
                    for pt_index in range(len(fields[index]['policyTags']['names'])):
                        policy_tag_id = fields[index]['policyTags']['names'][pt_index]
                        condition = "id=%s" % policy_tag_id
                        sql = self.create_select_sql(db_name, 'policyTagsTable', 'gcp_policy_tag_id,', condition=condition)
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

            return 'update successfully'
        except Exception as e:
            import traceback
            lg.error(traceback.format_exc())

        finally:
            conn.close()


if __name__ == '__main__':
    x = AddPolicyTagsToTable({
        "porject_id": 'principal-yen-328302',
        "dataset_name": 'austin_311',
        "table_name": '311_service_request',
        'column_policy_tags_dict': {
            'unique_key': 'projects/principal-yen-328302/locations/us/taxonomies/3180233960818548921/policyTags/4851542792588671512'}
    })
    x.execute()
    # print(x)
