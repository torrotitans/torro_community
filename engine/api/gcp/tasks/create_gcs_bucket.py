from api.gcp.tasks.baseTask import baseTask
from google.cloud import storage
import traceback
import logging
from googleapiclient.errors import HttpError
from utils.status_code import response_code
import json
logger = logging.getLogger("main.api.gcp.tasks" + __name__)

class CreateGCSBucket(baseTask):
    api_type = 'gcp'
    api_name = 'CreateGCSBucket'

    def __init__(self, stage_dict):
        super(CreateGCSBucket, self).__init__(stage_dict)
        self.target_project = stage_dict['porject_id']

    def execute(self, workspace_id=None, form_id=None, input_form_id=None, user_id=None):

        try:
            project_id = self.stage_dict['porject_id'].strip()
            bucket_name = self.stage_dict['bucket_name'].strip().replace(' ', '').replace('_', '-').lower()
            location = self.stage_dict['bucket_location'].strip()
            bucket_labels_str = self.stage_dict.get('bucket_labels', '').strip()
            bucket_labels = {}
            if bucket_labels_str:
                for bucket_label in bucket_labels_str.split(','):
                    key, value = bucket_label.split('=')
                    bucket_labels[key.strip()] = value.strip()

            bucket_class = self.stage_dict.get('bucket_class', None).strip()
            bucket_cmek = self.stage_dict.get('bucket_cmek', None).strip()
            logger.debug("FN:CreateGCSBucket_execute bucket_class:{} bucket_cmek:{}".format(bucket_class, bucket_cmek))
            logger.debug("FN:CreateGCSBucket_execute bucket_name:{} location:{}".format(bucket_name, location))
            storage_client = storage.Client(project_id)
            bucket = storage_client.create_bucket(bucket_name, location=location)

            if bucket_class:
                bucket.storage_class = bucket_class
            if bucket_labels:
                labels = bucket.labels
                for label in bucket_labels:
                    labels[label] = bucket_labels[label]
                bucket.labels = labels
            if bucket_cmek:
                bucket.default_kms_key_name = bucket_cmek

            bucket.patch()
            usecase_name = self.stage_dict.get('usecase_name', None)
            self.records_resource(workspace_id, input_form_id, usecase_name, 'Storage', bucket_name)

            data = response_code.SUCCESS
            data['data'] = "Bucket {} created.".format(bucket.name)
            return data
        except HttpError as e:
            error_json = json.loads(e.content)
            data = error_json['error']
            data["msg"] = data.pop("message")
            logger.error("FN:CreateGCSBucket_execute error:{}".format(traceback.format_exc()))
            return data
        except Exception as e:
            logger.error("FN:CreateGCSBucket_execute error:{}".format(traceback.format_exc()))
            data = response_code.BAD_REQUEST
            data['msg'] = str(e)
            return data


            
