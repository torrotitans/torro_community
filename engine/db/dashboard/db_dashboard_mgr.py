#!/usr/bin/python
# -*- coding: UTF-8 -*

from config import configuration
from db.base import DbBase
from db.connection_pool import MysqlConn
import json
from utils.status_code import response_code
from utils.log_helper import lg
from common.common_input_form_status import status

class DbDashboardMgr(DbBase):

    option_dict = {'AND': ' and ', 'OR': ' or '}
    key_mapping = {'approver_id': 'account_id', 'id': 'inputFormTable.id'}

    def get_data(self, user_id, condition_dict, workspace_id=None):
        """
        :return:
        """
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
                {'table_name': 'user_to_adgroupTable', 'join_condition': 'adgroupTable.ID=user_to_adgroupTable.AD_GROUP_ID'}
            ]
            sql = self.create_get_relation_sql(db_name, 'adgroupTable', 'GROUP_MAIL', relations=relation_tables, condition=condition)
            ad_group_infos = self.execute_fetch_all(db_conn, sql)
            group_list = []
            for ad_group in ad_group_infos:
                group_list.append(ad_group['GROUP_MAIL'])
            # print('group_list:', group_list)
            user_info['GROUP_LIST'] = group_list
            adgroup_list = user_info['GROUP_LIST']
            # # print('user_info', adgroup_list)
            # fetch inputFormTable info
            if 'approverView' in condition_dict:
                approverView = True
            else:
                approverView = False

            table_name = 'inputFormTable'
            max_history_condiction = ' GROUP BY id'
            fields = 'id,max(history_id)'
            max_history_sql = self.create_select_sql(db_name, table_name, fields, max_history_condiction).replace('where ', '')
            # print('max_history_condiction sql: ', max_history_sql)
            role_relations = [{"table_name": "inputFormIndexTable", "join_condition": "inputFormIndexTable.id=approvalTable.input_form_id"},
                              {"table_name": "inputFormTable", "join_condition": "inputFormTable.id=approvalTable.input_form_id"}]
            condition_list = []
            if 'approverView' in condition_dict:
                condition = "ad_group in ('%s') and (inputFormTable.id, history_id) in (%s) " % ("', '".join(adgroup_list), max_history_sql)
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
                    print('form_status:', form_status)
                    if status.pending_approval in form_status:
                        condition_list.append("(now_approval=1)")
                    else:
                        condition_list.append("(approvalTable.account_id='{}')".format(account_id))
                    if status.approved in form_status:
                        condition_dict['form_status'] = [[status.completed, '=']] + condition_dict['form_status']
                        condition_list.append("(approvalTable.is_approved=1)")
                    print('condition_dict:', condition_dict['form_status'] )
                else:
                    condition_list.append("(approvalTable.account_id='{}')".format(account_id))
            else:
                condition = "(inputFormTable.id, history_id) in (%s) and inputFormIndexTable.creator_id='%s'" % (max_history_sql, user_id)

            # # print(condition)
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
                        for i in range(len(filter_list)-1):
                            key_condition_list.append(tamplate.format(key=str(key), value=str(filter_list[i][0]), cond=str(filter_list[i][1])))
                    else:
                        option = ' and '
                        for value in filter_list:
                            key_condition_list.append(tamplate.format(key=str(key), value=str(value[0]), cond=str(value[1])))
                    key_condition = key_condition.format(option.join(key_condition_list))
                    condition_list.append(key_condition)
            condition += ' and '
            condition += ' and '.join(condition_list)
            condition += ' order by inputFormTable.create_time desc'
            # print('condition:', condition)
            fields = 'inputFormTable.id,history_id,form_id,workflow_id,creator_id,account_id as approver_id,workflow_name,fields_num,stages_num,form_status,ad_group,inputFormTable.create_time,inputFormTable.updated_time,inputFormTable.form_field_values_dict'
            role_name_query_sql = self.create_get_relation_sql(db_name, "approvalTable", fields, role_relations,
                                                               condition=condition)
            # print('role_name_query_sql: ', role_name_query_sql)
            # exit(0)

            # get usecase field info
            # print(status.system_form_id, workspace_id)
            dy_condition = "form_id=%s" % (status.system_form_id['usecase'])
            sql = self.create_select_sql(db_name, 'dynamicFieldTable',
                                         'id,label',
                                         condition=dy_condition)
            field_info = self.execute_fetch_one(db_conn, sql)
            if field_info:
                dy_field_id = 'd'+str(field_info['id'])
                dy_field_label = field_info['label']
            else:
                dy_field_id = None
                dy_field_label = None
            # dy_value_cond = 'dynamic_field_id=%s' % field_info['id']
            # sql = self.create_select_sql(db_name, 'dynamicFieldValueTable', 'option_label, option_value', condition=dy_value_cond)
            # dy_value_infos = self.execute_fetch_all(db_conn, sql)
            # dy_label_value_dict = {}
            # for dy_value_info in dy_value_infos:
            #     option_label = dy_value_info['option_label']
            #     option_value = dy_value_info['option_value']
            #     if option_value not in dy_label_value_dict:
            #         dy_label_value_dict[option_value] = option_label
            # print('dy_label_value_dict:', dy_label_value_dict)
            # fetch duplicate form
            print('role_name_query_sql:', role_name_query_sql)
            result = self.execute_fetch_all(db_conn, role_name_query_sql)
            return_result = []
            return_result_keys = []
            for raw_result in result:
                if approverView:
                    return_result_key = str(raw_result['ad_group'])+str(raw_result['approver_id'])+str(raw_result['id'])
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
                    print('user Table:', sql)
                    user_info = self.execute_fetch_one(db_conn, sql)
                    raw_result['creator_id'] = user_info['ACCOUNT_ID']
                    # get uasecase field value
                    form_field_values_dict = json.loads(raw_result['form_field_values_dict'])
                    raw_result[dy_field_label] = ''
                    # print('form_field_values_dict:', form_field_values_dict, dy_field_id)
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
            import traceback
            lg.error(traceback.format_exc())
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
                {'table_name': 'workspace_to_adgroupTable', 'join_condition': 'workspace_to_adgroupTable.AD_GROUP_ID=user_to_adgroupTable.AD_GROUP_ID'}
            ]
            sql = self.create_get_relation_sql(db_name, 'user_to_adgroupTable', 'user_to_adgroupTable.AD_GROUP_ID', relations=relation_tables,
                                               condition=condition)
            # print('create_get_relation_sql1:', sql)
            ad_group_infos = self.execute_fetch_all(db_conn, sql)
            # print('ad_group_infos:', ad_group_infos)
            group_id_set = set()
            for ad_group in ad_group_infos:
                group_id_set.add(str(ad_group['AD_GROUP_ID']))
            creators = []
            if group_id_set:
                condition = 'AD_GROUP_ID in (%s)' % ','.join(group_id_set)
                relation_tables = [
                    {'table_name': 'userTable',
                     'join_condition': 'userTable.ID=user_to_adgroupTable.USER_ID'}]
                sql = self.create_get_relation_sql(db_name, 'user_to_adgroupTable', 'userTable.ID, ACCOUNT_NAME, ACCOUNT_ID',
                                                   relations=relation_tables,
                                                   condition=condition)
                # print('create_get_relation_sql2:', sql)
                user_infos = self.execute_fetch_all(db_conn, sql)
                # print('user_infos:', user_infos)
                for user_info in user_infos:
                    creators.append({'label': user_info['ACCOUNT_ID'], 'value': user_info['ID']})
            condition = 'workspace_id = "%s"' % workspace_id
            sql = self.create_select_sql(db_name, 'formTable', '*', condition)
            form_infos = self.execute_fetch_all(db_conn, sql)
            formList = []
            for form_info in form_infos:
                formList.append({'label': form_info['title'], 'value': form_info['id']})
            data = response_code.SUCCESS
            data['data'] = {'creator': creators, 'formList': formList}
            return data
        except Exception as e:
            import traceback
            lg.error(traceback.format_exc())
            return response_code.GET_DATA_FAIL
        finally:
            db_conn.close()
dashboard_mgr = DbDashboardMgr()
