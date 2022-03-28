#!/usr/bin/python
# -*- coding: UTF-8 -*

from db.gcp.task_operator import taskFetcher
from config import configuration
from db.base import DbBase
from db.connection_pool import MysqlConn
import json
from google.cloud import bigquery
from utils.status_code import response_code
from google.cloud import datacatalog_v1
import traceback
import logging

logger = logging.getLogger("main." + __name__)

class DbGCPMgr(DbBase):

    def get_gpc_tasks(self, form_id=None, input_form_id=None):
        conn = MysqlConn()
        db_name = configuration.get_database_name()

        try:
            if form_id and input_form_id:
                form_id_infos = [{'id': input_form_id, 'form_id': form_id}]
            else:
                sql = self.create_select_sql(db_name, 'inputFormIndexTable', 'id, form_id')
                # print('inputFormIndexTable: ', sql)
                form_id_infos = self.execute_fetch_all(conn, sql)
            # form_id_infos = [{'id': 410}]
            tasks_infos = []
            for form_id_info in form_id_infos:

                miss_role_list = []

                input_form_id = form_id_info['id']
                form_id = form_id_info['form_id']
                input_form_condition = 'id="%s" order by history_id desc' % (input_form_id)
                sql = self.create_select_sql(db_name, 'inputFormTable', 'workflow_stages_id_list', input_form_condition)
                logger.debug("FN:DbGCPMgr_get_gpc_tasks inputFormTable_sql:{}".format(sql))
                form_infos = self.execute_fetch_all(conn, sql)
                if not form_infos:
                    continue

                workflow_stages_id_list = json.loads(form_infos[0]['workflow_stages_id_list'])
                logger.debug("FN:DbGCPMgr_get_gpc_tasks workflow_stages_id_list:{}".format(workflow_stages_id_list))
                workflow_stages_id_list = (str(id) for id in workflow_stages_id_list)

                input_stage_condition = "status!='%s' and id in ('%s')order by stage_index desc" % (1, "', '".join(workflow_stages_id_list))
                sql = self.create_select_sql(db_name, 'inputStageTable', 'id,apiTaskName,condition_value_dict',
                                             input_stage_condition)
                logger.debug("FN:DbGCPMgr_get_gpc_tasks inputStageTable_sql:{}".format(sql))
                stage_infos = self.execute_fetch_all(conn, sql)
                gcp_tasks = []
                tasks = []

                for stage_info in stage_infos:
                    tasks.append({'id': stage_info['id'], 'name': stage_info['apiTaskName'],
                                  "stages": json.loads(stage_info['condition_value_dict'])})

                logger.debug("FN:DbGCPMgr_get_gpc_tasks tasks:{}".format(tasks))
                torro_roles = taskFetcher.get_service_account_roles(taskFetcher.project_id,
                                                                    taskFetcher.service_account)
                for task in tasks:
                    task_name = task['name']
                    stage_dict = task['stages']
                    task = taskFetcher.build_task_object(task_name, stage_dict)
                    gcp_tasks.append(task)
                    task_type = task.api_type
                    if task_type == 'gcp':
                        task_project_id = task.target_project
                        sa_roles = None
                        if task_project_id == taskFetcher.project_id:
                            sa_roles = torro_roles
                        access_flag = taskFetcher.check_roles(task,
                                                              default_service_account=None,
                                                              default_project_sa_roles=sa_roles)
                        if access_flag == 0:
                            miss_role_list.append('-- ' + task_name + ': [' + ', '.join(task.role_list) + ']')
                if len(miss_role_list) != 0:
                    data = response_code.UPDATE_DATA_FAIL
                    data['msg'] = 'Your form\'s tasks miss one of roles of each tasks:\n{}\nPlease find IT support.'.format('\n'.join(miss_role_list))
                    tasks_infos.append(data)

                else:
                    data = response_code.SUCCESS
                    data['data'] = {'gcp_tasks': gcp_tasks, 'tasks': tasks, 'form_id': form_id, 'input_form_id': input_form_id}
                    tasks_infos.append(data)
            return tasks_infos

        except Exception as e:
            logger.error("FN:DbGCPMgr_get_gpc_tasks error:{}".format(traceback.format_exc()))
            return response_code.GET_DATA_FAIL
        finally:
            conn.close()

    def policy_tags_loop(self, field, db_name, conn):
        if field['type'] != 'RECORD':
            if 'policyTags' in field:
                policy_tags = field['policyTags']['names']
                local_policy_tag_id = []
                for gcp_policy_tag_id in policy_tags:
                    cond = "gcp_policy_tag_id='%s'" % gcp_policy_tag_id
                    sql = self.create_select_sql(db_name, 'policyTagsTable', 'id,ad_group', cond)
                    logger.debug("FN:DbGCPMgr_get_table_schema policyTagsTable_sql:{}".format(sql))
                    policy_tag_info = self.execute_fetch_one(conn, sql)
                    if policy_tag_info:
                        local_policy_tag_id.append(policy_tag_info['id'])
                    else:
                        local_policy_tag_id = [None]
                field['policyTags']['names'] = local_policy_tag_id
        else:
            for index in range(len(field['fields'])):
                field['fields'][index] = self.policy_tags_loop(field['fields'][index], db_name, conn)
        return field

    def column_tags_loop(self, field, parent_name, column_tags):
        if parent_name:
            field['column_name'] = parent_name + '.' + field['name']
        else:
            field['column_name'] = field['name']
        if field['type'] != 'RECORD':
            column_name = field['column_name']
            if column_name in column_tags:
                if 'tags' not in field:
                    field['tags'] = []
                field['tags'].append(column_tags[column_name])

            return field
        else:
            for index in range(len(field['fields'])):
                field['fields'][index] = self.column_tags_loop(field['fields'][index], field['column_name'], column_tags)
            return field

    def get_table_schema(self, request_data, user_key, workspace_id):
        conn = MysqlConn()
        db_name = configuration.get_database_name()

        try:

            # 1. check if the table is onboarded

            # 2. get columm tags
            project_id = request_data['projectId']
            dataset_id = request_data['datasetName']
            table_id = request_data['tableName']
            from_torro = request_data.get('fromTorro', False)

            client = bigquery.Client(project_id)
            project = client.project
            dataset_ref = bigquery.DatasetReference(project, dataset_id)
            table_ref = dataset_ref.table(table_id)
            table = client.get_table(table_ref)  # API request

            table_schema = table.to_api_repr()
            # workspace_id | project_id | dataset_id | table_id
            # check if it is alreadys in torro
            if from_torro:
                cond = "workspace_id='%s' and project_id='%s' and dataset_id='%s' and table_id='%s'" % (workspace_id, project_id, dataset_id, table_id)
                sql = self.create_select_sql(db_name, 'dataOnboardTable', 'input_form_id', cond)
                logger.debug("FN:DbGCPMgr_get_table_schema dataOnboardTable_sql:{}".format(sql))
                table_info = self.execute_fetch_one(conn, sql)
                if not table_info:
                    data = response_code.GET_DATA_FAIL
                    data['msg'] = 'Table not found in torro.'
                    return data
            # get tags
            datacatalog_client = datacatalog_v1.DataCatalogClient()
            resource_name = (
                f"//bigquery.googleapis.com/projects/{project_id}"
                f"/datasets/{dataset_id}/tables/{table_id}"
            )
            table_entry = datacatalog_client.lookup_entry(
                request={"linked_resource": resource_name}
            )
            table_tags = []
            column_tags = {}
            # print(table_entry)
            tags = datacatalog_client.list_tags(parent=table_entry.name)
            for tag in tags:
                tag_template_full_name = str(tag.template)
                if '/tagTemplates/' not in tag_template_full_name:
                    continue
                tag_tempalte_header, tag_template_id = tag_template_full_name.split('/tagTemplates/')
                tag_tempalte_header, tag_template_locations = tag_tempalte_header.split('/locations/')
                tag_template_project = tag_tempalte_header.replace('projects/', '')
                relations = [{"table_name": "formTable", "join_condition": "tagTemplatesTable.tag_template_form_id=formTable.id"}]
                condition = 'tag_template_id="%s" and project_id="%s" and location="%s" and (tagTemplatesTable.workspace_id="%s" or tagTemplatesTable.workspace_id=0)' % (tag_template_id, tag_template_project,tag_template_locations, workspace_id)
                sql = self.create_get_relation_sql(db_name, 'tagTemplatesTable', 'tag_template_form_id, fields_list', relations=relations, condition=condition)
                logger.debug("FN:DbGCPMgr_get_table_schema tagTemplatesTable_sql:{}".format(sql))
                data = self.execute_fetch_one(conn, sql)
                if not data:
                    continue
                tag_template_form_id = data['tag_template_form_id']
                field_list = json.loads(data['fields_list'])
                field_dict = dict(tag.fields)
                field_mapping = {}
                for field in field_list:
                    label = field['label']
                    field_id = label.replace(' ', '_').lower().strip()
                    id = field['id']
                    style = field['style']
                    if field_id not in field_mapping:
                        field_mapping[field_id] = {'id': id, 'style': style}

                return_data = {}

                # print('field_mapping:', field_mapping)
                # print('field_dict:', field_dict)
                for key in field_dict:
                    logger.debug("FN:DbGCPMgr_get_table_schema key:{} return_data:{}".format(key, return_data))
                    if key in field_mapping:
                        id = field_mapping[key]['id']
                        style = int(field_mapping[key]['style'])
                        if style == 5:
                            return_data[key] = field_dict[key].bool_value
                        elif style == 2:
                            return_data[key] = field_dict[key].enum_value
                        elif style == 1 or style == 3:
                            return_data[key] = field_dict[key].string_value
                        elif style == 6:
                            return_data[key] = field_dict[key].timestamp_value

                    else:
                        continue

                form_return_data = {}
                for field_id in return_data:
                    form_return_data[field_mapping[field_id]['id']] = return_data[field_id]
                return_tag = { "tag_template_form_id": tag_template_form_id, "data": form_return_data}
                tag_column_name = tag.column
                if tag_column_name == '':
                    table_tags.append(return_tag)
                else:
                    if tag_column_name not in column_tags:
                        column_tags[tag_column_name] = return_tag
            if not table_tags:
                table_schema['tags'] = []
            else:
                table_schema['tags'] = table_tags
            for index in range(len(table_schema['schema']['fields'])):
                # fill column tags
                # get record column name
                table_schema['schema']['fields'][index] = self.column_tags_loop(table_schema['schema']['fields'][index],
                                                                                '', column_tags)
                # column_name = table_schema['schema']['fields'][index]['column_name']
                # if column_name in column_tags:
                #     if 'tags' not in table_schema['schema']['fields'][index]:
                #         table_schema['schema']['fields'][index]['tags'] = []
                #     table_schema['schema']['fields'][index]['tags'].append(column_tags[column_name])

                # replace column policy tags
                table_schema['schema']['fields'][index] = self.policy_tags_loop(table_schema['schema']['fields'][index],
                                                                                db_name, conn)
                # if 'policyTags' in table_schema['schema']['fields'][index]:
                #     policy_tags = table_schema['schema']['fields'][index]['policyTags']['names']
                #     local_policy_tag_id = []
                #     for gcp_policy_tag_id in policy_tags:
                #         cond = "gcp_policy_tag_id='%s'" % gcp_policy_tag_id
                #         sql = self.create_select_sql(db_name, 'policyTagsTable', 'id,ad_group', cond)
                #         logger.debug("FN:DbGCPMgr_get_table_schema policyTagsTable_sql:{}".format(sql))
                #         policy_tag_info = self.execute_fetch_one(conn, sql)
                #         if policy_tag_info:
                #             local_policy_tag_id.append(policy_tag_info['id'])
                #         else:
                #             local_policy_tag_id = [None]
                #     table_schema['schema']['fields'][index]['policyTags']['names'] = local_policy_tag_id
            data = response_code.SUCCESS
            data['data'] = table_schema

            return data

        except Exception as e:
            logger.error("FN:DbGCPMgr_get_table_schema error:{}".format(traceback.format_exc()))
            return response_code.GET_DATA_FAIL
        finally:
            conn.close()

    def list_table(self, request_data, user_key, workspace_id):

        try:
            project_id = request_data.get('projectId', None)
            dataset_id = request_data.get('datasetName', None)

            if project_id is None:

                data = response_code.GET_DATA_FAIL
                data['msg'] = 'project not found'

            client = bigquery.Client(project_id)
            if dataset_id is None:
                datasets = list(client.list_datasets())
                if datasets:

                    data = response_code.SUCCESS
                    return_dataset = []
                    logger.debug("FN:DbGCPMgr_list_table datasets_project:{}".format(project_id))
                    for dataset in datasets:
                        return_dataset.append(dataset.dataset_id)
                    data['data'] = return_dataset
                    return data
                else:
                    data = response_code.GET_DATA_FAIL
                    data['msg'] = "{} project does not contain any datasets.".format(project_id)
                    return data
            else:
                tables = client.list_tables(dataset_id)  # Make an API request.
                return_tables = []
                logger.debug("FN:DbGCPMgr_list_table table_datasets:{}".format(dataset_id))

                for table in tables:
                    return_tables.append(table.table_id)
                data = response_code.SUCCESS
                data['data'] = return_tables
                return data

        except:
            logger.error("FN:DbGCPMgr_list_table error:{}".format(traceback.format_exc()))

            
db_gcp_mgr = DbGCPMgr()
