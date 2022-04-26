from api.gcp.tasks.baseTask import baseTask
from google.cloud import datacatalog_v1beta1
import traceback
import logging
from googleapiclient.errors import HttpError
from utils.status_code import response_code
import json

logger = logging.getLogger("main.api.gcp.tasks" + __name__)

class AddTagTemplateToTable(baseTask):
    api_type = 'gcp'
    api_name = 'AddTagTemplateToTable'
    arguments = {"source_project_id": {"type": str, "default": ''},
                 "table_project_id": {"type": str, "default": ''},
                 "location": {"type": str, "default": ''},
                 "tag_template_id": {"type": str, "default": ''},
                 "dataset_id ": {"type": str, "default": ''},
                 "table_id": {"type": str, "default": ''},
                 "tag_template_dict": {"type": dict, "default": {}}}
    role_list = ['roles/datacatalog.tagTemplateCreator', 'roles/datacatalog.admin']

    def __init__(self, stage_dict):
        super(AddTagTemplateToTable, self).__init__(stage_dict)
        self.full_resource_name = None
        self.target_project = stage_dict['source_project_id']

    def execute(self, workspace_id=None, form_id=None, input_form_id=None, user_id=None):
        try:
        
            missing_set = set()
            for key in self.arguments:
                # if key == 'bucket_cmek' or key == 'bucket_class' or key == 'bucket_labels':
                #     continue
                check_key = self.stage_dict.get(key, 'NotFound')
                if check_key == 'NotFound':
                    missing_set.add(key)
                # # print('{}: {}'.format(key, self.stage_dict[key]))
            if len(missing_set) != 0:
                data = response_code.BAD_REQUEST
                data['msg'] = 'Missing parameters: {}'.format(', '.join(missing_set))
                return data
            else:
                source_project_id = self.stage_dict['source_project_id']
                table_project_id = self.stage_dict['table_project_id']
                location = self.stage_dict['location']
                tag_template_id = self.stage_dict['tag_template_id']
                dataset_id = self.stage_dict['dataset_id']
                table_id = self.stage_dict['table_id']
                tag_template_dict = self.stage_dict['tag_template_dict']

                datacatalog_client = datacatalog_v1beta1.DataCatalogClient()
                tag_template = datacatalog_client.get_tag_template(
                    name=f"projects/{source_project_id}/locations/{location}/tagTemplates/{tag_template_id}",
                )

                logger.debug("FN:AddTagTemplateToTable_execute tag_template:{}".format(tag_template))
                # Lookup Data Catalog's Entry referring to the table.
                resource_name = (
                    f"//bigquery.googleapis.com/projects/{table_project_id}"
                    f"/datasets/{dataset_id}/tables/{table_id}"
                )

                logger.debug("FN:AddTagTemplateToTable_execute resource_name:{}".format(resource_name))

                table_entry = datacatalog_client.lookup_entry(
                    request={"linked_resource": resource_name}
                )

                logger.debug("FN:AddTagTemplateToTable_execute table_entry:{}".format(table_entry))

                # Attach a Tag to the table.
                tag = datacatalog_v1beta1.types.Tag()

                tag.template = tag_template.name
                tag.name = tag_template_dict['displayName']
                '''
                {
                "displayName": "Data Governance",
                "fields": {
                    "data_governor": { "type": "string", "value": "12345"},
                    "encrypted_data_asset": { "type": "bool", "value": True},
                    "approved_by_governance_date": { "type": "timestamp", "value": "2021-10-24 00:00:00"},
                    "data_classfication": { "type": "enum", "value": "Public"},
                    }  
                }
                
                '''

                logger.debug("FN:AddTagTemplateToTable_execute tag_template_dict_fields:{}".format(tag_template_dict['fields']))
                
                for field_name in tag_template_dict['fields']:
                    field = datacatalog_v1beta1.types.TagField()
                    if tag_template_dict['fields'][field_name]['type'] == 'string':
                        field.string_value = tag_template_dict['fields'][field_name]['value']
                    elif tag_template_dict['fields'][field_name]['type'] == 'bool':
                        field.bool_value = tag_template_dict['fields'][field_name]['value']
                    elif tag_template_dict['fields'][field_name]['type'] == 'double':
                        field.double_value = tag_template_dict['fields'][field_name]['value']
                    elif tag_template_dict['fields'][field_name]['type'] == 'timestamp':
                        field.timestamp_value = tag_template_dict['fields'][field_name]['value']
                    elif tag_template_dict['fields'][field_name]['type'] == 'enum':
                        field.enum_value.display_name = tag_template_dict['fields'][field_name]['value']
                    tag.fields[field_name] = field
                    # tag.fields["num_rows"] = datacatalog_v1beta1.types.TagField()
                    # tag.fields["num_rows"].double_value = 113496874
                    #
                    # tag.fields["has_pii"] = datacatalog_v1beta1.types.TagField()
                    # tag.fields["has_pii"].bool_value = False
                    #
                    # tag.fields["pii_type"] = datacatalog_v1beta1.types.TagField()
                    # tag.fields["pii_type"].enum_value.display_name = "NONE"

                logger.debug("FN:AddTagTemplateToTable_execute tag:{}".format(tag))
                tag = datacatalog_client.create_tag(parent=table_entry.name, tag=tag)
                data = response_code.SUCCESS
                data['data'] = 'Create successfully'
                return data
        except HttpError as e:
            error_json = json.loads(e.content, strict=False)
            data = error_json['error']
            data["msg"] = data.pop("message")
            logger.error("FN:AddTagTemplateToTable error:{}".format(traceback.format_exc()))
            return data
        except Exception as e:
            logger.error("FN:AddTagTemplateToTable error:{}".format(traceback.format_exc()))
            data = response_code.BAD_REQUEST
            data['msg'] = str(e)
            return data


        
if __name__ == '__main__':

    # print()
    pass