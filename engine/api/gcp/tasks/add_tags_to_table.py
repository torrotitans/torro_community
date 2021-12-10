# Import required modules.
from google.cloud import datacatalog_v1
from api.gcp.tasks.baseTask import baseTask
import json
from db.connection_pool import MysqlConn
from config import configuration
from db.base import DbBase
from utils.log_helper import lg
import traceback


class AddTagsToTable(baseTask, DbBase):
    api_type = 'gcp'

    api_name = 'AddTagsToTable'
    arguments = {"project_id": {"type": str, "default": ''},
                 "dataset_id": {"type": str, "default": ''},
                 "table_id": {"type": str, "default": ''},
                 "fields": {"type": list, "default": []},
                 "table_tags": {"type": dict, "default": {}}
                 }
    role_list = ['roles/datacatalog.categoryAdmin', 'roles/datacatalog.admin', 'roles/bigquery.dataOwner', 'roles/bigquery.admin']

    def __init__(self, stage_dict):
        super(AddTagsToTable, self).__init__(stage_dict)
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
                datacatalog_client = datacatalog_v1.DataCatalogClient()
                dataset_id = self.stage_dict['dataset_id']
                table_id = self.stage_dict['table_id']
                project_id = self.stage_dict['project_id']
                table_tags = self.stage_dict['table_tags']
                fields = self.stage_dict['fields']
                # Lookup Data Catalog's Entry referring to the table.
                resource_name = (
                    f"//bigquery.googleapis.com/projects/{project_id}"
                    f"/datasets/{dataset_id}/tables/{table_id}"
                )
                table_entry = datacatalog_client.lookup_entry(
                    request={"linked_resource": resource_name}
                )
                if table_tags:
                    tag_template_form_id = table_tags['tag_template_form_id']
                    data = table_tags['data']
                    table_tag = self.__get_tags(data, tag_template_form_id, db_name, conn)

                    table_tag = datacatalog_client.create_tag(parent=table_entry.name, tag=table_tag)
                    print(f"Created tag: {table_tag.name}")
                # if fields:
                #     for field in fields:
                #         if 'tags' in  field:
                #             for field_tag in field['tags']:
                #                 tag_template_form_id = field_tag['tag_template_form_id']
                #                 data = field_tag['data']
                #                 table_tag = self.__get_tags(data, tag_template_form_id, db_name, conn)


            return 'update successfully'
        except Exception as e:
            import traceback
            lg.error(traceback.format_exc())

        finally:
            conn.close()

    def __get_tags(self, data, form_id, db_name, conn):
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
        form_field_list = form_info['fields_list']
        # Attach a Tag to the table.
        tag = datacatalog_v1.types.Tag()

        tag.template = tag_template_name
        tag.name = display_name

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
                tag.fields["source"].timestamp_value = value
            else:
                continue
        return tag

if __name__ == '__main__':
    x = AddTagsToTable({
        "porject_id": 'principal-yen-328302',
        "dataset_name": 'austin_311',
        "table_name": '311_service_request',
        'column_policy_tags_dict': {
            'unique_key': 'projects/principal-yen-328302/locations/us/taxonomies/3180233960818548921/policyTags/4851542792588671512'}
    })
    x.execute()
    # print(x)
