from api.gcp.tasks.baseTask import baseTask
import time
from google.cloud import storage
import traceback
import logging
from googleapiclient.errors import HttpError
from utils.status_code import response_code
import json
logger = logging.getLogger("main.api.gcp.tasks" + __name__)

class GrantRoleForGCSBucket(baseTask):
    api_type = 'gcp'
    api_name = 'GrantRoleForGCSBucket'
    arguments = {"project_id": {"type": str, "default": ''},
                 "bucket_name": {"type": str, "default": ''},
                 "member_roles ": {"type": str, "default": ''}}

    def __init__(self, stage_dict):
        super(GrantRoleForGCSBucket, self).__init__(stage_dict)
        self.target_project = stage_dict['project_id']

    def execute(self, workspace_id=None, form_id=None, input_form_id=None, user_id=None):
        # Expected role input:
        # "ad1@abc.com+storage+storage.objectViewer,ad2@abc.com+storage+storage.objectViewer"
        try:
            successful_user = set()
            project_id = self.stage_dict['project_id']
            bucket_name = self.stage_dict['bucket_name']
            member_roles_str = self.stage_dict['member_roles']
            roles_members = {}
            for member_info in member_roles_str.split(','):
                user_name, role = member_info.split('+')
                user_name = user_name.strip()
                if role not in roles_members:
                    roles_members[role] = set()
                roles_members[role].add(user_name)

            logger.debug("FN:GrantRoleForGCSBucket_execute project_id:{} bucket_name:{}".format(project_id,bucket_name))
            storage_client = storage.Client(project_id)
            bucket = storage_client.bucket(bucket_name)

            logger.debug("FN:GrantRoleForGCSBucket_execute roles_members:{}".format(roles_members))

            for role in roles_members:
                members = roles_members[role]
                role = 'roles/' + role
                for member in members:

                        policy = bucket.get_iam_policy(requested_policy_version=3)
                        policy.bindings.append(
                            {
                                "role": role,
                                "members": [member],
                                })

                        logger.debug("FN:GrantRoleForGCSBucket_execute iam_binding_policy:{}".format(policy))
                        bucket.set_iam_policy(policy)
                        successful_user.add('{}+{}'.format(member, role))
                        time.sleep(1)

            return_msg = "Added member(s) successfully:\n{}".format(', '.join(successful_user))
            data = response_code.SUCCESS
            data['data'] = return_msg
            return data
        except HttpError as e:
            error_json = json.loads(e.content, strict=False)
            data = error_json['error']
            data["msg"] = data.pop("message")
            logger.error("FN:GrantRoleForGCSBucket_execute error:{}".format(traceback.format_exc()))
            return data
        except Exception as e:
            logger.error("FN:GrantRoleForGCSBucket_execute error:{}".format(traceback.format_exc()))
            data = response_code.BAD_REQUEST
            data['msg'] = str(e)
            return data
