#!/usr/bin/python
# -*- coding: UTF-8 -*

from string import Template
from utils.airflow_helper import system_approval
from db.gcp.task_operator import taskFetcher
from config import configuration
from db.base import DbBase
from db.connection_pool import MysqlConn
import json
from utils.status_code import response_code
from utils.ldap_helper import Ldap
import datetime
import traceback
from common.common_input_form_status import status as Status
from common.common_crypto import prpcrypt
import os
from config import config
import logging
import re

logger = logging.getLogger("main." + __name__)
config_name = os.getenv('FLASK_CONFIG') or 'default'
Config = config[config_name]
email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

class DbGovernanceMgr(DbBase):

    status = Status.code
    status_history_mapping = Status.status_history_mapping

    def __check_table_id_exist(self, table_id, table_name, db_name, conn):
        condition = 'id="%s"' % table_id
        sql = self.create_select_sql(db_name, table_name, '*', condition)
        logger.debug("FN:__check_table_id_exist {}_sql:{}".format(table_name, sql))
        form_info = self.execute_fetch_all(conn, sql)
        if form_info:
            return True
        else:
            return False

    def __get_adgroup_member(self, ad_group):
        return []
    
    # change inputform status
    def change_status(self, user_key, account_id, workspace_id, inputData, system_approval_flag=False, no_approval=False):
        conn = MysqlConn()
        db_name = configuration.get_database_name()

        try:

            miss_role_list = []
            # 1.get the approver's ad_group from ldap
            # if it is the system approval task
            if not system_approval_flag:
                checking_list = Ldap.get_member_ad_group(account_id, Status.offline_flag)
                # notice_ids = [account_id]
            else:
                checking_list = []
            notice_ids = []
            #  2.Also put the approver's email into the checking group
            checking_list.append(account_id)
            logger.debug("FN:change_status checking_list:{}".format(checking_list))
            # 2.get inputform id
            # do the form exists
            input_form_id = inputData['id']

            # 2.add user and input form owner to notify list
            relations = [
                {"table_name": "userTable", "join_condition": "userTable.ID=inputFormIndexTable.creator_id"}]
            input_form_cond = "inputFormIndexTable.id='%s'" % input_form_id
            sql = self.create_get_relation_sql(db_name, 'inputFormIndexTable', 'userTable.ACCOUNT_ID', relations=relations, condition=input_form_cond)
            logger.debug("FN:change_status userTable_join_inputFormIndexTable_sql:{}".format(sql))
            user_info = self.execute_fetch_one(conn, sql)
            if user_info:
                notice_ids.append(user_info['ACCOUNT_ID'])

            now = str(datetime.datetime.now())
            form_status = self.status.get(int(inputData['form_status']), None)
            comment = inputData.get('comment', '')
            if not form_status:
                data = response_code.UPDATE_DATA_FAIL
                data['data'] = {}
                data['data']['notice_ids'] = notice_ids
                data['msg'] = 'cannot find the status.'


            form_status_code = int(inputData['form_status'])

            input_form_condition = 'id="%s" order by history_id desc' % (input_form_id)
            sql = self.create_select_sql(db_name, 'inputFormTable', '*', input_form_condition)
            logger.debug("FN:change_status inputFormTable_sql:{}".format(sql))
            form_infos = self.execute_fetch_all(conn, sql)
            if not form_infos:
                data = response_code.ADD_DATA_FAIL
                data['data'] = {}
                data['data']['notice_ids'] = notice_ids
                data['msg'] = 'form not found'
                data['data']['history_id'] = ''
                return data
            # do the user exist
            creator_id = user_key
            user_exist_flag = self.__check_table_id_exist(creator_id, 'userTable', db_name, conn)
            if not user_exist_flag:
                data = response_code.ADD_DATA_FAIL
                data['data'] = {}
                data['data']['notice_ids'] = notice_ids
                data['msg'] = 'user not found'
                data['data']['history_id'] = ''
                return data
            # get history id
            history_id = form_infos[0]['history_id']
            # sign the comment
            comment = str(comment)
            if comment != '':
                if form_status_code == Status.approved:
                    comment = '[|{}|]'.format(Status.approved)+comment
                elif form_status_code == Status.rejected:
                    comment = '[|{}|]'.format(Status.rejected)+comment
                history_id = history_id
                now = str(datetime.datetime.now())
                fields = ('input_form_id', 'history_id', 'creator_id', 'comment', 'create_time')
                values = (input_form_id, history_id, user_key, comment, now)
                sql = self.create_insert_sql(db_name, 'inputCommentTable', '({})'.format(', '.join(fields)), values)
                logger.debug("FN:change_status inputCommentTable_sql:{}".format(sql))
                comment_id = self.insert_exec(conn, sql, return_insert_id=True)

            # check the approval condition
            if form_status_code not in (Status.completed, Status.pending_approval):
                approval_condition = "input_form_id='%s' and now_approval=1 and ad_group in ('%s')" % (input_form_id, "', '".join(checking_list))
                sql = self.create_select_sql(db_name, 'approvalTable', '*', approval_condition)
                logger.debug("FN:change_status approvalTable_sql:{}".format(sql))
                approval_infos = self.execute_fetch_all(conn, sql)

                # if the workflow have approval flow but user not in approval list
                if (not approval_infos and not no_approval):
                    print('no approval flag:', no_approval, (not approval_infos and not no_approval), approval_infos)
                    data = response_code.UPDATE_DATA_FAIL
                    data['data'] = {}
                    data['data']['notice_ids'] = notice_ids
                    data['msg'] = 'You are not in the approval ad group.'
                    data['data']['history_id'] = history_id
                    return data
                elif approval_infos:
                    now_approval_num = int(approval_infos[0]['approval_num'])
                    next_approval_num = now_approval_num + 1
                else:
                    now_approval_num = 0
                    next_approval_num = now_approval_num + 1

                if form_status_code == Status.approved:
                    # 3.change approval process
                    all_approval_flag = 0
                    miss_role_flag = 0

                    # if it is the last approval
                    approval_condition = "input_form_id='%s' and approval_num=%s" % (input_form_id, next_approval_num)
                    sql = self.create_select_sql(db_name, 'approvalTable', '*', approval_condition)
                    logger.debug("FN:change_status approvalTable_sql:{}".format(sql))
                    last_approval_info = self.execute_fetch_one(conn, sql)
                    # if cannot find the next approval task, is the last approval status
                    if not last_approval_info:
                        all_approval_flag = 1

                    # if it is the last approval, check the service account have enough right to execute the tasks
                    gcp_tasks = []
                    if all_approval_flag == 1:
                        workflow_stages_id_list = json.loads(form_infos[0]['workflow_stages_id_list'], strict=False)
                        workflow_stages_id_list = (str(id) for id in workflow_stages_id_list)
                        logger.debug("FN:change_status workflow_stages_id_list:{}".format(workflow_stages_id_list))
                        input_stage_condition = "id in ('%s') order by stage_index" % ("', '".join(workflow_stages_id_list))
                        sql = self.create_select_sql(db_name, 'inputStageTable', 'id,apiTaskName,condition_value_dict',
                                                     input_stage_condition)
                        logger.debug("FN:change_status inputStageTable_list:{}".format(sql))
                        stage_infos = self.execute_fetch_all(conn, sql)
                        tasks = []
                        for stage_info in stage_infos:
                            tasks.append({'id': stage_info['id'], 'name': stage_info['apiTaskName'],
                                          "stages": json.loads(stage_info['condition_value_dict'], strict=False)})
                        logger.debug("FN:change_status project_id:{} service_account:{}".format(taskFetcher.project_id, taskFetcher.service_account))
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
                                    miss_role_list.append('-- '+task_name+': ['+', '.join(task.role_list)+']')
                        if len(miss_role_list) != 0:
                            miss_role_flag = 1
                    # have all the gcp permission or it is not the last approval, approved successful
                    if miss_role_flag == 0:
                        # change approval status
                        fields = ('now_approval', 'is_approved', 'account_id', 'comment', 'updated_time')
                        values = (0, 1, account_id, comment, now)
                        approval_condition = "input_form_id='%s' and now_approval=1 and approval_num=%s and ad_group in ('%s')" % (input_form_id,
                                                                                                                                   now_approval_num,
                                                                                                                                   "', '".join(checking_list)
                                                                                                                                   )
                        # approval_condition = "input_form_id='%s' and now_approval=1 and ad_group in ('%s')" % (input_form_id, "', '".join(checking_list))
                        sql = self.create_update_sql(db_name, 'approvalTable', fields, values, approval_condition)
                        logger.debug("FN:change_status approvalTable_sql:{}".format(sql))
                        return_count = self.updete_exec(conn, sql)
                        if (return_count == 0 and not no_approval):
                            data = response_code.SUCCESS
                            data['data'] = {}
                            data['data']['notice_ids'] = notice_ids
                            data['msg'] = 'the %s level approval task has already been approved.' % now_approval_num
                            data['msg'] += '\n URL: ' + Config.FRONTEND_URL + '/app/approvalFlow?id=%s' % input_form_id

                            data['data']['history_id'] = history_id
                            return data
                        # close all the same num approval task
                        fields = ('now_approval', 'is_approved', 'comment', 'updated_time')
                        values = (0, 0, 'this approval num has been approved', now)
                        approval_condition = "input_form_id='%s' and now_approval=1 and approval_num=%s" % (input_form_id, now_approval_num)
                        # approval_condition = "input_form_id='%s' and now_approval=1 and ad_group in ('%s')" % (input_form_id, "', '".join(checking_list))
                        sql = self.create_update_sql(db_name, 'approvalTable', fields, values, approval_condition)
                        logger.debug("FN:change_status approvalTable_sql:{}".format(sql))
                        _ = self.updete_exec(conn, sql)

                        # next approval task
                        fields = ('now_approval', 'is_approved')
                        values = (1, 0)
                        approval_condition = "input_form_id='%s' and approval_num=%s" % (input_form_id, next_approval_num)
                        sql = self.create_select_sql(db_name, 'approvalTable', '*', condition=approval_condition)
                        logger.debug("FN:change_status next_approvalTable_sql:{}".format(sql))
                        next_approval_items = self.execute_fetch_all(conn, sql)
                        # notify next adgroup approvers
                        next_adgroup = []
                        # check if it is system approval task
                        system_approval_trigger_flag = 0
                        for next_approval_item in next_approval_items:
                            try:
                                ad_group = next_approval_item['ad_group']
                                try:
                                    _ = prpcrypt.decrypt(ad_group)
                                except:
                                    next_adgroup.append(ad_group)

                            except:
                                ad_group = []
                                # print('FN:next approval group:', ad_group)
                            # next_adgroup.append(ad_group)
                            if next_approval_item and next_approval_item['label'] == 'System approval':
                                try:
                                    token = next_approval_item['ad_group']
                                    if(re.fullmatch(email_regex, token)):
                                        pass
                                    else:
                                        # This is a valid token format, not an ADgroup
                                        token_json = prpcrypt.decrypt(token)
                                        logger.debug("FN:change_status airflow_token:{} airflow_token_json:{}".format(token, token_json))
                                        input_form_id, form_id, approval_order, time = token_json.split('||')
                                        retry = 0
                                        while retry < 3:
                                            return_flag = system_approval(token, input_form_id, form_id,
                                                                        workspace_id, approval_order)
                                            if not return_flag:
                                                retry += 1
                                                # time.sleep(1)
                                            else:
                                                break
                                except:
                                    logger.error("FN:change_status error:{}".format(traceback.format_exc()))

                        sql = self.create_update_sql(db_name, 'approvalTable', fields, values, approval_condition)
                        logger.debug("FN:change_status approvalTable_sql:{}".format(sql))
                        return_count = self.updete_exec(conn, sql)
                        logger.debug("FN:change_status return_count:{}".format(return_count))
                        # modify successfully, can send the email
                        logger.debug("FN:change_status notice_ids:{}".format(notice_ids))

                        for ad_group in next_adgroup:
                            member_list, _ = Ldap.get_ad_group_member(ad_group)
                            if member_list:
                                notice_ids.extend(member_list)
                        logger.debug("FN:change_status next_notice_ids:{}".format(notice_ids))
                        if (return_count != 0 and not no_approval):
                            all_approval_flag = 0

                        # 4.change status
                        # insert form
                        if all_approval_flag == 1:

                            form_status_code = Status.in_porgress
                            fields = ('form_status', 'updated_time')
                            values = (form_status_code, now)
                            update_condition = 'id="%s" and history_id="%s" ' % (input_form_id, history_id)
                            sql = self.create_update_sql(db_name, 'inputFormTable', fields, values, update_condition)
                            logger.debug("FN:change_status update_inputFormTable_sql:{}".format(sql))
                            return_count = self.updete_exec(conn, sql)

                            # checking_list = self.__get_adgroup_member(notice_ids)
                            data = response_code.SUCCESS
                            data['data'] = {'id': input_form_id, 'count': return_count, 'tasks': tasks,
                                            'gcp_tasks': gcp_tasks, 'is_approved': all_approval_flag}
                            data['msg'] = 'The input form is finished.'
                        else:
                            data = response_code.SUCCESS
                            data['msg'] = 'approved successfully, waiting for next approval: {}'.format(', '.join(next_adgroup))
                            # return data
                    else:
                        data = response_code.UPDATE_DATA_FAIL
                        data['msg'] = 'Your form\'s tasks miss one of roles of each tasks:\n{}\nPlease find IT support.'.format('\n'.join(miss_role_list))
                    if 'data' not in data:
                        data['data'] = {}
                    data['data']['notice_ids'] = list(set(notice_ids))
                    data['data']['history_id'] = history_id
                    return data
                elif form_status_code in (Status.rejected, Status.cancelled, Status.failed):
                    # update status
                    fields = ('now_approval', 'is_approved', 'account_id', 'comment', 'updated_time')
                    values = (0, 0, account_id, comment, now)
                    approval_condition = "input_form_id='%s' and now_approval=1 and approval_num=%s and ad_group in ('%s')" % (input_form_id,
                                                                                                                               now_approval_num,
                                                                                                                               "', '".join(checking_list))
                    sql = self.create_update_sql(db_name, 'approvalTable', fields, values, approval_condition)
                    logger.debug("FN:change_status rejected_approvalTable_sql:{}".format(sql))
                    return_count = self.updete_exec(conn, sql)
                    if return_count == 0:
                        data = response_code.SUCCESS
                        data['data']['notice_ids'] = notice_ids
                        data['msg'] = 'the %s level approval task has already been changed.' % now_approval_num
                        data['data']['history_id'] = history_id
                        return data
                    # close the other same level task
                    fields = ('now_approval', 'is_approved', 'comment', 'updated_time')
                    values = (0, 0, 'this approval num has been modified', now)
                    approval_condition = "input_form_id='%s' and approval_num=%s and now_approval=1" % (input_form_id, now_approval_num)
                    # approval_condition = "input_form_id='%s' and now_approval=1 and ad_group in ('%s')" % (input_form_id, "', '".join(checking_list))
                    sql = self.create_update_sql(db_name, 'approvalTable', fields, values, approval_condition)
                    logger.debug("FN:change_status update_approvalTable_sql:{}".format(sql))
                    _ = self.updete_exec(conn, sql)
                    # changes inputform status
                    fields = ('form_status', 'updated_time')
                    values = (form_status_code, now)
                    update_condition = 'id="%s" and history_id="%s" ' % (input_form_id, history_id)
                    sql = self.create_update_sql(db_name, 'inputFormTable', fields, values, update_condition)
                    logger.debug("FN:change_status update_inputFormTable_sql:{}".format(sql))
                    return_count = self.updete_exec(conn, sql)
                    data = response_code.SUCCESS
                    data['msg'] = 'update form status to: ' + form_status
                else:
                    data = response_code.UPDATE_DATA_FAIL
                    data['msg'] = 'Does not support this status option.'
                if 'data' not in data:
                    data['data'] = {}
                data['data']['notice_ids'] = notice_ids
            elif form_status_code == Status.pending_approval:
                fields = ('now_approval', 'is_approved', 'account_id', 'comment', 'updated_time')
                values = (0, 0, None, '', None)
                approval_condition = "input_form_id='%s' and approval_num!=1" % (input_form_id)
                sql = self.create_update_sql(db_name, 'approvalTable', fields, values, approval_condition)
                logger.debug("FN:change_status pending_approvalTable_sql:{}".format(sql))
                _ = self.updete_exec(conn, sql)

                fields = ('now_approval', 'is_approved', 'account_id', 'comment', 'updated_time')
                values = (1, 0, None, '', None)
                approval_condition = "input_form_id='%s' and approval_num=1 " % (input_form_id)
                # approval_condition = "input_form_id='%s' and approval_num=1 and ad_group in ('%s')" % (input_form_id, "', '".join(checking_list))
                sql = self.create_update_sql(db_name, 'approvalTable', fields, values, approval_condition)
                logger.debug("FN:change_status update_approvalTable_sql:{}".format(sql))
                _ = self.updete_exec(conn, sql)

                # changes inputform stauts
                fields = ('form_status', 'updated_time')
                values = (form_status_code, now)
                update_condition = 'id="%s" and history_id="%s" ' % (input_form_id, history_id)
                sql = self.create_update_sql(db_name, 'inputFormTable', fields, values, update_condition)
                logger.debug("FN:change_status update_inputFormTable_sql:{}".format(sql))
                _ = self.updete_exec(conn, sql)
                data = response_code.SUCCESS
                data['msg'] = 'update form status to: ' + form_status
                if 'data' not in data:
                    data['data'] = {}
                data['data']['notice_ids'] = notice_ids
            else:
                # change status
                fields = ('now_approval', 'is_approved', 'account_id', 'comment', 'updated_time')
                values = (0, 0, account_id, comment, now)
                approval_condition = "input_form_id='%s' and now_approval=1" % (input_form_id)
                sql = self.create_update_sql(db_name, 'approvalTable', fields, values, approval_condition)
                logger.debug("FN:change_status complete_approvalTable_sql:{}".format(sql))
                return_count = self.updete_exec(conn, sql)
                # if return_count == 0:
                #     data = response_code.SUCCESS
                #     data['msg'] = 'the %s level approval task has already been changed.' % now_approval_num
                #     return data
                # # close the other same level task
                # fields = ('now_approval', 'is_approved', 'comment', 'updated_time')
                # values = (0, 0, 'this approval num has been modified', now)
                # approval_condition = "input_form_id='%s' and now_approval=1" % (input_form_id)
                # # approval_condition = "input_form_id='%s' and now_approval=1 and ad_group in ('%s')" % (input_form_id, "', '".join(checking_list))
                # sql = self.create_update_sql(db_name, 'approvalTable', fields, values, approval_condition)
                # # # print('approvalTable update_sql: ', sql)
                # _ = self.updete_exec(conn, sql)
                # update input form task
                fields = ('form_status', 'updated_time')
                values = (form_status_code, now)
                update_condition = 'id="%s" and history_id="%s" ' % (input_form_id, history_id)
                sql = self.create_update_sql(db_name, 'inputFormTable', fields, values, update_condition)
                logger.debug("FN:change_status update_inputFormTable_sql:{}".format(sql))
                _ = self.updete_exec(conn, sql)
                data = response_code.SUCCESS
                data['msg'] = 'update form status to: ' + form_status
                if 'data' not in data:
                    data['data'] = {}
                data['data']['notice_ids'] = notice_ids
            if 'data' not in data:
                data['data'] = {}
            if 'notice_ids' not in data['data']:
                data['data']['notice_ids'] = []
            data['data']['id'] = input_form_id
            data['data']['history_id'] = history_id
            return data

        except Exception as e:
            logger.error("FN:change_status error:{}".format(traceback.format_exc()))
            return response_code.GET_DATA_FAIL
        finally:
            conn.close()


    # get admin info
    def get_admin_user_info(self):

        conn = MysqlConn()
        db_name = configuration.get_database_name()

        try:
            condition = 'ID=1'
            sql = self.create_select_sql(db_name, 'userTable', '*', condition)
            logger.debug("FN:get_admin_user_info userTable_sql:{}".format(sql))
            admin_info = self.execute_fetch_one(conn, sql)
            return admin_info
        except Exception as e:
            logger.error("FN:change_status error:{}".format(traceback.format_exc()))
            return {}
        finally:
            conn.close()
            
    # system approve
    def system_approval_trigger(self, user_key, account_id, inputData):
        conn = MysqlConn()
        db_name = configuration.get_database_name()

        try:
            notice_ids = []
            miss_role_list = []
            token = inputData.get('token', '')
            logger.debug("FN:system_approval_trigger inputData_token:{}".format(token))
            token_json = json.loads(prpcrypt.decrypt(token), strict=False)
            token = token_json.get('token', '||ERROR_TOKEN||')
            # do the form exists
            input_form_id = inputData.get('input_form_id', '-1')
            comment = 'system approval'
            # 2.add user and input form owner to notify list
            relations = [
                {"table_name": "userTable", "join_condition": "userTable.ID=inputFormIndexTable.creator_id"}]
            input_form_cond = "inputFormIndexTable.id='%s'" % input_form_id
            sql = self.create_get_relation_sql(db_name, 'inputFormIndexTable', 'userTable.ACCOUNT_ID', relations=relations, condition=input_form_cond)
            user_info = self.execute_fetch_one(conn, sql)
            if user_info:
                notice_ids.append(user_info['ACCOUNT_ID'])

            now = str(datetime.datetime.now())
            input_form_condition = 'id="%s" order by history_id desc' % (input_form_id)
            sql = self.create_select_sql(db_name, 'inputFormTable', '*', input_form_condition)
            logger.debug("FN:system_approval_trigger inputFormTable_sql:{}".format(sql))
            form_infos = self.execute_fetch_all(conn, sql)
            if not form_infos:
                data = response_code.ADD_DATA_FAIL
                data['data'] = {}
                data['data']['notice_ids'] = notice_ids
                data['msg'] = 'form not found'
                data['data']['history_id'] = ''
                return data

            # get history id
            history_id = form_infos[0]['history_id']
            # check the approval condition
            approval_condition = "input_form_id='%s' and now_approval=1 and ad_group='%s'" % (input_form_id, token)
            sql = self.create_select_sql(db_name, 'approvalTable', '*', approval_condition)
            logger.debug("FN:system_approval_trigger approvalTable_sql:{}".format(sql))
            approval_infos = self.execute_fetch_all(conn, sql)
            if not approval_infos:
                data = response_code.UPDATE_DATA_FAIL
                data['data'] = {}
                data['data']['notice_ids'] = notice_ids
                data['msg'] = 'Airflow trigger failed, token error.'
                data['data']['history_id'] = history_id
                return data
            now_approval_num = int(approval_infos[0]['approval_num'])
            next_approval_num = now_approval_num + 1

            # 3hange approval process
            all_approval_flag = 0
            miss_role_flag = 0

            # if it is the last approval
            approval_condition = "input_form_id='%s' and approval_num=%s" % (input_form_id, next_approval_num)
            sql = self.create_select_sql(db_name, 'approvalTable', '*', approval_condition)
            logger.debug("FN:system_approval_trigger check_last_approvalTable_sql:{}".format(sql))
            last_approval_info = self.execute_fetch_one(conn, sql)
            # if cannot find the next approval task, is the last approval status
            if not last_approval_info:
                all_approval_flag = 1

            # if it is the last approval, check the service account have enough right to execute the tasks
            gcp_tasks = []
            if all_approval_flag == 1:
                workflow_stages_id_list = json.loads(form_infos[0]['workflow_stages_id_list'], strict=False)
                workflow_stages_id_list = (str(id) for id in workflow_stages_id_list)
                logger.debug("FN:system_approval_trigger workflow_stages_id_list:{}".format(workflow_stages_id_list))
                input_stage_condition = "id in ('%s') order by stage_index" % ("', '".join(workflow_stages_id_list))
                sql = self.create_select_sql(db_name, 'inputStageTable', 'id,apiTaskName,condition_value_dict',
                                             input_stage_condition)
                logger.debug("FN:system_approval_trigger inputStageTable_sql:{}".format(sql))
                stage_infos = self.execute_fetch_all(conn, sql)
                tasks = []
                for stage_info in stage_infos:
                    tasks.append({'id': stage_info['id'], 'name': stage_info['apiTaskName'],
                                  "stages": json.loads(stage_info['condition_value_dict'], strict=False)})
                logger.debug("FN:system_approval_trigger project_id:{} service_account:{}".format(taskFetcher.project_id, taskFetcher.service_account))
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
                            miss_role_list.append('-- '+task_name+': ['+', '.join(task.role_list)+']')
                if len(miss_role_list) != 0:
                    miss_role_flag = 1
            # have all the gcp permission or it is not the last approval, approved successful
            if miss_role_flag == 0 or all_approval_flag == 0:
                # change approval status
                fields = ('now_approval', 'is_approved', 'account_id', 'comment', 'updated_time')
                values = (0, 1, account_id, comment, now)
                approval_condition = "input_form_id='%s' and now_approval=1 and approval_num=%s and ad_group='%s'" % (input_form_id,
                                                                                                                           now_approval_num,
                                                                                                                           token)
                # approval_condition = "input_form_id='%s' and now_approval=1 and ad_group in ('%s')" % (input_form_id, "', '".join(checking_list))
                sql = self.create_update_sql(db_name, 'approvalTable', fields, values, approval_condition)
                # # print('approvalTable update_sql: ', sql)
                logger.debug("FN:system_approval_trigger success_update_approvalTable_sql:{}".format(sql))
                return_count = self.updete_exec(conn, sql)
                if return_count == 0:
                    data = response_code.SUCCESS
                    data['data'] = {}
                    data['data']['notice_ids'] = notice_ids
                    data['msg'] = 'the %s level approval task has already been approved.' % now_approval_num
                    data['data']['history_id'] = history_id
                    return data
                # close all the same num approval task
                fields = ('now_approval', 'is_approved', 'comment', 'updated_time')
                values = (0, 0, 'this approval num has been approved', now)
                approval_condition = "input_form_id='%s' and now_approval=1 and approval_num=%s" % (input_form_id, now_approval_num)
                # approval_condition = "input_form_id='%s' and now_approval=1 and ad_group in ('%s')" % (input_form_id, "', '".join(checking_list))
                sql = self.create_update_sql(db_name, 'approvalTable', fields, values, approval_condition)
                logger.debug("FN:system_approval_trigger close_same_num_update_approvalTable_sql:{}".format(sql))
                _ = self.updete_exec(conn, sql)

                # next approval task
                fields = ('now_approval', 'is_approved')
                values = (1, 0)
                approval_condition = "input_form_id='%s' and approval_num=%s" % (input_form_id, next_approval_num)
                sql = self.create_update_sql(db_name, 'approvalTable', fields, values, approval_condition)
                logger.debug("FN:system_approval_trigger next_update_approvalTable_sql:{}".format(sql))
                return_count = self.updete_exec(conn, sql)


                # 4.change status
                # insert form
                if all_approval_flag == 1:

                    form_status_code = Status.in_porgress
                    fields = ('form_status', 'updated_time')
                    values = (form_status_code, now)
                    update_condition = 'id="%s" and history_id="%s" ' % (input_form_id, history_id)
                    sql = self.create_update_sql(db_name, 'inputFormTable', fields, values, update_condition)
                    logger.debug("FN:system_approval_trigger update_inputFormTable_sql:{}".format(sql))
                    return_count = self.updete_exec(conn, sql)

                    # checking_list = self.__get_adgroup_member(notice_ids)
                    data = response_code.SUCCESS
                    data['data'] = {'id': input_form_id, 'count': return_count, 'tasks': tasks,
                                    'gcp_tasks': gcp_tasks, 'is_approved': all_approval_flag}
                    data['msg'] = 'The input form is finished.'
                else:
                    data = response_code.SUCCESS
                    data['msg'] = 'Airflow approval success.'
                    # return data
            else:
                data = response_code.UPDATE_DATA_FAIL
                data['msg'] = 'Your form\'s tasks miss one of roles of each tasks:\n{}\nPlease find IT support.'.format('\n'.join(miss_role_list))
            if 'data' not in data:
                data['data'] = {}
            if 'notice_ids' not in data['data']:
                data['data']['notice_ids'] = []
            else:
                data['data']['notice_ids'] = list(set(data['data']['notice_ids']))
            data['data']['history_id'] = history_id
            return data

        except Exception as e:
            logger.error("FN:change_status error:{}".format(traceback.format_exc()))
            return response_code.GET_DATA_FAIL
        finally:
            conn.close()


    # when finish the workflow task, update the logs
    def updateTask(self, user_key, account_id, input_form_id, workspace_id, tasks, return_msg_list):
        conn = MysqlConn()
        db_name = configuration.get_database_name()

        try:
            creator_id = user_key

            input_form_condition = 'id="%s" order by history_id desc' % (input_form_id)
            sql = self.create_select_sql(db_name, 'inputFormTable', '*', input_form_condition)
            logger.debug("FN:updateTask inputFormTable_sql:{}".format(sql))
            form_infos = self.execute_fetch_all(conn, sql)
            if not form_infos:
                data = response_code.ADD_DATA_FAIL
                data['msg'] = 'form not found'
                return data
            history_id = form_infos[0]['history_id']
            # do the user exist
            user_exist_flag = self.__check_table_id_exist(creator_id, 'userTable', db_name, conn)
            if not user_exist_flag:
                data = response_code.ADD_DATA_FAIL
                data['msg'] = 'user not found'
                return data

            form_status_code = Status.completed
            now = str(datetime.datetime.now())
            # return_count = self.updete_exec(conn, sql)
            for i in range(len(tasks)):
                input_stage_id = tasks[i]['id']
                logs_item = return_msg_list[i][0]
                comment = return_msg_list[i][1]
                if logs_item['code'] == 200:
                    status = 1
                else:
                    status = -1
                    form_status_code = Status.failed
                if isinstance(logs_item, dict):
                    logs = json.dumps(logs_item).replace('\\', '\\\\')
                else:
                    logs = str(logs_item)
                fields = ('status', 'logs', 'comment', 'updated_time')
                values = (status, logs, comment, now)
                stage_condition = 'id="%s"' % (input_stage_id)
                sql = self.create_update_sql(db_name, 'inputStageTable', fields, values, stage_condition)
                logger.debug("FN:updateTask inputStageTable_sql:{}".format(sql))
                return_count = self.updete_exec(conn, sql)

            # update form
            # inputData = {'id': input_form_id, 'form_status': form_status_code, 'comment': ''}
            # data = self.change_status(user_key, account_id, workspace_id, inputData)
            fields = ('form_status', 'updated_time')
            values = (form_status_code, now)
            update_condition = 'id="%s" and history_id="%s" ' % (input_form_id, history_id)
            sql = self.create_update_sql(db_name, 'inputFormTable', fields, values, update_condition)
            _ = self.updete_exec(conn, sql)

            # data = response_code.SUCCESS
            # data['data'] = {'history_id': history_id}
            return response_code.SUCCESS
        except Exception as e:
            logger.error("FN:change_status error:{}".format(traceback.format_exc()))
            return response_code.GET_DATA_FAIL
        finally:
            conn.close()

    # def add_new_usecase_setting(self, input_form_id, form_id, user_id, workspace_id):

    #     from db.usecase.db_usecase_mgr import usecase_mgr
    #     from db.form.db_form_mgr import form_mgr
    #     from db.input_form.db_input_form_mgr import input_form_mgr
    #     try:
    #         input_form_data = input_form_mgr.get_input_form_data(user_id, input_form_id)
    #         if input_form_data['code'] != 200:
    #             return response_code.GET_DATA_FAIL
    #         # logger.debug("FN:add_new_usecase_setting input_form_data:{}".format(input_form_data))

    #         usecase = {'workspace_id': workspace_id}
    #         form_field_values_dict = input_form_data['data'][0]['form_field_values_dict']
    #         usecase_info = form_mgr.get_details_form_by_id(form_id)['data']
    #         # logger.debug("FN:add_new_usecase_setting inputData:{}".format(inputData.keys()))

    #         for index, field_item in enumerate(usecase_info['fieldList']):
    #             field_key = field_item['label']
    #             field_id = field_item['id']
    #             # logger.debug("FN:add_new_usecase_setting field_key:{} field_id:{}".format(field_key, field_id))
    #             usecase[field_key] = form_field_values_dict[field_id]
    #         # form_field_values_dict = inputData['form_field_values_dict']
    #         # # print("inputData:", inputData.keys())
    #         # print('usecase:', usecase)
    #         # logger.debug("FN:add_new_usecase_setting inputData:{} usecase:{}".format(inputData.keys(), usecase))
    #         # exit(0)
    #         data = usecase_mgr.add_new_usecase_setting(usecase)
    #         return data
    #     except Exception as e:
    #         error = traceback.format_exc()
    #         logger.error("FN:add_new_usecase_setting error:" + e)
    #         logger.error("FN:add_new_usecase_setting error:" + error)
    #         return response_code.GET_DATA_FAIL

    # def add_new_policy_tags(self,  input_form_id, form_id, user_id, workspace_id):
    #
    #     from db.workspace.db_workspace_mgr import workspace_mgr
    #     from db.form.db_form_mgr import form_mgr
    #     from db.input_form.db_input_form_mgr import input_form_mgr
    #     try:
    #         input_form_data = input_form_mgr.get_input_form_data(user_id, input_form_id)
    #         if input_form_data['code'] != 200:
    #             return response_code.GET_DATA_FAIL
    #         # print('input_form_data:', input_form_data)
    #
    #         policy_tags = {'workspace_id': workspace_id, 'input_form_id': input_form_id, 'creator_id': user_id}
    #         form_field_values_dict = input_form_data['data'][0]['form_field_values_dict']
    #         policy_tags_info = form_mgr.get_details_form_by_id(form_id)['data']
    #         # # print("inputData:", inputData.keys())
    #         for index, field_item in enumerate(policy_tags_info['fieldList']):
    #             field_key = field_item['label']
    #             field_id = field_item['id']
    #             # print(field_key, field_id)
    #             policy_tags[field_key] = form_field_values_dict[field_id]
    #         # form_field_values_dict = inputData['form_field_values_dict']
    #         # # print("inputData:", inputData.keys())
    #         # print('policy_tags:', policy_tags)
    #         # exit(0)
    #         data = workspace_mgr.add_new_policy_tags(policy_tags)
    #         return data
    #     except Exception as e:
    #         error = traceback.format_exc()
    #         # print(error)
    #         return response_code.GET_DATA_FAIL

governance_mgr = DbGovernanceMgr()
