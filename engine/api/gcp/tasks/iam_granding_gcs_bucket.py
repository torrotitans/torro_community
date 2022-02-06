from api.gcp.tasks.baseTask import baseTask
import time
from google.cloud import storage

class GrantRoleForGCSBucket(baseTask):
    api_type = 'gcp'
    api_name = 'GrantRoleForGCSBucket'
    arguments = {"porject_id": {"type": str, "default": ''},
                 "bucket_name": {"type": str, "default": ''},
                 "member_roles ": {"type": dict, "default": {}}}

    def __init__(self, stage_dict):
        super(GrantRoleForGCSBucket, self).__init__(stage_dict)
        self.target_project = stage_dict['project_id']

    def execute(self):
        missing_set = set()
        for key in self.arguments:
            if key == 'bucket_cmek' or key == 'bucket_class' or key == 'bucket_labels':
                continue
            check_key = self.stage_dict.get(key, 'NotFound')
            if check_key == 'NotFound':
                missing_set.add(key)
        if len(missing_set) != 0:
            return 'Missing parameters: {}'.format(', '.join(missing_set))
        else:
            successful_user = set()
            error_user = set()
            project_id = self.stage_dict['porject_id']
            bucket_name = self.stage_dict['bucket_name']
            member_roles_str = self.stage_dict['member_roles']
            roles_members = {}
            for member_info in member_roles_str.split(','):
                user_name, role = member_info.split('+')
                user_name = user_name.strip()
                if role not in roles_members:
                    roles_members[role] = set()
                roles_members[role].add(user_name)

            storage_client = storage.Client(project_id)

            bucket = storage_client.bucket(bucket_name)

            for role in roles_members:
                members = roles_members[role]
                role = 'roles/' + role
                for member in members:
                    try:
                        policy = bucket.get_iam_policy(requested_policy_version=3)

                        policy.bindings.append(
                            {
                                "role": role,
                                "members": [member],
                                })
                        bucket.set_iam_policy(policy)
                        successful_user.add('{}+{}'.format(member, role))
                        time.sleep(1)
                    except Exception as e:
                        e = str(e)
                        error_user.add('{}+{}'.format(member, role))


            return_msg = "Added member(s) successfully:\n{}".format(', '.join(successful_user))
            return_msg += '\nAdded member(s) failed:\n{}'.format(', '.join(error_user))
            return(return_msg)
