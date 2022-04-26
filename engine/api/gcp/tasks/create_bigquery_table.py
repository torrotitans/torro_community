from api.gcp.tasks.baseTask import baseTask
from google.cloud import bigquery
import csv
import logging
from googleapiclient.errors import HttpError
from utils.status_code import response_code
import traceback
import json

logger = logging.getLogger("main.api.gcp.tasks" + __name__)


class CreateBQTable(baseTask):
    api_type = 'gcp'
    api_name = 'CreateBQTable'
    arguments = {"porject_id": {"type": str, "default": ''},
                 "usecase_name": {"type": str, "default": ''},
                 "dataset_name": {"type": str, "default": ''},
                 "table_name": {"type": str, "default": ''},
                 "table_labels": {"type": str, "default": ''},
                 "table_schema_csv": {"type": str, "default": ''}}

    def __init__(self, stage_dict):
        super(CreateBQTable, self).__init__(stage_dict)
        self.target_project = stage_dict['porject_id']

    def execute(self, workspace_id=None, form_id=None, input_form_id=None, user_id=None):
        try:
            missing_set = set()
            for key in self.arguments:
                if key == 'table_labels':
                    continue
                check_key = self.stage_dict.get(key, 'NotFound')
                if check_key == 'NotFound':
                    missing_set.add(key)
                # # print('{}: {}'.format(key, self.stage_dict[key]))
            if len(missing_set) != 0:
                data = response_code.BAD_REQUEST
                data['msg'] = 'Missing parameters: {}'.format(', '.join(missing_set))
                return data
            else:
                project_id = self.stage_dict['porject_id'].strip()
                dataset_name = self.stage_dict['dataset_name'].strip()
                table_name = self.stage_dict['table_name'].strip()
                table_id = '{}.{}.{}'.format(project_id, dataset_name, table_name)
                try:
                    table_schema_csv_path = json.loads(self.stage_dict['table_schema_csv'].replace('\\', '\\\\'), strict=False)
                except:
                    table_schema_csv_path = self.stage_dict['table_schema_csv']
                if isinstance(table_schema_csv_path, list):
                    table_schema_csv_path = table_schema_csv_path[0]
                table_labels_str = self.stage_dict.get('table_labels', '')
                table_labels = {}
                for table_label in table_labels_str.split(','):
                    key, value = table_label.split('=')
                    table_labels[key.strip()] = value.strip().replace(' ', '').lower()
                print('table_id:', table_id)
                print('label:', table_labels)
                schema = []

                # bucket_name = table_schema_csv_path.split('/')[0].replace('gs://', '')
                # object_name = table_schema_csv_path.split('/')[-1]
                # blob_name = table_schema_csv_path.replace('gs://'+bucket_name+'/', '')
                # temp_file_name = 'temp/'+table_schema_csv_path.replace('gs://', '')
                # temp_path = temp_file_name.replace(object_name, '')
                # print('create table path:', bucket_name, object_name, blob_name)
                # print('temp path:', temp_file_name, temp_path)
                # if not os.path.exists(temp_path):
                #     os.makedirs(temp_path)
                # bucket_object_helper.download_blob(bucket_name, blob_name, temp_file_name)
                fr = open(table_schema_csv_path, 'r')
                f = csv.reader(fr)
                for index, line in enumerate(f):
                    if index == 0:
                        continue
                    column_schema = bigquery.SchemaField(line[0].strip(), line[1].strip(), mode=line[2].strip())
                    schema.append(column_schema)
                fr.close()
                # os.system('rm -rf {}'.format(temp_path))
                print('schema:', schema)
                # exit(0)
                # create table
                table = bigquery.Table(table_id, schema=schema)
                client = bigquery.Client()
                table = client.create_table(table)


                if table_labels:
                    table.labels = table_labels
                    table = client.update_table(table, ["labels"])  # API request

                usecase_name = self.stage_dict.get('usecase_name', None)
                self.records_resource(workspace_id, input_form_id, usecase_name, 'BigQuery Table', table_name)

                data = response_code.SUCCESS
                data['data'] = "Created table {}.{}.{}".format(table.project, table.dataset_id, table.table_id)
                return data
        except HttpError as e:
            error_json = json.loads(e.content.replace('\\', '\\\\'), strict=False)
            data = error_json['error']
            data["msg"] = data.pop("message")
            logger.error("FN:CreateBQTable_execute error:{}".format(traceback.format_exc()))
            return data
        except Exception as e:
            logger.error("FN:CreateBQTable_execute error:{}".format(traceback.format_exc()))
            data = response_code.BAD_REQUEST
            data['msg'] = str(e)
            return data