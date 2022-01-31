#!/usr/bin/python
# -*- coding: UTF-8 -*

from string import Template
from config import configuration
from db.base import DbBase
from db.connection_pool import MysqlConn
import json
from utils.status_code import response_code
from utils.log_helper import lg
from utils.bucket_object_helper import upload_blob
from utils.bucket_url_helper import generate_download_signed_url_v4
from common.common_crypto import prpcrypt
from common.common_input_form_status import status as Status
import datetime
import traceback
import os
from common.common_input_form_status import status
from config import config
from utils.ldap_helper import Ldap
config_name = os.getenv('FLASK_CONFIG') or 'default'
Config = config[config_name]


class DbInputFormMgr(DbBase):
    status = Status.code
    status_history_mapping = Status.status_history_mapping
    system_execute_tasks = Status.system_execute_tasks

    def __get_workspace_owner_group(self, workspace_id, approval_label):
        conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            ad_group_set = set()
            ad_group_id_set = set()
            condition = "WORKSPACE_ID='%s'" % workspace_id
            select_table_sql = self.create_select_sql(db_name, "workspace_to_adgroupTable", 'LABEL_LIST,AD_GROUP_ID',
                                                      condition)
            # print('workspace_to_adgroupTable_sql:', select_table_sql)
            label_list_infos = self.execute_fetch_all(conn, select_table_sql)
            for label_list_info in label_list_infos:
                label_list = json.loads(label_list_info['LABEL_LIST'])
                if approval_label in label_list:
                    ad_group_id_set.add(str(label_list_info['AD_GROUP_ID']))
            if ad_group_id_set:
                condition = "ID in (%s)" % ','.join(ad_group_id_set)
                select_table_sql = self.create_select_sql(db_name, "adgroupTable", '*', condition)
                # print('adgroupTable_sql:', select_table_sql)
                adgroup_infos = self.execute_fetch_all(conn, select_table_sql)
                for adgroup_info in adgroup_infos:
                    ad_group_set.add(adgroup_info['GROUP_MAIL'])
            return list(ad_group_set)
        except Exception as e:
            lg.error(e)
            return []
        finally:
            conn.close()

    def __get_workspace_region_group(self, workspace_id, region):
        conn = MysqlConn()
        try:

            db_name = configuration.get_database_name()
            adgroup = None
            condition = "ID=%s" % workspace_id
            select_table_sql = self.create_select_sql(db_name, "workspaceTable", '*', condition)
            # print('select_table_sql:', select_table_sql)
            workspace_info = self.execute_fetch_one(conn, select_table_sql)
            # print('workspace_info:', workspace_info)
            if workspace_info:
                regions = json.loads(workspace_info['REGOINS'])
                # # print(regions)
                for region_info in regions:
                    if adgroup is not None:
                        break
                    if region_info['region'] == region:
                        adgroup = region_info['group']
                        continue
                    if adgroup is None:
                        for country_info in region_info['countryList']:
                            if country_info['country'] == region:
                                adgroup = country_info['group']
                                break
            if adgroup:
                return [adgroup]
            else:
                return []

        except Exception as e:
            lg.error(e)
            return []
        finally:
            conn.close()

    def __add_approval(self, input_form_id, approval_num, ad_group, label=''):
        conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            if approval_num == 1:
                now_approval = 1
            else:
                now_approval = 0
            fields = ('input_form_id', 'approval_num', 'ad_group', 'now_approval', 'label')
            # now = str(datetime.datetime.today())
            values = (input_form_id, approval_num, ad_group, now_approval, label)
            sql = self.create_insert_sql(db_name, 'approvalTable', '({})'.format(', '.join(fields)), values)
            # print('approvalTable sql:', sql)
            approval_id = self.insert_exec(conn, sql, return_insert_id=True)
            return approval_id
        except Exception as e:
            lg.error(e)
            return response_code.ADD_DATA_FAIL
        finally:
            conn.close()

    def __remove_approval(self, input_form_id):
        conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            condition = "input_form_id=%s" % input_form_id
            select_table_sql = self.create_select_sql(db_name, "approvalTable", '*', condition)
            approval_infos = self.execute_fetch_all(conn, select_table_sql)
            if approval_infos:
                delete_table_sql = self.create_delete_sql(db_name, "approvalTable", condition)
                self.delete_exec(conn, delete_table_sql)
            return True
        except Exception as e:
            lg.error(e)
            return False
        finally:
            conn.close()

    def get_input_form_data(self, account_id, input_form_id, approver_view=False):

        db_conn = MysqlConn()
        try:


            adgroup_list = Ldap.get_member_ad_group(account_id, Status.offline_flag)

            input_form_list = []
            db_name = configuration.get_database_name()

            condition = 'id="%s"' % (input_form_id)
            sql = self.create_select_sql(db_name, 'inputFormIndexTable', '*', condition)
            # print('formTable: ', sql)
            input_form_index = self.execute_fetch_one(db_conn, sql)
            if not input_form_index:
                data = response_code.GET_DATA_FAIL
                data['msg'] = 'the input form id not exist.'
                return data
            form_id = input_form_index['form_id']
            # get inputForminfo
            table_name = 'inputFormTable'
            role_relations = [
                {"table_name": "inputFormIndexTable", "join_condition": "inputFormIndexTable.id=inputFormTable.id"}]
            condition = "inputFormTable.id='%s' order by history_id desc" % (input_form_id)
            fields = '*'
            sql = self.create_get_relation_sql(db_name, table_name, fields, role_relations,
                                               condition=condition)
            # print(sql)
            input_form_infos = self.execute_fetch_all(db_conn, sql)
            form_status = int(input_form_infos[0]['form_status'])
            form_field_values_dict = json.loads(input_form_infos[0]['form_field_values_dict'])
            # history_id = int(input_form_infos[0]['history_id'])
            # get status history
            status_history_list = []
            old_status_history_list = []
            # get approval data info and check if
            data_access_review = []
            table_name = 'approvalTable'
            condition = "input_form_id=%s " % (input_form_id)
            fields = '*'
            sql = self.create_select_sql(db_name, table_name, fields, condition)
            approval_infos = self.execute_fetch_all(db_conn, sql)
            now_approver_group = ''
            for index, approval_info in enumerate(approval_infos):
                approver_id = approval_info['account_id']
                approver_group = approval_info['ad_group']
                approver_label = approval_info.get('label', None)
                approver_time = approval_info['updated_time']
                approver_comment = approval_info['comment']
                now_approval_flag = approval_info['now_approval']
                print('now_approval:', now_approval_flag, approver_group, adgroup_list)
                if int(now_approval_flag) == 1 and approver_view and approver_group not in adgroup_list:
                    data = response_code.GET_DATA_FAIL
                    data['msg'] = 'you do not have access to view this page.'
                    return data
                if approver_comment is None:
                    approver_comment = ''
                is_approved = approval_info['is_approved']
                if approver_label:
                    status_label = 'Pending {} [{}] approval'.format(approver_group, approver_label)
                else:
                    status_label = 'Pending {} approval'.format(approver_group)
                status_history = {'label': status_label, 'operator': '', 'comment': '', 'time': approver_time}
                if approver_id:
                    status_history['label'] = '{} approved'.format(approver_group)
                    status_history['operator'] = approver_id
                    approved_flag = '[|{}|]'.format(Status.approved)
                    reject_flag = '[|{}|]'.format(Status.rejected)
                    if approved_flag in approver_comment:
                        approver_comment = approver_comment.replace(approved_flag, '')
                    elif reject_flag in status_history['comment']:
                        approver_comment = approver_comment.replace(reject_flag, '')
                    status_history['comment'] = approver_comment
                if is_approved == 0 and approver_time is not None and form_status in (1, 5, 6):
                    status_history['label'] = '{} {}'.format(status_label, self.status[form_status])
                else:
                    # find out now approval data
                    if form_id == Status.system_form_id['data_access']:
                        column_fields = form_field_values_dict.get(
                            Status.system_form_field_id['data_access']['field_id'], None)
                        if column_fields and 'value' in column_fields:
                            access_fields = column_fields['value']
                            for access_field in access_fields:
                                if 'policyTags' in access_field and 'names' in access_field['policyTags']:
                                    field_name = access_field['name']
                                    for local_policy_tags_id in access_field['policyTags']['names']:
                                        if not local_policy_tags_id:
                                            continue
                                        condition = "id=%s" % local_policy_tags_id
                                        sql = self.create_select_sql(db_name, 'policyTagsTable', 'ad_group',
                                                                     condition=condition)
                                        print('policyTagsTable sql:', sql)
                                        ad_group = self.execute_fetch_one(db_conn, sql)['ad_group']
                                        if ad_group == approver_group:
                                            data = {
                                                'project_id': form_field_values_dict.get(
                                                    Status.system_form_field_id['data_access']['project_id'],
                                                    {'value': None})['value'],
                                                'location': form_field_values_dict.get(
                                                    Status.system_form_field_id['data_access']['location'],
                                                    {'value': None})['value'],
                                                'dataset_id': form_field_values_dict.get(
                                                    Status.system_form_field_id['data_access']['dataset_id'],
                                                    {'value': None})['value'],
                                                'table_id': form_field_values_dict.get(
                                                    Status.system_form_field_id['data_access']['table_id'],
                                                    {'value': None})['value'],
                                                'field_name': field_name
                                            }
                                            data_access_review.append(data)

                    # pass
                status_history_list.append(status_history)
                old_status_history_list.append({'label': status_label, 'operator': '', 'comment': '', 'time': None})

            for input_form_info in input_form_infos:
                history_id = int(input_form_info['history_id'])
                form_field_values_dict = json.loads(input_form_info['form_field_values_dict'])
                input_form_info['form_field_values_dict'] = {}
                for field_id in form_field_values_dict:
                    if form_field_values_dict[field_id]['style'] == 4:
                        input_form_info['form_field_values_dict'][field_id] = []
                        for file_path in form_field_values_dict[field_id]['value']:
                            bucket_name = file_path.replace('gs://', '').split('/')[0]
                            blob_name = file_path.replace('gs://', '').replace(bucket_name, '')[1:]
                            file_name = file_path.split('/')[-1]
                            bucket_url_obj = {"fileName": file_name,
                                              "fileURL": generate_download_signed_url_v4(bucket_name, blob_name,
                                                                                         Config.DEFAULT_SA)}
                            # bucket_url_obj = {"fileName": file_name,   "fileURL": bucket_name+'||'+blob_name}
                            input_form_info['form_field_values_dict'][field_id].append(bucket_url_obj)
                    else:
                        input_form_info['form_field_values_dict'][field_id] = form_field_values_dict[field_id]['value']
                input_form_info['workflow_stages_id_list'] = json.loads(input_form_info['workflow_stages_id_list'])
                input_form_info['workflow_stages_list'] = []
                for index, input_stage_id in enumerate(input_form_info['workflow_stages_id_list']):
                    condition = "id='%s'" % (input_stage_id)
                    db_name = configuration.get_database_name()
                    sql = self.create_select_sql(db_name, 'inputStageTable', '*', condition=condition)
                    stage_info = self.execute_fetch_one(db_conn, sql)
                    # print('stage_info sql:', sql)
                    stage_info['condition_value_dict'] = json.loads(stage_info['condition_value_dict'])
                    # # print(field_info)
                    input_form_info['workflow_stages_list'].append(stage_info)
                del input_form_info['workflow_stages_id_list']
                input_form_info['status_history'] = old_status_history_list + self.status_history_mapping[5]

                condition = "input_form_id = %s and history_id = %s" % (input_form_id, history_id)
                relation = [{"table_name": "userTable", "join_condition": "userTable.id=inputCommentTable.creator_id"}]
                fields = (
                    'ACCOUNT_NAME', 'ACCOUNT_ID', 'comment', 'inputCommentTable.create_time', 'inputCommentTable.id')
                sql = self.create_get_relation_sql(db_name, 'inputCommentTable', ','.join(fields), relation, condition)
                # print('comment sql:', sql)
                comment_infos = self.execute_fetch_all(db_conn, sql)
                comment_history = []
                for comment_info in comment_infos:
                    comment = comment_info['comment']
                    comment_json = {"accountId": comment_info['ACCOUNT_ID'],
                                    "comment_id": comment_info['id'],
                                    "time": comment_info['create_time']}

                    approved_flag = '[|{}|]'.format(Status.approved)
                    reject_flag = '[|{}|]'.format(Status.rejected)
                    if approved_flag in comment:
                        comment = comment.replace(approved_flag, '')
                        comment_json['tag'] = 'Approved'
                    elif reject_flag in comment:
                        comment = comment.replace(reject_flag, '')
                        comment_json['tag'] = 'Rejected'
                    comment_json['comment'] = comment
                    comment_history.append(comment_json)
                input_form_info['comment_history'] = comment_history
                input_form_list.append(input_form_info)
            # # print(input_form_list)

            update_time = input_form_list[0]['updated_time']
            status_history_suffix = self.status_history_mapping.get(form_status, self.status_history_mapping[0])
            if form_status in (2, 3):
                status_history_suffix[0]['time'] = status_history_list[-1]['time']
            if form_status in (1, 2, 5, 6):
                status_history_suffix[-1]['time'] = update_time

            input_form_list[0]['status_history'] = status_history_list + status_history_suffix
            input_form_list[0]['data_approval'] = data_access_review
            # input_form_list[0]['comment_history'] = comment_history
            data = response_code.SUCCESS
            data['data'] = input_form_list
            return data
        except Exception as e:
            # lg.error(e)
            lg.error(traceback.format_exc())
            return response_code.GET_DATA_FAIL
        finally:
            db_conn.close()

    def input_form_data(self, user_key, inputData, workspace_id):
        """
        :return:
        """
        conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            form_id = inputData['form_id']
            field_ids = inputData['field_ids']
            creator_id = user_key
            # do the form exist
            condition = 'id=%s' % form_id
            sql = self.create_select_sql(db_name, 'formTable', 'updated_time', condition=condition)
            form_info = self.execute_fetch_one(conn, sql)
            if not form_info:
                data = response_code.ADD_DATA_FAIL
                data['msg'] = 'form not found'
                return data
            # do the user exist
            user_exist_flag = self.__check_table_id_exist(creator_id, 'userTable', db_name, conn)
            if not user_exist_flag:
                data = response_code.ADD_DATA_FAIL
                data['msg'] = 'user not found'
                return data
            # get workflow and check if the workflow expires
            form_field_values_dict = inputData['form_field_values_dict']
            form_field_input_dict, form_field_values_dict = self.__get_form_field_input_dict(form_field_values_dict,
                                                                                             field_ids)

            condition = 'form_id="%s"' % form_id
            sql = self.create_select_sql(db_name, 'workflowTable', '*', condition)
            # print('workflowTable: ', sql)
            workflow_infos = self.execute_fetch_all(conn, sql)
            if not workflow_infos:
                data = response_code.ADD_DATA_FAIL
                data['msg'] = 'workflow not found'
                return data
            else:
                trigger_worfklow = self.__get_trigger_worflow(form_field_values_dict, workflow_infos)
            if not trigger_worfklow:
                data = response_code.ADD_DATA_FAIL
                data['msg'] = 'workflow not found'
                return data
            # print('trigger_worfklow: ', trigger_worfklow)
            stage_hash = prpcrypt.decrypt(trigger_worfklow['stage_hash'])
            old_id, last_time = stage_hash.split('||')
            # # print('id: ', old_id, form_id, int(old_id) == int(form_id))
            # # print('time: ', last_time, form_info['updated_time'], last_time == str(form_info['updated_time']))
            if int(old_id) != int(form_id) or last_time != str(form_info['updated_time']):
                data = response_code.ADD_DATA_FAIL
                data['msg'] = 'the workflow expired.'
                return data
            # # print('pass:', trigger_worfklow)
            # exit(0)
            # insert form index
            # approver_info = {'itemList': [{'id': 1}, {'id': 2}]}
            fields = ('creator_id', 'form_id', 'workspace_id')
            values = (creator_id, form_id, workspace_id)
            sql = self.create_insert_sql(db_name, 'inputFormIndexTable', '({})'.format(', '.join(fields)), values)
            # print('inputFormIndexTable sql:', sql)
            input_form_id = self.insert_exec(conn, sql, return_insert_id=True)
            # print('input_form_id:', input_form_id)
            now = str(datetime.datetime.today())
            # get approval info and workflow stages list
            fields_num = len(form_field_values_dict)
            workflow_id = trigger_worfklow['id']
            workflow_name = trigger_worfklow['workflow_name']
            workflow_stages_list = json.loads(trigger_worfklow['stages'])[1:]
            stages_num = len(workflow_stages_list)

            # get input form data and form's workflow stages list and approver stage
            input_form, workflow_stages_id_list, approver_info = self.__get_workflow_stages(
                workflow_stages_list,
                form_field_values_dict, input_form_id,
                form_id, workspace_id, db_name, conn)
            # # print('approver_info:', approver_info)
            # # print('workflow_stages_id_list:', workflow_stages_id_list)
            # exit(0)
            # add approval
            # create approval list
            approvers = self.__get_approvers(approver_info, input_form_id, form_id, workspace_id,
                                             form_field_values_dict, db_name, conn)

            # insert form details
            fields = ('id', 'workflow_id', 'workflow_name', 'fields_num', 'stages_num',
                      'form_status', 'form_field_values_dict', 'workflow_stages_id_list', 'create_time', 'updated_time')
            values = (input_form_id, workflow_id, workflow_name, fields_num, stages_num,
                      0, json.dumps(form_field_input_dict), json.dumps(workflow_stages_id_list), now, now)
            sql = self.create_insert_sql(db_name, 'inputFormTable', '({})'.format(', '.join(fields)), values)
            # print('inputFormTable sql:', sql)
            history_id = self.insert_exec(conn, sql, return_insert_id=True)

            # check dynamic field and insert
            fields = ('dynamic_field_id', 'option_label', 'using_form_id', 'using_input_form_id', 'create_time')
            for input_field_id in form_field_input_dict:
                if 'd' in input_field_id:
                    values = (input_field_id, form_field_input_dict[input_field_id]['value'],
                              form_id, input_form_id, now)
                    sql = self.create_insert_sql(db_name, 'dynamicField_to_inputFormTable',
                                                 '({})'.format(', '.join(fields)), values)
                    self.insert_exec(conn, sql)

            input_form['id'] = input_form_id
            input_form['history_id'] = history_id
            input_form['form_id'] = form_id
            input_form['approvers'] = approvers
            data = response_code.SUCCESS
            data['data'] = input_form

            return data
        except Exception as e:
            error = traceback.format_exc()
            # print(error)
            lg.error(error)
            data = response_code.ADD_DATA_FAIL
            data['msg'] = 'Something went wrong. Please double check your input.'
            return data
        finally:
            conn.close()

    def update_form_data(self, user_key, inputData, workspace_id, ):
        """
        :return:
        """
        conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            form_id = inputData['form_id']
            field_ids = inputData['field_ids']
            creator_id = user_key
            input_form_id = inputData['id']
            # do the form exist
            form_exist_flag = self.__check_table_id_exist(form_id, 'formTable', db_name, conn)
            if not form_exist_flag:
                data = response_code.ADD_DATA_FAIL
                data['msg'] = 'form not found'
                return data
            # do the user exist
            user_exist_flag = self.__check_table_id_exist(creator_id, 'userTable', db_name, conn)
            if not user_exist_flag:
                data = response_code.ADD_DATA_FAIL
                data['msg'] = 'user not found'
                return data
            # do the input form exist
            condition = 'id=%s' % form_id
            sql = self.create_select_sql(db_name, 'formTable', 'updated_time', condition=condition)
            form_info = self.execute_fetch_one(conn, sql)
            if not form_info:
                data = response_code.ADD_DATA_FAIL
                data['msg'] = 'form not found'
                return data

            # get workflow and check if the workflow expires
            form_field_values_dict = inputData['form_field_values_dict']
            form_field_input_dict, form_field_values_dict = self.__get_form_field_input_dict(form_field_values_dict,
                                                                                             field_ids)

            condition = 'form_id="%s"' % form_id
            sql = self.create_select_sql(db_name, 'workflowTable', '*', condition)
            # print('workflowTable: ', sql)
            workflow_infos = self.execute_fetch_all(conn, sql)
            if not workflow_infos:
                data = response_code.ADD_DATA_FAIL
                data['msg'] = 'workflow not found'
                return data
            else:
                trigger_worfklow = self.__get_trigger_worflow(form_field_values_dict, workflow_infos)
            if not trigger_worfklow:
                data = response_code.ADD_DATA_FAIL
                data['msg'] = 'workflow not found'
                return data
            # print('trigger_worfklow: ', trigger_worfklow)
            stage_hash = prpcrypt.decrypt(trigger_worfklow['stage_hash'])
            old_id, last_time = stage_hash.split('||')
            # # print('id: ', old_id, form_id, int(old_id) == int(form_id))
            # # print('time: ', last_time, form_info['updated_time'], last_time == str(form_info['updated_time']))
            if int(old_id) != int(form_id) or last_time != str(form_info['updated_time']):
                data = response_code.ADD_DATA_FAIL
                data['msg'] = 'the workflow expired.'
                return data

            fields_num = len(form_field_values_dict)
            workflow_id = trigger_worfklow['id']
            workflow_name = trigger_worfklow['workflow_name']
            workflow_stages_list = json.loads(trigger_worfklow['stages'])[1:]
            stages_num = len(workflow_stages_list)

            input_form, workflow_stages_id_list, approver_info = self.__get_workflow_stages(
                workflow_stages_list,
                form_field_values_dict, input_form_id,
                form_id, workspace_id, db_name, conn)
            # approver_info = {'itemList': [{'id': 1}, {'id': 2}]}
            now = str(datetime.datetime.today())
            # get approval
            approvers = self.__get_approvers(approver_info, input_form_id, form_id, workspace_id,
                                             form_field_values_dict, db_name, conn)

            # insert form details
            fields = ('id', 'workflow_id', 'workflow_name', 'fields_num', 'stages_num',
                      'form_status', 'form_field_values_dict', 'workflow_stages_id_list', 'create_time', 'updated_time')
            values = (input_form_id, workflow_id, workflow_name, fields_num, stages_num,
                      0, json.dumps(form_field_input_dict), json.dumps(workflow_stages_id_list), now, now)
            sql = self.create_insert_sql(db_name, 'inputFormTable', '({})'.format(', '.join(fields)), values)
            # print('inputFormTable sql:', sql)
            history_id = self.insert_exec(conn, sql, return_insert_id=True)
            input_form['id'] = input_form_id
            input_form['form_id'] = form_id
            input_form['history_id'] = history_id
            input_form['approvers'] = approvers
            data = response_code.SUCCESS
            data['data'] = input_form

            return data
        except Exception as e:
            error = traceback.format_exc()
            # print(error)
            return response_code.UPDATE_DATA_FAIL
        finally:
            conn.close()

    def __check_table_id_exist(self, table_id, table_name, db_name, conn):
        condition = 'id="%s"' % table_id
        sql = self.create_select_sql(db_name, table_name, '*', condition)
        # print('Table: ', sql)
        form_info = self.execute_fetch_all(conn, sql)
        if form_info:
            return True
        else:
            return False

    def __get_trigger_worflow(self, form_field_values_dict, workflow_infos):
        trigger_worfklow = None

        for workflow_info in workflow_infos:

            trigger_stage = json.loads(workflow_info['stages'])[0]
            workflow_conds = trigger_stage['condition']
            cond_length = len(workflow_conds)
            match_length = 0
            # print('workflow_conds: ', workflow_conds)
            for workflow_cond in workflow_conds:
                # # print('workflow_cond: ', workflow_cond)
                cond_id = workflow_cond['id']
                cond_type = workflow_cond['conditionType']
                cond_value = workflow_cond['value']
                # cond_type = int(workflow_cond['conditionType'])
                input_value = form_field_values_dict.get(cond_id, None)
                # get the condiction values
                if not input_value:
                    data = response_code.ADD_DATA_FAIL
                    data['msg'] = 'cannot find the condiction field: {}'.format(str(cond_id))
                    return data
                # if fill all the condiction
                if int(cond_type) == 0 and input_value == cond_value:
                    match_length += 1
                if int(cond_type) == 1 and input_value != cond_value:
                    match_length += 1
                if int(cond_type) == 2 and input_value >= cond_value:
                    match_length += 1
                if int(cond_type) == 3 and input_value <= cond_value:
                    match_length += 1
            if match_length == cond_length:
                trigger_worfklow = workflow_info
                break

        return trigger_worfklow

    def __get_form_field_input_dict(self, form_field_values_dict, field_ids):
        form_field_input_dict = {}
        for field_id in form_field_values_dict:
            field_style = field_ids[field_id]
            value = form_field_values_dict[field_id]
            try:
                value = json.loads(value)
                form_field_values_dict[field_id] = value
            except:
                pass
            # print(field_id, field_style, value)
            if field_style == 4:
                form_field_input_dict[field_id] = {'style': field_style, 'value': []}
                for file_path in value:
                    upload_blob(Config.DEFAULT_BUCEKT, file_path, file_path[2:])
                    # print('BUCEKT:', Config.DEFAULT_BUCEKT, file_path, file_path[2:])
                    form_field_input_dict[field_id]['value'].append(
                        'gs://{}/{}'.format(Config.DEFAULT_BUCEKT, file_path[2:]))
            else:
                form_field_input_dict[field_id] = {'style': field_style, 'value': value}
        return form_field_input_dict, form_field_values_dict

    def __get_workflow_stages(self, workflow_stages_list, form_field_values_dict, input_form_id, form_id, workspace_id,
                              db_name, conn):
        workflow_stages_info_list = []
        workflow_stages_id_list = []
        now = str(datetime.datetime.now())
        # print('workflow_stages_list:', workflow_stages_list)
        index = 0
        # exit(0)
        approver_info = None
        for stage_info in workflow_stages_list:
            if stage_info['flowType'] == 'Trigger':
                continue
            if stage_info['flowType'] == 'System' and stage_info['apiTaskName'] not in self.system_execute_tasks:
                continue
            elif stage_info['flowType'] == 'Approval':
                approver_info = stage_info
                continue
            else:
                index += 1
            condition_value = {}
            stage_id = stage_info['id']
            input_stage_info = [stage_id, index, stage_info['flowType'], stage_info['apiTaskName']]
            # # print('form_field_values_dict:', form_field_values_dict)
            for condition in stage_info['condition']:
                style = int(condition['style'])
                # # print('condition:', condition)
                para_name = condition['id']
                value = condition['value']
                if value in form_field_values_dict:
                    value = form_field_values_dict[value]
                else:
                    if style == 3:
                        value = Template(value)
                        value = value.safe_substitute(form_field_values_dict)
                    if style == 5:
                        value = form_field_values_dict[value]
                # # print(value)
                condition_value[para_name] = value
            # if stage_info['flowType'] == 'System' and stage_info['apiTaskName'] == 'system_define_field':
            #     condition_value['workspace_id'] = workspace_id
            #     condition_value['input_form_id'] = input_form_id
            #     option_label = condition_value['optionLabel']
            #     field_label = condition_value['FieldLabel']
            #     dynamic_field_relations = [{"table_name": "dynamicFieldValueTable",
            #                        "join_condition": "dynamicFieldTable.id=dynamicFieldValueTable.dynamic_field_id"},
            #                                ]
            #     dynamic_field_condition = "workspace_id=%s and option_label='%s'" % (workspace_id, option_label)
            #     fields = 'dynamicFieldTable.id'
            #     dynamic_field_query_sql = self.create_get_relation_sql(db_name, "dynamicFieldTable", fields, dynamic_field_relations,
            #                                                        condition=dynamic_field_condition)
            #     # print('dynamic_field_query_sql: ', dynamic_field_query_sql)
            #     # exit(0)
            #     dynamic_field_infos = self.execute_fetch_all(conn, dynamic_field_query_sql)
            #     if dynamic_field_infos:
            #         raise Exception("dynamic_field optionLabel always exist: {} in {}".format(option_label, field_label))
            input_stage_info.append(json.dumps(condition_value))
            input_stage_info.extend([now, now])
            workflow_stages_info_list.append(input_stage_info)
        # print('workflow_stages_info_list: ', workflow_stages_info_list)

        input_form = {'id': '', 'input_stage_id_list': [], 'form_id': form_id, 'history_id': ''}
        for input_stage_info in workflow_stages_info_list:
            fields = ('stage_id', 'stage_index', 'stage_group', 'apiTaskName', 'condition_value_dict',
                      'create_time', 'updated_time')
            values = tuple(input_stage_info)
            sql = self.create_insert_sql(db_name, 'inputStageTable', '({})'.format(', '.join(fields)), values)
            # # print('inputStageTable sql:', sql)
            input_stage_id = self.insert_exec(conn, sql, return_insert_id=True)
            input_form['input_stage_id_list'].append(input_stage_id)
            workflow_stages_id_list.append(input_stage_id)
        return input_form, workflow_stages_id_list, approver_info

    def __get_approvers(self, approver_info, input_form_id, form_id, workspace_id, form_field_values_dict, db_name,
                        conn):
        approvers = []
        self.__remove_approval(input_form_id)
        index = 1
        # De-duplication dict
        approval_dict = {}
        for approval_item in approver_info['condition']:
            approval_label = approval_item['label']
            # get workspace owner group
            if int(approval_item['id']) == 1:
                ad_groups = self.__get_workspace_owner_group(workspace_id, 'dg_group')
                # print('ad_groups:', ad_groups)
                for ad_group in ad_groups:
                    if ad_group not in approval_dict:
                        approval_dict[ad_group] = {'index': index, 'label_list': [approval_label]}
                    else:
                        approval_dict[ad_group]['label_list'].append(approval_label)
                    # self.__add_approval(input_form_id, index, ad_group, approval_label)
                approvers.append(ad_groups)
                if ad_groups:
                    index += 1
            # get region group, default id=s1
            elif int(approval_item['id']) == 2:
                region = form_field_values_dict.get('s1', None)
                ad_groups = self.__get_workspace_region_group(workspace_id, region)
                # print('ad_groups:', ad_groups)
                for ad_group in ad_groups:
                    if ad_group not in approval_dict:
                        approval_dict[ad_group] = {'index': index, 'label_list': [approval_label]}
                    else:
                        approval_dict[ad_group]['label_list'].append(approval_label)
                    # self.__add_approval(input_form_id, index, ad_group, approval_label)
                approvers.append(ad_groups)
                if ad_groups:
                    index += 1
            # get dynamic field group
            elif int(approval_item['id']) == 3:
                field = approval_item['value']
                field_id = field.replace('d', '').strip()
                option_label = form_field_values_dict.get(field, None)
                relations = [
                    {"table_name": "dynamicFieldTable",
                     "join_condition": "dynamicFieldValueTable.dynamic_field_id=dynamicFieldTable.id"}]
                condition = "dynamicFieldTable.id=%s and option_label='%s' and workspace_id='%s'" % (
                    field_id, option_label, workspace_id)
                sql = self.create_get_relation_sql(db_name, 'dynamicFieldValueTable',
                                                   'dynamicFieldTable.id, option_value',
                                                   relations, condition)
                print('dynamicFieldTable sql:', sql)
                dynamic_field_info = self.execute_fetch_one(conn, sql)

                # print('ad_group:', ad_group)
                if dynamic_field_info:
                    ad_group = dynamic_field_info['option_value']
                    if ad_group not in approval_dict:
                        approval_dict[ad_group] = {'index': index, 'label_list': [approval_label]}
                    else:
                        approval_dict[ad_group]['label_list'].append(approval_label)
                    # self.__add_approval(input_form_id, index, ad_group, approval_label)
                    approvers.append([ad_group])
                    index += 1
            # get usecase data linear group
            elif int(approval_item['id']) == 5:
                ad_groups = self.__get_data_linear_approval(form_field_values_dict, workspace_id)
                # print('ad_group:', ad_group)
                for ad_group in ad_groups:
                    if ad_group not in approval_dict:
                        approval_dict[ad_group] = {'index': index, 'label_list': [approval_label]}
                    else:
                        approval_dict[ad_group]['label_list'].append(approval_label)
                    # self.__add_approval(input_form_id, index, ad_group, approval_label)
                    index += 1
                    approvers.append([ad_group])

            # get policy tags ad group
            elif int(approval_item['id']) == 6:
                ad_groups = self.__get_policy_tags_approval(form_field_values_dict, workspace_id)
                # print('ad_group:', ad_group)
                for ad_group in ad_groups:
                    if ad_group not in approval_dict:
                        approval_dict[ad_group] = {'index': index, 'label_list': [approval_label]}
                    else:
                        approval_dict[ad_group]['label_list'].append(approval_label)
                    # self.__add_approval(input_form_id, index, ad_group, approval_label)
                    index += 1
                    approvers.append([ad_group])
            # get policy tags ad group
            elif int(approval_item['id']) == 0:
                ad_groups = self.__get_data_approval(form_field_values_dict, workspace_id, form_id)
                # print('ad_group:', ad_group)
                for ad_group in ad_groups:
                    if ad_group not in approval_dict:
                        approval_dict[ad_group] = {'index': index, 'label_list': [approval_label]}
                    else:
                        approval_dict[ad_group]['label_list'].append(approval_label)
                    # self.__add_approval(input_form_id, index, ad_group, approval_label)
                    index += 1
                    approvers.append([ad_group])
        for approval_ad_group in approval_dict:
            approval_index = approval_dict[approval_ad_group]['index']
            label_set = set(approval_dict[approval_ad_group]['label_list'])
            label = ','.join(label_set)
            self.__add_approval(input_form_id, approval_index, approval_ad_group, label)
        # print('approvers:', approvers)
        return approvers

    def __get_data_linear_approval(self, form_field_values_dict, workspace_id):
        conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            dy_condition = "form_id=%s" % (status.system_form_id['usecase'])
            sql = self.create_select_sql(db_name, 'dynamicFieldTable',
                                         'id,label',
                                         condition=dy_condition)
            print('dynamicFieldTable sql:', sql)
            field_info = self.execute_fetch_one(conn, sql)
            print('dynamicFieldTable field_info:', field_info)
            dy_field_id = 'd' + str(field_info['id'])
            form_dy_field_label = form_field_values_dict.get(dy_field_id, None)
            ad_groups = []
            if form_dy_field_label:
                dy_value_cond = "dynamic_field_id='%s' and option_label='%s' and using_form_id=%s" % (dy_field_id,
                                                                                                      form_dy_field_label,
                                                                                                      status.system_form_id[
                                                                                                          'data_access'])
                sql = self.create_select_sql(db_name, 'dynamicField_to_inputFormTable', 'id, using_input_form_id',
                                             condition=dy_value_cond)
                print('dynamicField_to_inputFormTable sql:', sql)
                using_input_form_id_infos = self.execute_fetch_all(conn, sql)
                using_input_form_id_list = [str(item['using_input_form_id']) for item in using_input_form_id_infos]
                print('using_input_form_id_list:', using_input_form_id_list)
                apporval_condition = "input_form_id in (%s)" % ''.join(using_input_form_id_list)
                sql = self.create_select_sql(db_name, 'approvalTable',
                                             'id,ad_group',
                                             condition=apporval_condition)
                print('approvalTable sql:', sql)
                approval_infos = self.execute_fetch_all(conn, sql)
                ad_group_set = set([item['ad_group'] for item in approval_infos])
                print('approvalTable ad_group_set:', ad_group_set)
                ad_groups = list(ad_group_set)
            return ad_groups
        except Exception as e:
            lg.error(e)
            return []
        finally:
            conn.close()

    def __get_policy_tags_approval(self, form_field_values_dict, workspace_id):
        conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            dy_condition = "form_id=%s" % (status.system_form_id['usecase'])
            sql = self.create_select_sql(db_name, 'dynamicFieldTable',
                                         'id,label',
                                         condition=dy_condition)
            print('dynamicFieldTable sql:', sql)
            field_info = self.execute_fetch_one(conn, sql)
            print('dynamicFieldTable field_info:', field_info)
            dy_field_id = 'd' + str(field_info['id'])
            form_dy_field_label = form_field_values_dict.get(dy_field_id, None)
            ad_groups = []
            if form_dy_field_label:
                dy_value_cond = "dynamic_field_id='%s' and option_label='%s' and using_form_id=%s" % (dy_field_id,
                                                                                                      form_dy_field_label,
                                                                                                      status.system_form_id[
                                                                                                          'data_access'])
                sql = self.create_select_sql(db_name, 'dynamicField_to_inputFormTable', 'id, using_input_form_id',
                                             condition=dy_value_cond)
                print('dynamicField_to_inputFormTable sql:', sql)
                using_input_form_id_infos = self.execute_fetch_all(conn, sql)
                using_input_form_id_list = [str(item['using_input_form_id']) for item in using_input_form_id_infos]
                print('using_input_form_id_list:', using_input_form_id_list)
                apporval_condition = "input_form_id in (%s)" % ''.join(using_input_form_id_list)
                sql = self.create_select_sql(db_name, 'approvalTable',
                                             'id,ad_group',
                                             condition=apporval_condition)
                print('approvalTable sql:', sql)
                approval_infos = self.execute_fetch_all(conn, sql)
                ad_group_set = set([item['ad_group'] for item in approval_infos])
                print('approvalTable ad_group_set:', ad_group_set)
                ad_groups = list(ad_group_set)
            return ad_groups
        except Exception as e:
            lg.error(e)
            return []
        finally:
            conn.close()

    def __get_data_approval(self, form_field_values_dict, workspace_id, form_id):
        conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            ad_groups = []
            project_id = ''
            location = ''
            dataset_id = ''
            table_id = ''
            if form_id == status.system_form_id['data_ob']:
                project_id = form_field_values_dict.get(status.system_form_field_id['data_ob']['project_id'], '')
                location = form_field_values_dict.get(status.system_form_field_id['data_ob']['location'], '')
                dataset_id = form_field_values_dict.get(status.system_form_field_id['data_ob']['dataset_id'], '')
                table_id = form_field_values_dict.get(status.system_form_field_id['data_ob']['table_id'], '')
            elif form_id == status.system_form_id['data_access']:
                project_id = form_field_values_dict.get(status.system_form_field_id['data_access']['project_id'], '')
                location = form_field_values_dict.get(status.system_form_field_id['data_access']['location'], '')
                dataset_id = form_field_values_dict.get(status.system_form_field_id['data_access']['dataset_id'], '')
                table_id = form_field_values_dict.get(status.system_form_field_id['data_access']['table_id'], '')
            dy_condition = "workspace_id='%s' and project_id='%s' and location='%s' and dataset_id='%s' and table_id='%s'" % (
            workspace_id, project_id, location, dataset_id, table_id)
            sql = self.create_select_sql(db_name, 'dataOnboardTable',
                                         'input_form_id,data_owner',
                                         condition=dy_condition)
            print('dataOnboardTable sql:', sql)
            data_info = self.execute_fetch_one(conn, sql)
            print('data_info:', data_info)
            if data_info:
                ad_group = data_info['data_owner']
                if ad_group:
                    ad_groups.append(ad_group)

            return ad_groups
        except Exception as e:
            lg.error(e)
            return []
        finally:
            conn.close()


input_form_mgr = DbInputFormMgr()
