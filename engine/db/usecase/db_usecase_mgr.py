#!/usr/bin/python
# -*- coding: UTF-8 -*

from common.common_input_form_status import status as Status
from db.base import DbBase
from db.connection_pool import MysqlConn
import copy
import datetime
from utils.status_code import response_code
from config import configuration
from db.workspace.db_workspace_mgr import workspace_mgr
import json
from utils.ldap_helper import Ldap
from common.common_input_form_status import status
import traceback
import logging

logger = logging.getLogger("main." + __name__)

class DbUseCaseMgr(DbBase):
    """
    Use case related DB Operation
    """
    resource_list = ['jupyter', 'datastudio']

    def __set_usecase(self, usecase_info, usecase_id=None):

        conn = MysqlConn()
        try:
            group_dict = usecase_info['group_dict']
            group_label = usecase_info['group_label']
            workspace_id = usecase_info['workspace_id']
            region_country = usecase_info['region_country']
            validity_date = usecase_info['validity_date']
            des = usecase_info['uc_des']
            budget = usecase_info['budget']
            admin_sa = usecase_info['admin_sa']
            allow_cross_region = bool(usecase_info['allow_cross_region'])
            usecase_name = usecase_info['usecase_name']
            create_time = usecase_info['create_time']
            input_form = usecase_info.get('uc_input_form', -1)
            jupyter_access, studio_access = usecase_info['resources_access'].split(',')
            resources_access = {'jupyter': jupyter_access, 'datastudio': studio_access}

            db_name = configuration.get_database_name()

            # insert workspace
            if usecase_id is not None:
                fields = ('ID', 'WORKSPACE_ID', 'USECASE_NAME', 'VALIDITY_TILL', 'BUDGET', 'INPUT_FORM_ID',
                          'REGION_COUNTRY', 'RESOURCES_ACCESS_LIST', 'SERVICE_ACCOUNT',
                          'CROSS_REGION', 'CREATE_TIME', 'DES')
                values = (usecase_id, workspace_id, usecase_name, validity_date, budget, input_form, region_country,
                          json.dumps(resources_access), admin_sa, allow_cross_region, create_time, des)
            else:
                fields = ('WORKSPACE_ID', 'USECASE_NAME', 'VALIDITY_TILL', 'BUDGET', 'INPUT_FORM_ID',
                          'REGION_COUNTRY', 'RESOURCES_ACCESS_LIST', 'SERVICE_ACCOUNT',
                          'CROSS_REGION', 'CREATE_TIME', 'DES')
                values = (workspace_id, usecase_name, validity_date, budget, input_form, region_country,
                          json.dumps(resources_access), admin_sa, allow_cross_region, create_time, des)
            sql = self.create_insert_sql(db_name, 'usecaseTable', '({})'.format(', '.join(fields)), values)
            logger.debug("FN:DbUseCaseMgr__set_usecase insert_usecaseTable_sql:{}".format(sql))
            usecase_id = self.insert_exec(conn, sql, return_insert_id=True)

            # insert group info
            ad_group_fields = ('GROUP_MAIL', 'CREATE_TIME', 'DES')
            for ad_group_name in group_dict:
                role_list = group_dict[ad_group_name]
                label_list = group_label[ad_group_name]
                select_condition = "GROUP_MAIL='%s' " % ad_group_name
                select_table_sql = self.create_select_sql(db_name, "adgroupTable", "*", select_condition)
                ad_group_info = self.execute_fetch_one(conn, select_table_sql)
                if ad_group_info:
                    group_id = ad_group_info['ID']
                else:
                    values = (ad_group_name, create_time, des)
                    sql = self.create_insert_sql(db_name, 'adgroupTable', '({})'.format(', '.join(ad_group_fields)),
                                                 values)
                    logger.debug("FN:DbUseCaseMgr__set_usecase insert_adgroupTable_sql:{}".format(sql))
                    group_id = self.insert_exec(conn, sql, return_insert_id=True)
                # insert workspace_to_adgroupTable
                w2a_fields = ('USECASE_ID', 'LABEL_LIST', 'AD_GROUP_ID', 'ROLE_LIST')
                values = (usecase_id, json.dumps(label_list), group_id, json.dumps(role_list))
                sql = self.create_insert_sql(db_name, 'usecase_to_adgroupTable', '({})'.format(', '.join(w2a_fields)),
                                             values)
                logger.debug("FN:DbUseCaseMgr__set_usecase insert_usecase_to_adgroupTable_sql:{}".format(sql))
                self.insert_exec(conn, sql, return_insert_id=True)

            usecase_info['usecase_id'] = usecase_id
            data = response_code.SUCCESS
            data['data'] = usecase_info
            return data
        except Exception as e:
            logger.error("FN:DbUseCaseMgr__set_usecase error:{}".format(traceback.format_exc()))
            return response_code.GET_DATA_FAIL
        finally:
            conn.close()

    def __delete_usecase(self, id):
        conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()

            condition = "ID=%s" % id
            delete_table_sql = self.create_delete_sql(db_name, "usecaseTable", condition)
            self.delete_exec(conn, delete_table_sql)
            return response_code.SUCCESS
        except Exception as e:
            logger.error("FN:DbUseCaseMgr__delete_usecase error:{}".format(traceback.format_exc()))
            return response_code.DELETE_DATA_FAIL
        finally:
            conn.close()

    def __delete_2ad_to_usecase(self, id):
        conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()

            condition = "USECASE_ID=%s" % id
            # select_table_sql = self.create_select_sql(db_name, "usecase_to_adgroupTable", '*', condition)
            # wp_ad_info = self.delete_exec(conn, select_table_sql)
            # for wp_ad in wp_ad_info:
            #     ad_group_id = wp_ad['AD_GROUP_ID']
            #     ad_condition = "ID=%s" % ad_group_id
            #     delete_table_sql = self.create_delete_sql(db_name, "adgroupTable", ad_condition)
            #     self.delete_exec(conn, delete_table_sql)

            delete_table_sql = self.create_delete_sql(db_name, "usecase_to_adgroupTable", condition)
            self.delete_exec(conn, delete_table_sql)
            return response_code.SUCCESS
        except Exception as e:
            logger.error("FN:DbUseCaseMgr__delete_2ad_to_usecase error:{}".format(traceback.format_exc()))
            return response_code.DELETE_DATA_FAIL
        finally:
            conn.close()

    def add_new_usecase_setting(self, usecase):
        conn = MysqlConn()
        try:
            workspace_id = usecase['workspace_id']
            data = workspace_mgr.get_workspace_info_by_id(workspace_id)
            if data['code'] != 200:
                data = response_code.UPDATE_DATA_FAIL
                data['msg'] = 'the workspace does not exists, update failed'
                return data

            db_name = configuration.get_database_name()
            usecase_info = {}
            usecase_name = usecase['usecase_name']
            usecase_info['workspace_id'] = usecase['workspace_id']
            usecase_info['region_country'] = usecase['region_country']
            usecase_info['validity_date'] = usecase['validity_date']
            usecase_info['uc_des'] = usecase['uc_des']
            usecase_info['admin_sa'] = usecase['admin_sa']
            usecase_info['budget'] = usecase['budget']
            usecase_info['allow_cross_region'] = usecase['allow_cross_region']
            usecase_info['usecase_name'] = usecase_name
            usecase_info['resources_access'] = usecase['resources_access']
            create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            usecase_info['create_time'] = create_time
            usecase_info['uc_input_form'] = usecase['uc_input_form']
            usecase_info['group_dict'] = {}
            usecase_info['group_label'] = {}
            group_mapping = [
                (usecase['uc_team_group'], 'USER', 'uc_team_group'),
                (usecase['uc_owner_group'], 'GOVERNOR', 'uc_owner_group'),
            ]
            for group_item in group_mapping:
                ad_group = group_item[0]
                role = group_item[1]
                label = group_item[2]
                if ad_group not in usecase_info['group_dict']:
                    usecase_info['group_dict'][ad_group] = [role]
                else:
                    usecase_info['group_dict'][ad_group].append(role)
                if ad_group not in usecase_info['group_label']:
                    usecase_info['group_label'][ad_group] = [label]
                else:
                    usecase_info['group_label'][ad_group].append(label)

            condition = 'USECASE_NAME="%s" and WORKSPACE_ID="%s"' % (usecase_name, workspace_id)
            sql = self.create_select_sql(db_name, 'usecaseTable', '*', condition)
            logger.debug("FN:DbUseCaseMgr_add_new_usecase_setting usecaseTable_sql:{}".format(sql))
            usecase_infos = self.execute_fetch_all(conn, sql)
            if usecase_infos:
                data = response_code.ADD_DATA_FAIL
                data['msg'] = 'UseCase already existed'
                return data
            logger.debug("FN:DbUseCaseMgr_add_new_usecase_setting usecase_info:{}".format(usecase_info))
            usecase_insert = self.__set_usecase(usecase_info)
            data = response_code.SUCCESS
            usecase['usecase_id'] = usecase_insert['data']['usecase_id']
            data['data'] = usecase
            return data
        except Exception as e:
            logger.error("FN:DbUseCaseMgr_add_new_usecase_setting error:{}".format(traceback.format_exc()))
            return response_code.GET_DATA_FAIL
        finally:
            conn.close()

    # get usecase info
    def get_usecase_info_by_ad_group(self, account_id):
        conn = MysqlConn()
        # # print('ad_group_list:', ad_group_list)
        try:
            ad_group_list = Ldap.get_member_ad_group(account_id, Status.offline_flag)
            db_name = configuration.get_database_name()
            # check workspace and org ad group


            usecase_id_set = set()
            for ad_group_name in ad_group_list:
                condition = "GROUP_MAIL='%s' " % (ad_group_name)
                relations = [{"table_name": "usecase_to_adgroupTable",
                              "join_condition": "usecase_to_adgroupTable.AD_GROUP_ID=adgroupTable.ID"}]
                sql = self.create_get_relation_sql(db_name, 'adgroupTable', '*', relations, condition)
                uc_ad_info = self.execute_fetch_all(conn, sql)
                logger.debug("FN:DbUseCaseMgr_get_usecase_info_by_ad_group adgroupTable_sql:{}".format(sql))
                usecase_id_set = usecase_id_set | set([str(wp_ad['USECASE_ID']) for wp_ad in uc_ad_info])
            logger.debug("FN:DbUseCaseMgr_get_usecase_info_by_ad_group usecase_id_set:{}".format(usecase_id_set))
            if 'None' in usecase_id_set:
                usecase_id_set.remove('None')
            logger.debug("FN:DbUseCaseMgr_get_usecase_info_by_ad_group usecase_id_set:{}".format(usecase_id_set))

            if not usecase_id_set:
                data = response_code.SUCCESS
                data['data'] = []
                data['msg'] = 'no usecase'
                return data
            condition = 'ID in ({})'.format(','.join(usecase_id_set))
            db_name = configuration.get_database_name()
            sql = self.create_select_sql(db_name, 'usecaseTable',
                                         'ID,WORKSPACE_ID,USECASE_NAME,VALIDITY_TILL,RESOURCES_ACCESS_LIST,CREATE_TIME',
                                         condition)
            print('usecaseTable sql:', sql)
            usecase_infos = self.execute_fetch_all(conn, sql)
            return_infos = []
            for index, usecase_info in enumerate(usecase_infos):
                usecase_id = usecase_info['ID']

                one_usecase = {'id': usecase_id, 'workspace_id': usecase_info['WORKSPACE_ID'],
                               'usecase_name': usecase_info['USECASE_NAME'],
                               'validity_date': usecase_info['VALIDITY_TILL'],
                               'create_time': usecase_info['CREATE_TIME']}
                one_usecase['resources_access_list'] = []
                resource_access_items = json.loads(usecase_info['RESOURCES_ACCESS_LIST'])
                for item in self.resource_list:
                    if item in resource_access_items:
                        one_usecase['resources_access_list'].append(resource_access_items[item].strip())
                one_usecase['resources_access_list'] = ','.join(one_usecase['resources_access_list'])
                logger.debug("FN:DbUseCaseMgr_get_usecase_info_by_ad_group one_usecase:{}".format(one_usecase))
                # db_name = configuration.get_database_name()
                condition = "USECASE_ID='%s' " % (usecase_id)
                relations = [{"table_name": "adgroupTable",
                              "join_condition": "adgroupTable.ID=usecase_to_adgroupTable.AD_GROUP_ID"}]
                sql = self.create_get_relation_sql(db_name, 'usecase_to_adgroupTable', '*', relations, condition)
                ad_group_infos = self.execute_fetch_all(conn, sql)
                for ad_group_info in ad_group_infos:
                    label_list = json.loads(ad_group_info['LABEL_LIST'])
                    for label in label_list:
                        one_usecase[label] = ad_group_info['GROUP_MAIL']
                return_infos.append(one_usecase)
            logger.debug("FN:DbUseCaseMgr_get_usecase_info_by_ad_group return_infos:{}".format(return_infos))
            data = response_code.SUCCESS
            data['data'] = return_infos
            return data
        except Exception as e:
            logger.error("FN:DbUseCaseMgr_get_usecase_info_by_ad_group error:{}".format(traceback.format_exc()))
            return response_code.GET_DATA_FAIL
        finally:
            conn.close()

    # get usecase info
    def get_usecase_info_by_workspace(self, workspace_id):
        
        conn = MysqlConn()
        try:

            condition = "WORKSPACE_ID='%s'" % workspace_id
            db_name = configuration.get_database_name()
            sql = self.create_select_sql(db_name, 'usecaseTable',
                                         'ID,WORKSPACE_ID,USECASE_NAME,VALIDITY_TILL,RESOURCES_ACCESS_LIST,CREATE_TIME',
                                         condition)
            logger.debug("FN:DbUseCaseMgr_get_usecase_info_by_workspace usecaseTable_sql:{}".format(sql))
            usecase_infos = self.execute_fetch_all(conn, sql)
            return_infos = []
            for index, usecase_info in enumerate(usecase_infos):
                usecase_id = usecase_info['ID']

                one_usecase = {'id': usecase_id, 'workspace_id': usecase_info['WORKSPACE_ID'],
                               'usecase_name': usecase_info['USECASE_NAME'],
                               'validity_date': usecase_info['VALIDITY_TILL'],
                               'create_time': usecase_info['CREATE_TIME']}
                one_usecase['resources_access_list'] = []
                resource_access_items = json.loads(usecase_info['RESOURCES_ACCESS_LIST'])
                for item in self.resource_list:
                    if item in resource_access_items:
                        one_usecase['resources_access_list'].append(resource_access_items[item].strip())
                one_usecase['resources_access_list'] = ','.join(one_usecase['resources_access_list'])
                logger.debug("FN:DbUseCaseMgr_get_usecase_info_by_workspace one_usecase:{}".format(one_usecase))
                # db_name = configuration.get_database_name()
                condition = "USECASE_ID='%s' " % (usecase_id)
                relations = [{"table_name": "adgroupTable",
                              "join_condition": "adgroupTable.ID=usecase_to_adgroupTable.AD_GROUP_ID"}]
                sql = self.create_get_relation_sql(db_name, 'usecase_to_adgroupTable', '*', relations, condition)
                ad_group_infos = self.execute_fetch_all(conn, sql)
                for ad_group_info in ad_group_infos:
                    label_list = json.loads(ad_group_info['LABEL_LIST'])
                    for label in label_list:
                        one_usecase[label] = ad_group_info['GROUP_MAIL']
                return_infos.append(one_usecase)
            logger.debug("FN:DbUseCaseMgr_get_usecase_info_by_workspace return_infos:{}".format(return_infos))
            data = response_code.SUCCESS
            data['data'] = return_infos
            return data
        except Exception as e:
            logger.error("FN:DbUseCaseMgr_get_usecase_info_by_workspace error:{}".format(traceback.format_exc()))
            return response_code.GET_DATA_FAIL
        finally:
            conn.close()

    # get usecase info
    def get_usecase_info_by_id(self, id):
        conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            condition = "ID=%s " % (id)
            sql = self.create_select_sql(db_name, 'usecaseTable', '*', condition)
            logger.debug("FN:DbUseCaseMgr_get_usecase_info_by_id usecaseTable_sql:{}".format(sql))
            usecase_info = self.execute_fetch_one(conn, sql)
            if usecase_info:
                data = response_code.SUCCESS
                data['data'] = usecase_info
            else:
                data = response_code.GET_DATA_FAIL
            return data
        except Exception as e:
            logger.error("FN:DbUseCaseMgr_get_usecase_info_by_id error:{}".format(traceback.format_exc()))
            return response_code.GET_DATA_FAIL
        finally:
            conn.close()

    # modify usecase info
    def update_usecase_info(self, usecase):
        conn = MysqlConn()
        try:
            usecase_id = usecase['id']
            workspace_id = usecase['workspace_id']

            data = workspace_mgr.get_workspace_info_by_id(workspace_id)
            if data['code'] != 200:
                data = response_code.UPDATE_DATA_FAIL
                data['msg'] = 'the workspace does not exists, update failed'
                return data
            data = self.get_usecase_info_by_id(usecase_id)
            if data['code'] != 200:
                data = response_code.UPDATE_DATA_FAIL
                data['msg'] = 'the usecase does not exists, update failed'
                return data

            self.__delete_2ad_to_usecase(usecase_id)
            self.__delete_usecase(usecase_id)

            usecase_info = {}
            usecase_name = usecase['usecase_name']
            usecase_info['region_country'] = usecase['region_country']
            usecase_info['validity_date'] = usecase['validity_date']
            usecase_info['uc_des'] = usecase['uc_des']
            usecase_info['admin_sa'] = usecase['admin_sa']
            usecase_info['budget'] = usecase['budget']
            usecase_info['allow_cross_region'] = usecase['allow_cross_region']
            usecase_info['usecase_name'] = usecase_name
            usecase_info['resources_access'] = usecase['resources_access']
            create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            usecase_info['create_time'] = create_time
            usecase_info['group_dict'] = {}
            usecase_info['group_label'] = {}
            group_mapping = [
                (usecase['uc_team_group'], 'vistor', 'uc_team_group'),
                (usecase['uc_owner_group'], 'admin', 'uc_owner_group'),
            ]
            for group_item in group_mapping:
                ad_group = group_item[0]
                role = group_item[1]
                label = group_item[2]
                if ad_group not in usecase_info['group_dict']:
                    usecase_info['group_dict'][ad_group] = [role]
                else:
                    usecase_info['group_dict'][ad_group].append(role)
                if ad_group not in usecase_info['group_label']:
                    usecase_info['group_label'][ad_group] = [label]
                else:
                    usecase_info['group_label'][ad_group].append(label)

            usecase_insert = self.__set_usecase(usecase_info, usecase_id)
            data = response_code.SUCCESS
            usecase['usecase_id'] = usecase_insert['data']['usecase_id']
            data['data'] = usecase
            return data
        except Exception as e:
            logger.error("FN:DbUseCaseMgr_update_usecase_info error:{}".format(traceback.format_exc()))
            return response_code.GET_DATA_FAIL
        finally:
            conn.close()

    def delete_usecase_info(self, usecase):
        conn = MysqlConn()
        try:
            usecase_id = usecase['id']
            data = self.get_usecase_info_by_id(usecase_id)
            if data['code'] != 200:
                data = response_code.UPDATE_DATA_FAIL
                data['msg'] = 'the usecase does not exists, update failed'
                return data
            logger.debug("FN:DbUseCaseMgr_delete_usecase_info data:{}".format(data))
            self.__delete_2ad_to_usecase(usecase_id)
            self.__delete_usecase(usecase_id)
            data = response_code.SUCCESS
            data['data'] = usecase
            return data
        except Exception as e:
            logger.error("FN:DbUseCaseMgr_delete_usecase_info error:{}".format(traceback.format_exc()))
            return response_code.GET_DATA_FAIL
        finally:
            conn.close()

    def get_usecase_details_info_by_id(self, workspace_id, usecase_id):
        conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            data = self.get_usecase_info_by_id(usecase_id)
            if data['code'] != 200:
                return response_code.GET_DATA_FAIL
            # get usecase
            usecase_info = data['data']
            usecase_name = usecase_info['USECASE_NAME']
            relations = [
                {"table_name": "dynamicFieldTable",
                 "join_condition": "dynamicFieldValueTable.dynamic_field_id=dynamicFieldTable.id"}]
            condition = "form_id=%s and option_label='%s' and workspace_id='%s'" % (status.system_form_id['usecase'], usecase_name, workspace_id)
            sql = self.create_get_relation_sql(db_name, 'dynamicFieldValueTable', 'dynamicFieldTable.id, option_label',
                                               relations, condition)
            logger.debug("FN:DbUseCaseMgr_get_usecase_details_info_by_id dynamicFieldValueTable_sql:{}".format(sql))
            dynamic_field_infos = self.execute_fetch_all(conn, sql)
            user_input_form_id = []
            user_infos = []
            for dynamic_field_info in dynamic_field_infos:
                dy_id = 'd' + str(dynamic_field_info['id'])
                dy_label = dynamic_field_info['option_label']
                input_form_cond = "dynamic_field_id='%s' and option_label='%s' and using_form_id=%s" % (dy_id,
                                                                                                        dy_label,
                                                                                                        status.system_form_id[
                                                                                                            'add_user'])
                sql = self.create_select_sql(db_name, 'dynamicField_to_inputFormTable', '*', input_form_cond)
                logger.debug("FN:DbUseCaseMgr_get_usecase_details_info_by_id dynamicField_to_inputFormTable_sql:{}".format(sql))
                input_form_infos = self.execute_fetch_all(conn, sql)
                for input_form_info in input_form_infos:
                    user_input_form_id.append(input_form_info['using_input_form_id'])
            # get user info
            user_form_comd = "id=%s" % status.system_form_id['add_user']
            sql = self.create_select_sql(db_name, 'formTable', 'id, fields_list', condition=user_form_comd)
            # get label - field id mapping
            field_name_id_mapping = {}
            user_form_fields = json.loads(self.execute_fetch_one(conn, sql)['fields_list'])
            for field_info in user_form_fields:
                id = field_info['id']
                label = field_info['label']
                field_name_id_mapping[id] = label
            # get user infos
            for input_form_id in user_input_form_id:
                user_info = {}
                user_input_form_comd = "id=%s" % input_form_id
                sql = self.create_select_sql(db_name, 'inputFormTable', 'id, form_field_values_dict', condition=user_input_form_comd)
                user_input_form_fields = json.loads(self.execute_fetch_one(conn, sql)['form_field_values_dict'])
                for field_id in user_input_form_fields:
                    if field_id in field_name_id_mapping:
                        user_info[field_name_id_mapping[field_id]] = user_input_form_fields[field_id]['value']
                    else:
                        user_info[field_name_id_mapping[field_id]] = ''
                user_infos.append(user_info)
            # # print(usecase_id_set)
            # print('data', data)

            return_info = {}
            usecase_id = usecase_info['ID']
            return_info['id'] = usecase_id
            return_info['user_infos'] = user_infos
            return_info['workspace_id'] = usecase_info['WORKSPACE_ID']
            return_info['usecase_name'] = usecase_name
            return_info['validity_date'] = usecase_info['VALIDITY_TILL']
            return_info['budget'] = usecase_info['BUDGET']
            return_info['region_country'] = usecase_info['REGION_COUNTRY']
            allow_cross_region = usecase_info['CROSS_REGION']
            if int(allow_cross_region) == 1:
                return_info['allow_cross_region'] = 'true'
            else:
                return_info['allow_cross_region'] = 'false'
            return_info['service_account'] = usecase_info['SERVICE_ACCOUNT']
            return_info['validity_date'] = usecase_info['VALIDITY_TILL']
            return_info['uc_des'] = usecase_info['DES']
            return_info['create_time'] = usecase_info['CREATE_TIME']
            return_info['resources_access_list'] = []
            resource_access_items = json.loads(usecase_info['RESOURCES_ACCESS_LIST'])
            for item in self.resource_list:
                return_info['resources_access_list'].append(resource_access_items[item].strip())
            return_info['resources_access_list'] = ','.join(return_info['resources_access_list'])
            # db_name = configuration.get_database_name()
            logger.debug("FN:DbUseCaseMgr_get_usecase_details_info_by_id return_info:{}".format(return_info))
            condition = "USECASE_ID='%s' " % (usecase_id)
            relations = [
                {"table_name": "adgroupTable", "join_condition": "adgroupTable.ID=usecase_to_adgroupTable.AD_GROUP_ID"}]
            sql = self.create_get_relation_sql(db_name, 'usecase_to_adgroupTable', '*', relations, condition)
            logger.debug("FN:DbUseCaseMgr_get_usecase_details_info_by_id usecase_to_adgroupTable_sql:{}".format(sql))
            ad_group_infos = self.execute_fetch_all(conn, sql)
            for ad_group_info in ad_group_infos:
                label_list = json.loads(ad_group_info['LABEL_LIST'])
                for label in label_list:
                    return_info[label] = ad_group_info['GROUP_MAIL']
            # get usecase data info
            condition = "workspace_id='%s' and usecase_id='%s'" % (workspace_id, usecase_id)
            relations = [
                {"table_name": "dataOnboardTable", "join_condition": "dataOnboardTable.input_form_id=dataAccessTable.data_input_form_id"}]
            sql = self.create_get_relation_sql(db_name, 'dataAccessTable', 'project_id,location,dataset_id,table_id,dataAccessTable.fields,dataAccessTable.create_time', relations, condition)
            logger.debug("FN:DbUseCaseMgr_get_usecase_details_info_by_id dataAccessTable_sql:{}".format(sql))
            data_access_infos = self.execute_fetch_all(conn, sql)
            for index in range(len(data_access_infos)):
                data_access_infos[index]['fields'] = json.loads(data_access_infos[index]['fields'])
            return_info['data_access'] = data_access_infos

            # print('last:', return_info)
            data = response_code.SUCCESS
            data['data'] = return_info
            return data
        except Exception as e:
            logger.error("FN:DbUseCaseMgr_get_usecase_details_info_by_id error:{}".format(traceback.format_exc()))
            return response_code.GET_DATA_FAIL
        finally:
            conn.close()


    def update_usecase_resource(self, workspace_id, usecase_id, uc_owner_group):

        conn = MysqlConn()
        db_name = configuration.get_database_name()
        try:
            condition = "WORKSPACE_ID='%s' and OWNER_GROUP='%s'" % (workspace_id, uc_owner_group)
            fields = ('USECASE_ID', 'AVAILABLE')
            values = (usecase_id, '0')
            sql = self.create_update_sql(db_name, 'usecaseResourceTable', fields, values, condition)
            logger.debug("FN:DbUseCaseMgr_update_usecase_resource update_usecaseResourceTable_sql:{}".format(sql))
            _ = self.updete_exec(conn, sql)
            return response_code.SUCCESS
        except Exception as e:
            logger.error("FN:DbUseCaseMgr_update_usecase_resource error:{}".format(traceback.format_exc()))
            return response_code.GET_DATA_FAIL
        finally:
            conn.close()
usecase_mgr = DbUseCaseMgr()
