#!/usr/bin/python
# -*- coding: UTF-8 -*

from config import configuration
from db.base import DbBase
from db.connection_pool import MysqlConn
import json
from utils.status_code import response_code
from common.common_input_form_status import status
# from utils.ldap_helper import Ldap
import traceback
import logging

logger = logging.getLogger("main." + __name__)


class DbDashboardMgr(DbBase):
    option_dict = {'AND': ' and ', 'OR': ' or '}
    key_mapping = {'approver_id': 'account_id', 'id': 'inputFormTable.id'}

    def get_data(self, user_id, condition_dict, workspace_id=None):
        db_conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            # fetch adgroup info
            condition = 'ID="%s"' % user_id
            user_fields = 'ID,ACCOUNT_ID'
            sql = self.create_select_sql(db_name, 'userTable', user_fields, condition=condition)
            user_info = self.execute_fetch_one(db_conn, sql)
            if not user_info:
                data = response_code.GET_DATA_FAIL
                data['msg'] = 'cannot find users, please login in again'
                return data
            account_id = user_info['ACCOUNT_ID']
            del user_info['ACCOUNT_ID']
            condition = 'USER_ID="%s"' % user_id
            relation_tables = [
                {'table_name': 'user_to_adgroupTable',
                 'join_condition': 'adgroupTable.ID=user_to_adgroupTable.AD_GROUP_ID'}
            ]
            sql = self.create_get_relation_sql(db_name, 'adgroupTable', 'GROUP_MAIL', relations=relation_tables,
                                               condition=condition)
            ad_group_infos = self.execute_fetch_all(db_conn, sql)
            group_list = []
            for ad_group in ad_group_infos:
                group_list.append(ad_group['GROUP_MAIL'])
            # logger.debug("FN:get_data group_list:{}".format(group_list))
            user_info['GROUP_LIST'] = group_list
            adgroup_list = user_info['GROUP_LIST'] + [account_id]
            # logger.debug("FN:get_data adgroup_list:{}".format(adgroup_list))
            # fetch inputFormTable info
            if 'approverView' in condition_dict:
                approverView = True
            else:
                approverView = False

            table_name = 'inputFormTable'
            max_history_condiction = ' GROUP BY id'
            fields = 'id,max(history_id)'
            max_history_sql = self.create_select_sql(db_name, table_name, fields, max_history_condiction).replace(
                'where ', '')
            # logger.debug("FN:get_data max_history_sql:{}".format(max_history_sql))
            role_relations = [
                {"table_name": "inputFormIndexTable",
                 "join_condition": "inputFormTable.id=inputFormIndexTable.id"},
                {"table_name": "approvalTable",
                 "join_condition": "inputFormTable.id=approvalTable.input_form_id"}
            ]
            condition_list = []
            if 'approverView' in condition_dict:
                condition = "ad_group in ('%s') and (inputFormTable.id, history_id) in (%s) " % (
                    "', '".join(adgroup_list), max_history_sql)
                del condition_dict['approverView']
                if 'form_status' in condition_dict:
                    form_status = []
                    option = condition_dict['form_status'][-1]
                    if isinstance(option, str):
                        form_status_length = len(condition_dict['form_status']) - 1
                    else:
                        form_status_length = len(condition_dict['form_status'])
                    for i in range(form_status_length):
                        form_status.append(int(condition_dict['form_status'][i][0]))
                    logger.debug("FN:get_data form_status:{}".format(form_status))
                    if status.pending_approval in form_status:
                        condition_list.append("(now_approval=1)")
                    else:
                        condition_list.append("(approvalTable.account_id='{}')".format(account_id))
                    if status.approved in form_status:
                        condition_dict['form_status'] = [[status.completed, '=']] + condition_dict['form_status']
                        condition_list.append("(approvalTable.is_approved=1)")
                    logger.debug("FN:get_data condition_dict:{}".format(condition_dict['form_status']))
                else:
                    condition_list.append("(approvalTable.account_id='{}')".format(account_id))
            else:
                condition = "(inputFormTable.id, history_id) in (%s) and inputFormIndexTable.creator_id='%s'" % (
                    max_history_sql, user_id)

            # logger.debug("FN:get_data condition:{}".format(condition))
            condition_list.append("(inputFormIndexTable.workspace_id='%s')" % workspace_id)
            if condition_dict:
                tamplate = "{key}{cond}'{value}'"
                for key in condition_dict:
                    key_condition = "({})"
                    key_condition_list = []
                    filter_list = condition_dict[key]
                    # if key == 'approver_id':
                    #     key = 'account_id'
                    option = filter_list[-1]
                    key = self.key_mapping.get(key, key)
                    if isinstance(option, str):
                        option = self.option_dict.get(option.upper(), ' and ')
                        for i in range(len(filter_list) - 1):
                            key_condition_list.append(tamplate.format(key=str(key), value=str(filter_list[i][0]),
                                                                      cond=str(filter_list[i][1])))
                    else:
                        option = ' and '
                        for value in filter_list:
                            key_condition_list.append(
                                tamplate.format(key=str(key), value=str(value[0]), cond=str(value[1])))
                    key_condition = key_condition.format(option.join(key_condition_list))
                    condition_list.append(key_condition)
            condition += ' and '
            condition += ' and '.join(condition_list)
            condition += ' order by inputFormTable.create_time desc'
            # logger.debug("FN:get_data condition:{}".format(condition))
            fields = 'inputFormTable.id,history_id,form_id,workflow_id,creator_id,account_id as approver_id,' \
                     'workflow_name,fields_num,stages_num,form_status,ad_group,inputFormTable.create_time,' \
                     'inputFormTable.updated_time,inputFormTable.form_field_values_dict'
            role_name_query_sql = self.create_get_relation_sql(db_name, "inputFormTable", fields, role_relations,
                                                               condition=condition)
            logger.debug("FN:get_data role_name_query_sql:{}".format(role_name_query_sql))
            # exit(0)

            # get usecase field info
            # logger.debug("FN:get_data system_form_id:{} workspace_id:{}".format(status.system_form_id, workspace_id))
            dy_condition = "form_id=%s" % (status.system_form_id['usecase'])
            sql = self.create_select_sql(db_name, 'dynamicFieldTable',
                                         'id,label',
                                         condition=dy_condition)
            field_info = self.execute_fetch_one(db_conn, sql)
            if field_info:
                dy_field_id = 'd' + str(field_info['id'])
                dy_field_label = field_info['label']
            else:
                dy_field_id = None
                dy_field_label = None
            # fetch duplicate form

            logger.debug("FN:get_data role_name_query_sql:{}".format(role_name_query_sql))
            result = self.execute_fetch_all(db_conn, role_name_query_sql)
            return_result = []
            return_result_keys = []
            for raw_result in result:
                if approverView:
                    return_result_key = str(raw_result['ad_group']) + str(raw_result['approver_id']) + str(
                        raw_result['id'])
                else:
                    return_result_key = str(raw_result['id'])
                    del raw_result['ad_group']
                    del raw_result['approver_id']
                if return_result_key not in return_result_keys:
                    return_result_keys.append(return_result_key)
                    user_id = raw_result['creator_id']
                    condition = 'ID="%s"' % user_id
                    user_fields = 'ACCOUNT_ID'
                    sql = self.create_select_sql(db_name, 'userTable', user_fields, condition=condition)
                    # logger.debug("FN:get_data userTable_sql:{}".format(sql))
                    user_info = self.execute_fetch_one(db_conn, sql)
                    raw_result['creator_id'] = user_info['ACCOUNT_ID']
                    # get uasecase field value
                    form_field_values_dict = json.loads(raw_result['form_field_values_dict'], strict=False)
                    raw_result[dy_field_label] = ''
                    # logger.debug("FN:get_data form_field_values_dict:{} dy_field_id:{}".format(form_field_values_dict, dy_field_id))
                    if dy_field_id in form_field_values_dict:
                        dy_label_value = form_field_values_dict[dy_field_id]['value']
                        # if dy_value in dy_label_value_dict:
                        raw_result[dy_field_label] = dy_label_value
                    del raw_result['form_field_values_dict']
                    if None in raw_result:
                        del raw_result[None]
                    return_result.append(raw_result)

            data = response_code.SUCCESS
            data['data'] = return_result
            return data
        except Exception as e:
            logger.error("FN:get_data error:{}".format(traceback.format_exc()))
            return response_code.GET_DATA_FAIL
        finally:
            db_conn.close()

    def get_options(self, user_id, workspace_id):

        db_conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            condition = 'USER_ID="%s" and WORKSPACE_ID="%s"' % (user_id, workspace_id)
            relation_tables = [
                {'table_name': 'adgroupTable', 'join_condition': 'adgroupTable.ID=user_to_adgroupTable.AD_GROUP_ID'},
                {'table_name': 'workspace_to_adgroupTable',
                 'join_condition': 'workspace_to_adgroupTable.AD_GROUP_ID=user_to_adgroupTable.AD_GROUP_ID'}
            ]
            sql = self.create_get_relation_sql(db_name, 'user_to_adgroupTable', 'user_to_adgroupTable.AD_GROUP_ID',
                                               relations=relation_tables,
                                               condition=condition)
            # logger.debug("FN:get_options user_to_adgroupTable_sql:{}".format(sql))
            ad_group_infos = self.execute_fetch_all(db_conn, sql)
            # logger.debug("FN:get_options ad_group_infos:{}".format(ad_group_infos))
            group_id_set = set()
            for ad_group in ad_group_infos:
                group_id_set.add(str(ad_group['AD_GROUP_ID']))
            creators = []
            if group_id_set:
                condition = 'AD_GROUP_ID in (%s)' % ','.join(group_id_set)
                relation_tables = [
                    {'table_name': 'userTable',
                     'join_condition': 'userTable.ID=user_to_adgroupTable.USER_ID'}]
                sql = self.create_get_relation_sql(db_name, 'user_to_adgroupTable',
                                                   'userTable.ID, ACCOUNT_NAME, ACCOUNT_ID',
                                                   relations=relation_tables,
                                                   condition=condition)
                # logger.debug("FN:get_options user_to_adgroupTable_sql:{}".format(sql))
                user_infos = self.execute_fetch_all(db_conn, sql)
                # logger.debug("FN:get_options user_infos:{}".format(user_infos))
                for user_info in user_infos:
                    creators.append({'label': user_info['ACCOUNT_ID'], 'value': user_info['ID']})
            condition = 'workspace_id = "%s"' % workspace_id
            sql = self.create_select_sql(db_name, 'formTable', '*', condition)
            # logger.debug("FN:get_options formTable_sql:{}".format(sql))
            form_infos = self.execute_fetch_all(db_conn, sql)
            formList = []
            for form_info in form_infos:
                formList.append({'label': form_info['title'], 'value': form_info['id']})
            data = response_code.SUCCESS
            data['data'] = {'creator': creators, 'formList': formList}
            return data

        except Exception as e:
            logger.error("FN:get_options error:{}".format(traceback.format_exc()))
            return response_code.GET_DATA_FAIL
        finally:
            db_conn.close()

    def get_notify(self, account_id, is_read=None):
        db_conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()

            notify_infos = []
            if is_read:
                is_read_str = "is_read='%s' and " % is_read
            else:
                is_read_str = ""

            # condition = is_read_str + "account_id='%s'" % account_id
            # sql = self.create_select_sql(db_name, 'inputNotifyTable', '*', condition=condition)

            condition = is_read_str + "account_id='%s' order by create_time desc" % account_id
            relation_tables = [
                {'table_name': 'inputFormIndexTable',
                 'join_condition': 'inputNotifyTable.input_form_id=inputFormIndexTable.id'},
                {'table_name': 'formTable', 'join_condition': 'inputFormIndexTable.form_id=formTable.id'}
            ]
            sql = self.create_get_relation_sql(db_name, 'inputNotifyTable', 'inputNotifyTable.*, formTable.title',
                                               relations=relation_tables,
                                               condition=condition)
            # logger.debug("FN:get_options inputNotifyTable_sql:{}".format(sql))
            return_notify_infos = self.execute_fetch_all(db_conn, sql)

            # return_notify_infos = self.execute_fetch_all(db_conn, sql)
            if isinstance(return_notify_infos, list):
                notify_infos.extend(return_notify_infos)

            notify_id_list = list()
            return_data = []

            for notify_info in notify_infos:
                id = notify_info['id']

                if id not in notify_id_list:
                    notify_id_list.append(id)
                    return_data.append(notify_info)

            data = response_code.SUCCESS
            data['data'] = return_data
            return data

        except Exception as e:
            logger.error("FN:get_notify error:{}".format(traceback.format_exc()))
            return response_code.GET_DATA_FAIL
        finally:
            db_conn.close()

    def read_notify(self, account_id, notify_id, is_read=None):
        db_conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            if not is_read:
                is_read = 0

            if isinstance(notify_id, list):
                # Check if notify_id is a list
                notify_list = "{}".format(notify_id)[1:-1]  # Remove the []
                condition = "id in (%s) and account_id='%s'" % (notify_list, account_id)
            else:
                condition = "id='%s' and account_id='%s'" % (notify_id, account_id)

            fields = ('is_read',)
            values = (is_read,)
            sql = self.create_update_sql(db_name, 'inputNotifyTable', fields, values, condition=condition)
            logger.debug("FN:read_notify inputNotifyTable_sql:{}".format(sql))
            _ = self.updete_exec(db_conn, sql)
            return response_code.SUCCESS

        except Exception as e:
            logger.error("FN:read_notify error:{}".format(traceback.format_exc()))
            return response_code.GET_DATA_FAIL

        finally:
            db_conn.close()


dashboard_mgr = DbDashboardMgr()
