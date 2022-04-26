from api.gcp.tasks.baseTask import baseTask
from google.cloud import datacatalog_v1beta1
from db.connection_pool import MysqlConn
import datetime
from config import configuration
import traceback
import logging
from googleapiclient.errors import HttpError
from utils.status_code import response_code
import json
logger = logging.getLogger("main." + __name__)


class CreatePolicyTagsV1(baseTask):
    api_type = 'gcp'
    api_name = 'CreatePolicyTagsV1'
    arguments = {"porject_id": {"type": str, "default": ''},
                 "policy_location": {"type": str, "default": ''},
                 "taxonomy_display_name": {"type": str, "default": ''},
                 "taxonomy_ad_group": {"type": str, "default": ''},
                 "description": {"type": str, "default": ''},
                 "activated_policy_types": {"type": str, "default": [1]},
                 "policy_tags_list": {"type": list, "default": []}}
    role_list = ['roles/datacatalog.categoryAdmin', 'roles/datacatalog.admin']

    def __init__(self, stage_dict):
        super(CreatePolicyTagsV1, self).__init__(stage_dict)
        print('self.stage_dict:', self.stage_dict)

        self.full_resource_name = None
        self.target_project = stage_dict['porject_id']

    def execute(self, workspace_id=None, form_id=None, input_form_id=None, user_id=None):

        conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()

            missing_set = set()
            for key in self.arguments:
                if key == 'description' or key == 'activated_policy_types':
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
                project_id = self.stage_dict['porject_id']
                location = self.stage_dict['policy_location']
                taxonomy_display_name = self.stage_dict['taxonomy_display_name']
                taxonomy_ad_group = self.stage_dict['taxonomy_ad_group']
                description = self.stage_dict.get('description', self.arguments['description']['default'])

                client = datacatalog_v1beta1.PolicyTagManagerClient()
                logger.info('FN:CreatePolicyTagsV1_execute data_catalog_client:{}'.format(client))
                activated_policy_types = self.stage_dict.get('activated_policy_types',
                                                             self.arguments['activated_policy_types']['default'])
                parent = f"projects/{project_id}/locations/{location}"
                taxonomy_list = client.list_taxonomies(parent=parent)
                chosen_taxonomy = None
                for taxonomy in taxonomy_list:
                    if taxonomy.display_name == taxonomy_display_name:
                        chosen_taxonomy = taxonomy
                        break
                if chosen_taxonomy is None:
                    chosen_taxonomy = client.create_taxonomy(
                        parent=parent,
                        taxonomy=datacatalog_v1beta1.Taxonomy(
                            display_name=taxonomy_display_name,
                            description=description,
                            activated_policy_types=activated_policy_types
                        )
                    )

                '''
                [   
                    {'display_name': '', 'description': '', 'sub_tags': []},
                    {}
                ]
                '''
                policy_tags_list = self.stage_dict.get('policy_tags_list', [])
                gcp_taxonomy_id = chosen_taxonomy.name
                create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # insert into taxonomyTable
                condition = 'workspace_id="%s" and input_form_id="%s" and creator_id="%s" and project_id="%s" and display_name="%s"' % (
                workspace_id, input_form_id, user_id, project_id, taxonomy_display_name)
                sql = self.create_select_sql(db_name, 'taxonomyTable', '*', condition=condition)
                # print('taxonomy select sql:', sql)
                taxonomy_info = self.execute_fetch_one(conn, sql)
                if not taxonomy_info:
                    fields = (
                    'workspace_id', 'input_form_id', 'creator_id', 'project_id', 'location', 'display_name', 'gcp_taxonomy_id', 'ad_group',
                    'description', 'create_time')
                    values = (
                    workspace_id, input_form_id, user_id, project_id, location, taxonomy_display_name, gcp_taxonomy_id, taxonomy_ad_group,
                    description, create_time)
                    sql = self.create_insert_sql(db_name, 'taxonomyTable', '({})'.format(', '.join(fields)), values)
                    # print('taxonomy insert sql:', sql)
                    local_taxonomy_id = self.insert_exec(conn, sql, return_insert_id=True)
                else:
                    local_taxonomy_id = taxonomy_info['id']

                # print('taxonomy_id:', gcp_taxonomy_id, local_taxonomy_id)
                # print('policy_tags_list:', policy_tags_list)
                while policy_tags_list:
                    new_policy_tags_list = []
                    for tag in policy_tags_list:

                        parent_local_id = -1
                        ad_group = tag.get('ad_group', '')
                        display_name = tag['display_name']
                        description = tag['description']
                        create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        policy_tag = datacatalog_v1beta1.PolicyTag(
                            display_name=display_name,
                            description=description
                        )

                        if 'parent_tag' in tag:
                            parent_local_id = tag['parent_local_id']
                            policy_tag.parent_policy_tag = tag['parent_tag']

                        tag_obj = client.create_policy_tag(parent=gcp_taxonomy_id, policy_tag=policy_tag)

                        # insert policy tags table
                        fields = (
                            'local_taxonomy_id', 'parent_local_id', 'gcp_policy_tag_id', 'ad_group', 'display_name',
                            'description', 'create_time')
                        values = (
                            local_taxonomy_id, parent_local_id, tag_obj.name, ad_group, display_name, description,
                            create_time)
                        sql = self.create_insert_sql(db_name, 'policyTagsTable', '({})'.format(', '.join(fields)), values)
                        logger.debug('FN:CreatePolicyTagsV1_execute policyTagsTable_insert_sql:{}'.format(sql))
                        local_id = self.insert_exec(conn, sql, return_insert_id=True)
                        if tag_obj and 'sub_tags' in tag:
                            parent_tag = tag_obj.name
                            for i in range(len(tag['sub_tags'])):
                                tag['sub_tags'][i]['parent_tag'] = parent_tag
                                tag['sub_tags'][i]['parent_local_id'] = local_id
                            new_policy_tags_list.extend(tag['sub_tags'])

                    policy_tags_list = new_policy_tags_list
                
                logger.debug('FN:CreatePolicyTagsV1_execute new_policy_tags_list:{}'.format(policy_tags_list))

                data = response_code.SUCCESS
                data['data'] = 'create successfully.'
                return data
        except HttpError as e:
            error_json = json.loads(e.content.replace('\\', '\\\\'), strict=False)
            data = error_json['error']
            data["msg"] = data.pop("message")
            logger.error("FN:CreatePolicyTagsV1_execute error:{}".format(traceback.format_exc()))
            return data
        except Exception as e:
            logger.error("FN:CreatePolicyTagsV1_execute error:{}".format(traceback.format_exc()))
            data = response_code.BAD_REQUEST
            data['msg'] = str(e)
            return data
        finally:
            conn.close()
