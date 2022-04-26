#!/usr/bin/python
# -*- coding: UTF-8 -*

import datetime
from db.base import DbBase
from db.connection_pool import MysqlConn
import copy
from utils.status_code import response_code
from config import configuration
from common.common_crypto import prpcrypt
import json
# from werkzeug.security import generate_password_hash, check_password_hash
import traceback
import logging

logger = logging.getLogger("main." + __name__)

class DbWorkflowMgr(DbBase):
 
    # already have 0-6 approval
    defalut_stages = [
                {
                    "group": "Approval",
                    "itemList": [
                        {
                            "apiTaskName": "",
                            "condition": [],
                            "flowType": "Approval",
                            "id": "101",
                            "label": "Approval Process"
                        }
                    ],
                    "commonConditions": [
                        {"id": 8, "label": "System approval", "value": "", "style": 6},
                        {"id": 1, "label": "Workspace owner", "value": "", "style": 6},
                        {"id": 7, "label": "Workspace IT approval", "value": "", "style": 6},
                        {"id": 2, "label": "Region / Country owner", "value": "", "style": 6},
                        # {"id": 3, "label": "{ynamic field approval".format(label), "value": field_id, "style": 6}
                        {"id": 0, "label": "Data owner", "value": "", "style": 6},
                        {"id": 5, "label": "Use case data approver(s)", "value": "", "style": 6},
                        {"id": 4, "label": "Line manager", "value": "", "style": 6},
                        # id 6 is policy tag approval task

                    ],
                    "label": "Approval Process"
                },
                {
                    "group": "GoogleCloud",
                    "label": "Google Cloud Task",
                    "itemList": []
                },
                {
                    "group": "System",
                    "itemList": [
                        {
                            "apiTaskName": "system_email_notify",
                            "condition": [
                                {
                                    "id": "groups",
                                    "label": "Groups",
                                    "value": "",
                                    "style": 3
                                },
                                {
                                    "id": "emails",
                                    "label": "User emails",
                                    "value": "",
                                    "style": 3
                                },
                                {
                                    "id": "email_msg",
                                    "label": "Email msg",
                                    "value": "",
                                    "style": 3
                                }
                            ],
                            "flowType": "System",
                            "id": 102,
                            "label": "Emails Notification"
                        },
                        {
                            "apiTaskName": "system_notify",
                            "condition": [
                                {
                                    "id": "groups",
                                    "label": "Groups",
                                    "value": "",
                                    "style": 3
                                },
                                {
                                    "id": "emails",
                                    "label": "User emails",
                                    "value": "",
                                    "style": 3
                                },
                                {
                                    "id": "notify_msg",
                                    "label": "Notify msg",
                                    "value": "",
                                    "style": 3
                                }
                            ],
                            "flowType": "System",
                            "id": 103,
                            "label": "System Notification"
                        },
                        {
                            "apiTaskName": "system_define_field",
                            "condition": [
                                {
                                    "id": "FieldLabel",
                                    "label": "Field Label",
                                    "value": "",
                                    "style": 1
                                },
                                {
                                    "id": "optionLabel",
                                    "label": "Option Label",
                                    "value": "",
                                    "style": 5
                                },
                                {
                                    "id": "optionsValue",
                                    "label": "Option Value",
                                    "value": "",
                                    "style": 5
                                }
                            ],
                            "flowType": "System",
                            "id": 107,
                            "label": "Dynamic Approval Field"
                        },
                        {
                            "apiTaskName": "system_create_form",
                            "condition": [
                                {
                                    "id": "form_name",
                                    "label": "Form Name",
                                    "value": "",
                                    "style": 5
                                },
                                {
                                    "id": "description",
                                    "label": "Description",
                                    "value": "",
                                    "style": 5
                                },
                                {
                                    "id": "field_list",
                                    "label": "field list",
                                    "value": "",
                                    "style": 5
                                }
                            ],
                            "flowType": "System",
                            "id": 104,
                            "label": "Create Form"
                        },
                        {
                            "apiTaskName": "system_update_form",
                            "condition": [
                                {
                                    "id": "id",
                                    "label": "Form ID",
                                    "value": "",
                                    "style": 5
                                },
                                {
                                    "id": "form_name",
                                    "label": "Form Name",
                                    "value": "",
                                    "style": 5
                                },
                                {
                                    "id": "description",
                                    "label": "Description",
                                    "value": "",
                                    "style": 5
                                },
                                {
                                    "id": "field_list",
                                    "label": "field list",
                                    "value": "",
                                    "style": 5
                                }
                            ],
                            "flowType": "System",
                            "id": 105,
                            "label": "Update Form"
                        },
                        {
                            "apiTaskName": "system_delete_form",
                            "condition": [
                                {
                                    "id": "id",
                                    "label": "Form ID",
                                    "value": "",
                                    "style": 5
                                },
                            ],
                            "flowType": "System",
                            "id": 106,
                            "label": "Delete Form"
                        },
                        {
                            "apiTaskName": "system_add_new_usecase",
                            "condition": [
                                {
                                    "id": "usecase_name",
                                    "label": "Usecase Name",
                                    "value": "",
                                    "style": 5
                                },
                                {
                                    "id": "region_country",
                                    "label": "Region/Country",
                                    "value": "",
                                    "style": 5
                                },
                                {
                                    "id": "validity_date",
                                    "label": "Validity Date",
                                    "value": "",
                                    "style": 5
                                },
                                {
                                    "id": "uc_des",
                                    "label": "Description",
                                    "value": "",
                                    "style": 5
                                },
                                {
                                    "id": "admin_sa",
                                    "label": "Admin Service Account",
                                    "value": "",
                                    "style": 5
                                },
                                {
                                    "id": "budget",
                                    "label": "Budget",
                                    "value": "",
                                    "style": 5
                                },
                                {
                                    "id": "allow_cross_region",
                                    "label": "Allow Cross Region",
                                    "value": "",
                                    "style": 5
                                },
                                {
                                    "id": "resources_access",
                                    "label": "Resources Access",
                                    "value": "",
                                    "style": 5
                                },
                                {
                                    "id": "uc_team_group",
                                    "label": "Team group",
                                    "value": "",
                                    "style": 5
                                },
                                {
                                    "id": "uc_owner_group",
                                    "label": "Owner group",
                                    "value": "",
                                    "style": 5
                                }
                            ],
                            "flowType": "System",
                            "id": 107,
                            "label": "Create New Use Case"
                        }
                    ],
                    "label": "System Task"
                }]


    def get_all_base_workflow(self, workspace_id):
        """
        get all workflow list
        :return:
        """
        conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            # get all workspace form
            sql = self.create_select_sql(db_name, 'formTable',
                                         'id', condition='hide=0 and (workspace_id="%s" or workspace_id=0)' % workspace_id)
            forms_info = self.execute_fetch_all(conn, sql)
            form_id_set = set()
            for form_info in forms_info:
                id = form_info['id']
                form_id_set.add(str(id))
            condition = 'form_id in ({})'.format(' , '.join(form_id_set))
            sql = self.create_select_sql(db_name, 'workflowTable',
                                         'id,form_id,workflow_name,stage_hash,stage_num,creator_id,available,last_modify_id,create_time,updated_time,des',
                                         condition)
            logger.debug("FN:DbWorkflowMgr_get_all_base_workflow workflowTable_sql:{}".format(sql))
            workflows_info = self.execute_fetch_all(conn, sql)
            data = response_code.SUCCESS
            data['data'] = workflows_info
            return data
        except Exception as e:
            logger.error("FN:DbWorkflowMgr_get_all_base_workflow error:{}".format(traceback.format_exc()))
            return response_code.GET_DATA_FAIL
        finally:
            conn.close()

    # get all base workflow by form id
    def get_all_base_workflow_by_form_id(self, form_id):
        """
        get all workflow list
        :return:
        """
        conn = MysqlConn()
        try:
            condition = "form_id='%s'" % form_id
            db_name = configuration.get_database_name()
            sql = self.create_select_sql(db_name, 'workflowTable',
                                         'id,form_id,workflow_name,stage_hash,stage_num,available,creator_id,last_modify_id,create_time,updated_time,des',
                                         condition=condition)
            logger.debug("FN:DbWorkflowMgr_get_all_base_workflow_by_form_id workflowTable_sql:{}".format(sql))
            workflows_info = self.execute_fetch_all(conn, sql)
            data = response_code.SUCCESS
            data['data'] = workflows_info
            return data
        except Exception as e:
            logger.error("FN:DbWorkflowMgr_get_all_base_workflow_by_form_id error:{}".format(traceback.format_exc()))
            return response_code.GET_DATA_FAIL
        finally:
            conn.close()

    # get one base workflow by id
    def get_base_workflow_by_workflow_id(self, id):
        """
        get workflow base info
        :return:
        """
        conn = MysqlConn()
        try:
            condition = "id='%s'" % id
            db_name = configuration.get_database_name()
            sql = self.create_select_sql(db_name, 'workflowTable',
                                         'id,form_id,workflow_name,stage_hash,stage_num,creator_id,last_modify_id,create_time,updated_time,des',
                                         condition=condition)
            logger.debug("FN:DbWorkflowMgr_get_base_workflow_by_workflow_id workflowTable_sql:{}".format(sql))
            workflow_info = self.execute_fetch_one(conn, sql)
            data = response_code.SUCCESS
            data['data'] = workflow_info
            return data
        except Exception as e:
            logger.error("FN:DbWorkflowMgr_get_base_workflow_by_workflow_id error:{}".format(traceback.format_exc()))
            return response_code.GET_DATA_FAIL
        finally:
            conn.close()  # get detail workflow

    # get all details workflow by form id
    def get_all_details_workflow_by_form_id(self, form_id):
        """
        get all workflow list
        :return:
        """
        conn = MysqlConn()
        try:
            condition = "form_id='%s'" % form_id
            db_name = configuration.get_database_name()
            sql = self.create_select_sql(db_name, 'workflowTable',
                                         'id,form_id,workflow_name,stage_hash,stage_num,available,creator_id,last_modify_id,stages,field_id_list,create_time,updated_time,des',
                                         condition=condition)
            logger.debug("FN:DbWorkflowMgr_get_all_details_workflow_by_form_id workflowTable_sql:{}".format(sql))
            workflows_info = self.execute_fetch_all(conn, sql)
            for index in range(len(workflows_info)):
                workflows_info[index]['stages'] = json.loads(workflows_info[index]['stages'].replace('\\', '\\\\'), strict=False)
                workflows_info[index]['field_id_list'] = json.loads(workflows_info[index]['field_id_list'].replace('\\', '\\\\'), strict=False)
            data = response_code.SUCCESS
            data['data'] = workflows_info
            return data
        except Exception as e:
            logger.error("FN:DbWorkflowMgr_get_all_details_workflow_by_form_id error:{}".format(traceback.format_exc()))
            return response_code.GET_DATA_FAIL
        finally:
            conn.close()

    # get one details workflow by id
    def get_detail_workflow_by_workflow_id(self, id):
        """
        get workflow base info
        :return:
        """
        conn = MysqlConn()
        try:
            condition = "id='%s'" % id
            db_name = configuration.get_database_name()
            sql = self.create_select_sql(db_name, 'workflowTable',
                                         'id,form_id,workflow_name,stage_hash,stage_num,creator_id,available,last_modify_id,stages,field_id_list,create_time,updated_time,des',
                                         condition=condition)
            logger.debug("FN:DbWorkflowMgr_get_detail_workflow_by_workflow_id workflowTable_sql:{}".format(sql))
            workflow_info = self.execute_fetch_one(conn, sql)
            logger.debug("FN:DbWorkflowMgr_get_detail_workflow_by_workflow_id workflow_info:{}".format(workflow_info))
            workflow_info['stages'] = json.loads(workflow_info['stages'].replace('\\', '\\\\'), strict=False)
            workflow_info['field_id_list'] = json.loads(workflow_info['field_id_list'].replace('\\', '\\\\'), strict=False)
            data = response_code.SUCCESS
            data['data'] = workflow_info
            return data
        except Exception as e:
            logger.error("FN:DbWorkflowMgr_get_detail_workflow_by_workflow_id error:{}".format(traceback.format_exc()))
            return response_code.GET_DATA_FAIL
        finally:
            conn.close()  # get detail workflow

    # get stages by label, group, flowtype
    def get_stages_with_condition(self, condition={}):
        """
        get workflow detail info
        :return:
        """
        conn = MysqlConn()
        try:
            condition_set = set()
            for field in condition:
                condition_set.add("%s='%s'" % (field.strip(), condition[field].strip()))
            condition_str = ','.join(condition_set)
            db_name = configuration.get_database_name()
            sql = self.create_select_sql(db_name, 'stageTable', '*', condition=condition_str)
            logger.debug("FN:DbWorkflowMgr_get_stages_with_condition stageTable_sql:{}".format(sql))
            stage_info = self.execute_fetch_all(conn, sql)
            for index in range(len(stage_info)):
                stage_info[index]['arguments'] = json.loads(stage_info[index]['arguments'].replace('\\', '\\\\'), strict=False)
            # get fields info
            data = response_code.SUCCESS
            data['data'] = stage_info
            return data
        except Exception as e:
            logger.error("FN:DbWorkflowMgr_get_stages_with_condition error:{}".format(traceback.format_exc()))
            return response_code.GET_DATA_FAIL
        finally:
            conn.close()

    # get stages by id
    def get_stage_by_id(self, id):
        conn = MysqlConn()
        try:
            condition = "id='%s'" % id
            db_name = configuration.get_database_name()
            sql = self.create_select_sql(db_name, 'stageTable', '*', condition=condition)
            logger.debug("FN:DbWorkflowMgr_get_all_stages stageTable_sql:{}".format(sql))
            stage_info = self.execute_fetch_one(conn, sql)
            stage_info['arguments'] = json.loads(stage_info['arguments'].replace('\\', '\\\\'), strict=False)
            data = response_code.SUCCESS
            data['data'] = stage_info
            return data
        except Exception as e:
            logger.error("FN:DbWorkflowMgr_get_all_stages error:{}".format(traceback.format_exc()))
            return response_code.GET_DATA_FAIL
        finally:
            conn.close()  # get detail workflow

    # get all stages
    def get_all_stages(self):
        """
        get all stage info
        :return:
        """
        db_conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            table_name = 'stageTable'
            fields = '*'
            sql = self.create_select_sql(db_name, table_name, fields)
            logger.debug("FN:DbWorkflowMgr_get_all_stages {}_sql:{}".format(table_name,sql))
            result = copy.deepcopy(self.defalut_stages)
            itemList = self.execute_fetch_all(db_conn, sql)
            for index in range(len(itemList)):
                itemList[index]['condition'] = json.loads(itemList[index]['condition'].replace('\\', '\\\\'), strict=False)
            result[1]["itemList"] = itemList
            data = response_code.SUCCESS
            data['data'] = result
            return data
        except Exception as e:
            logger.error("FN:DbWorkflowMgr_get_all_stages error:{}".format(traceback.format_exc()))
            return response_code.GET_DATA_FAIL
        finally:
            db_conn.close()

    def get_all_stages_v2(self, workflow_id):
        """
        get all stage info
        :return:
        """
        db_conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            table_name = 'stageTable'
            fields = '*'
            sql = self.create_select_sql(db_name, table_name, fields)
            result = copy.deepcopy(self.defalut_stages)
            itemList = self.execute_fetch_all(db_conn, sql)
            for index in range(len(itemList)):
                itemList[index]['condition'] = json.loads(itemList[index]['condition'].replace('\\', '\\\\'), strict=False)
            result[1]["itemList"] = itemList


            table_name = 'workflowTable'
            role_relations = [{"table_name": "formTable", "join_condition": "workflowTable.form_id=formTable.id"}]
            condition = "workflowTable.id='%s'" % (workflow_id)
            fields = 'formTable.fields_list'
            sql = self.create_get_relation_sql(db_name, table_name, fields, role_relations,
                                                               condition=condition)
            # conditon = 'id=%s' % (form_id)
            print('sql:', sql)
            # sql = self.create_select_sql(db_name, 'formTable', '*', condition=conditon)
            form_info = self.execute_fetch_one(db_conn, sql)
            fields_list = json.loads(form_info['fields_list'].replace('\\', '\\\\'), strict=False)
            # deduplication list
            field_id_list = []
            for field in fields_list:
                field_id = field['id']
                label = field['label']
                print('field_id_list:', field_id_list)
                if 'd' in field_id and field_id not in field_id_list:
                    field_id_list.append(field_id)
                    approval_item = {"id": 3, "label": "{} approval".format(label), "value": field_id, "style": 6}
                    logger.debug("FN:DbWorkflowMgr_get_all_stages_v2 approval_item:{}".format(result[0]['commonConditions']))
                    result[0]['commonConditions'].append(approval_item)
            logger.debug("FN:DbWorkflowMgr_get_all_stages_v2 result:{}".format(result))
            data = response_code.SUCCESS
            data['data'] = result
            return data
        except Exception as e:
            logger.error("FN:DbWorkflowMgr_get_all_stages_v2 error:{}".format(traceback.format_exc()))
            return response_code.GET_DATA_FAIL
        finally:
            db_conn.close()

    # delete one workflow
    def delete_workflow(self, workflow):

        conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            id = workflow['id']
            # Check if Workflow exists
            data = self.get_base_workflow_by_workflow_id(id=id)
            # # print('data', data)
            logger.debug("FN:DbWorkflowMgr_delete_workflow data:{}".format(data))
            if data['code'] == 200 and data['data']['stage_hash'] == workflow['stage_hash']:
                condition = "id=%s" % id
                delete_table_sql = self.create_delete_sql(db_name, "workflowTable", condition)
                self.delete_exec(conn, delete_table_sql)
            else:
                data = response_code.DELETE_DATA_FAIL

            return data

        except Exception as e:
            logger.error("FN:DbWorkflowMgr_delete_workflow error:{}".format(traceback.format_exc()))
            conn.conn.rollback()
            return response_code.DELETE_DATA_FAIL
        finally:
            conn.close()

    # add new workflow
    def add_new_workflow(self, workflow):

        conn = MysqlConn()
        try:
            form_id = workflow['form_id']
            workflow_name = workflow['workflow_name']
            # stage_hash = secret_key(workflow_name, 32)
            stage_num = len(workflow['stages'])
            creator_id = workflow.get('creator_id', '')
            last_modify_id = workflow.get('creator_id', '')
            stages = json.dumps(workflow['stages'])
            field_id_list = json.dumps(workflow['field_id_list'])
            des = workflow.get('des', '')
            create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            update_time = create_time
            db_name = configuration.get_database_name()

            # get hash code
            condition = 'id = "%s"' % form_id
            sql = self.create_select_sql(db_name, 'formTable', 'id,updated_time', condition)
            form_info = self.execute_fetch_one(conn, sql)
            if not form_info:
                data = response_code.GET_DATA_FAIL
                data['msg'] = 'can not find the form.'
                return data
            stage_hash = prpcrypt.encrypt(str(form_info['id'])+'||'+str(form_info['updated_time']))
            # # print('stage_hash:', prpcrypt.decrypt(stage_hash))
            # insert workflow
            fields = ('form_id', 'workflow_name', 'stage_hash', 'stage_num', 'creator_id', 'last_modify_id', 'stages',
                      'field_id_list', 'create_time', 'updated_time', 'des')
            values = (form_id, workflow_name, stage_hash, stage_num, creator_id, last_modify_id, stages, field_id_list,
                      create_time, update_time, des)
            sql = self.create_insert_sql(db_name, 'workflowTable', '({})'.format(', '.join(fields)), values)
            logger.debug("FN:DbWorkflowMgr_add_new_workflow insert_workflowTable_sql:{}".format(sql))
            workflow_id = self.insert_exec(conn, sql, return_insert_id=True)
            workflow['id'] = workflow_id
            workflow['stage_hash'] = stage_hash
            data = response_code.SUCCESS
            data['data'] = workflow
            return data
        except Exception as e:
            logger.error("FN:DbWorkflowMgr_add_new_workflow error:{}".format(traceback.format_exc()))
            return response_code.GET_DATA_FAIL
        finally:
            conn.close()

    # update workflow
    def update_workflow(self, workflow):
        conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()

            workflow_id = workflow['id']
            # Check if workflow exist
            select_workflow = self.get_base_workflow_by_workflow_id(id=workflow_id)
            logger.debug("FN:DbWorkflowMgr_update_workflow select_workflow:{}".format(select_workflow))
            if select_workflow['code'] == 200 and select_workflow['data']['stage_hash'] == workflow['stage_hash']:
                workflow_condition = "id='%s'" % workflow_id

                form_id = workflow['form_id']
                workflow_name = workflow['workflow_name']
                # get hash code
                condition = 'id = "%s"' % form_id
                sql = self.create_select_sql(db_name, 'formTable', 'id,updated_time', condition)
                form_info = self.execute_fetch_one(conn, sql)
                if not form_info:
                    data = response_code.GET_DATA_FAIL
                    data['msg'] = 'can not find the form.'
                    return data
                stage_hash = prpcrypt.encrypt(str(form_info['id']) + '||' + str(form_info['updated_time']))

                stage_num = len(workflow['stages'])
                creator_id = workflow.get('creator_id', '')
                last_modify_id = workflow.get('creator_id', '')
                stages = json.dumps(workflow['stages'])
                field_id_list = json.dumps(workflow['field_id_list'])
                des = workflow.get('des', '')
                create_time = workflow.get('create_time', datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                update_time = create_time
                fields = (
                    'form_id', 'workflow_name', 'stage_hash', 'stage_num', 'creator_id', 'last_modify_id', 'stages',
                    'field_id_list',
                    'create_time', 'updated_time', 'des')
                values = (
                    form_id, workflow_name, stage_hash, stage_num, creator_id, last_modify_id, stages, field_id_list,
                    create_time,
                    update_time, des)
                # update workflow
                sql = self.create_update_sql(db_name, 'workflowTable', fields, values, workflow_condition)
                logger.debug("FN:DbWorkflowMgr_update_workflow update_workflowTable_sql:{}".format(sql))
                return_count = self.updete_exec(conn, sql)
                data = response_code.SUCCESS
                data['data'] = workflow
            else:
                data = response_code.UPDATE_DATA_FAIL
            return data
        except Exception as e:
            logger.error("FN:DbWorkflowMgr_update_workflow error:{}".format(traceback.format_exc()))
            return response_code.GET_DATA_FAIL
        finally:
            conn.close()


workflow_mgr = DbWorkflowMgr()
