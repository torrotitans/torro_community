#!/usr/bin/python
# -*- coding: UTF-8 -*

from common.common_input_form_status import status as Status
from db.base import DbBase
from db.connection_pool import MysqlConn
from utils.log_helper import lg
import copy
import datetime
from utils.status_code import response_code
from config import configuration
from utils.ldap_helper import Ldap
from db.user.db_user_mgr import user_mgr
import json
import traceback
import logging

logger = logging.getLogger("main." + __name__)

class DbWorkspaceMgr(DbBase):
    """
    用户相关数据库表操作类
    """

    def __set_workspace(self, workspace_info, workspace_id=None):

        conn = MysqlConn()
        try:
            group_dict = workspace_info['group_dict']
            group_label = workspace_info['group_label']
            workspace_name = workspace_info['workspace_name']
            if workspace_info['it_approval'] == '':
                it_approval = False
            else:
                it_approval = True
            if workspace_info['head_approval'] == '':
                head_approval = False
            else:
                head_approval = True
            cycle = workspace_info['cycle']
            regions = workspace_info['regions']
            system = workspace_info['system']
            create_time = workspace_info['create_time']
            des = workspace_info['des']
            db_name = configuration.get_database_name()

            # insert workspace
            if workspace_id is not None:

                condition = "ID='%s'" % workspace_id

                fields = ('WORKSPACE_NAME', 'IT_APPROVAL', 'HEAD_APPROVAL', 'RECERTIFICATION_CYCLE', 'REGIONS',
                          'CREATE_TIME',
                          'DES')
                values = (workspace_name, it_approval, head_approval, cycle, json.dumps(regions), create_time, des)

                sql = self.create_update_sql(db_name, 'workspaceTable', fields, values, condition=condition)
                logger.debug("FN:DbWorkspaceMgr__set_workspace workspaceTable_sql:{}".format(sql))
                _ = self.updete_exec(conn, sql)

                # update group info
                ad_group_fields = ('GROUP_MAIL', 'CREATE_TIME', 'DES')
                for ad_group_name in group_dict:
                    role_list = list(group_dict[ad_group_name])
                    label_list = list(group_label[ad_group_name])
                    select_condition = "GROUP_MAIL='%s' " % ad_group_name
                    sql = self.create_select_sql(db_name, "adgroupTable", "*", select_condition)
                    logger.debug("FN:DbWorkspaceMgr__set_workspace adgroupTable_sql:{}".format(sql))
                    ad_group_info = self.execute_fetch_one(conn, sql)
                    if ad_group_info:
                        group_id = ad_group_info['ID']
                    else:
                        values = (ad_group_name, create_time, des)
                        sql = self.create_insert_sql(db_name, 'adgroupTable', '({})'.format(', '.join(ad_group_fields)),
                                                     values)
                        logger.debug("FN:DbWorkspaceMgr__set_workspace insert_adgroupTable_sql:{}".format(sql))
                        group_id = self.insert_exec(conn, sql, return_insert_id=True)

                    # insert workspace_to_adgroupTable
                    w2a_fields = ('WORKSPACE_ID', 'LABEL_LIST', 'AD_GROUP_ID', 'ROLE_LIST')
                    values = (workspace_id, json.dumps(label_list), group_id, json.dumps(role_list))
                    sql = self.create_insert_sql(db_name, 'workspace_to_adgroupTable',
                                                 '({})'.format(', '.join(w2a_fields)),
                                                 values)
                    logger.debug("FN:DbWorkspaceMgr__set_workspace insert_workspace_to_adgroupTable_sql:{}".format(sql))
                    self.insert_exec(conn, sql, return_insert_id=True)

                # update system fields
                system_id_dict = {}
                condition = "id=%s and workspace_id='%s'" % ('1', workspace_id)
                sql = self.create_select_sql(db_name, 'fieldTable', '*', condition)
                logger.debug("FN:DbWorkspaceMgr__set_workspace fieldTable_sql:{}".format(sql))
                region_country_info = self.execute_fetch_one(conn, sql)
                if len(region_country_info) == 0:
                    field_fields = ('id', 'workspace_id', 'u_id', 'style', 'label', 'default_value', 'placeholder',
                                    'value_num', 'value_list', 'edit', 'des', 'create_time', 'updated_time')
                    values = ('1', workspace_id, '0', '2', 'Region / Country', '', '', 0,
                              '[]', '0', des, create_time, create_time)
                    sql = self.create_insert_sql(db_name, 'fieldTable', '({})'.format(', '.join(field_fields)), values)
                    logger.debug("FN:DbWorkspaceMgr__set_workspace insert_fieldTable_sql:{}".format(sql))
                    self.insert_exec(conn, sql, return_insert_id=True)
                system_id_dict['s1'] = 's1'

                for system_style in system:
                    for system_item in system[system_style]:
                        u_id = int(system_item['id'].replace('s', '').replace('u', ''))

                        condition = "workspace_id='%s' and id='%s' " % (workspace_id, u_id)
                        default_value = system_item.get('default', '')
                        des = system_item.get('des', '')
                        edit = system_item.get('edit', 1)
                        label = system_item['label']
                        placeholder = system_item.get('placeholder', '')
                        # u_id = int(system_item['id'].replace('s', '').replace('u', ''))
                        value_list = system_item.get('options', [])
                        value_num = len(value_list)

                        insert_flag = 0
                        if u_id != 1:
                            sql = self.create_select_sql(db_name, 'fieldTable', 'id', condition=condition)
                            print('fieldTable sql:', sql)
                            field_info = self.execute_fetch_one(conn, sql)
                            if not field_info:
                                insert_flag = 1
                        # s1 is region system field, so it cannot be the existing system field, add new one for it.
                        elif u_id == 1:
                            insert_flag = 1
                        if insert_flag:
                            # insert field info
                            field_fields = ('u_id', 'workspace_id', 'style', 'label', 'default_value', 'placeholder',
                                            'value_num', 'value_list', 'edit', 'des', 'create_time', 'updated_time')
                            values = (u_id, workspace_id, system_style, label, default_value, placeholder, value_num,
                                      json.dumps(value_list), edit, des, create_time, create_time)
                            sql = self.create_insert_sql(db_name, 'fieldTable', '({})'.format(', '.join(field_fields)), values)
                            logger.debug("FN:DbWorkspaceMgr__set_workspace insert_fieldTable_sql:{}".format(sql))
                            _ = self.insert_exec(conn, sql)
                        else:
                            # update group info
                            field_fields = ('u_id', 'style', 'label', 'default_value', 'placeholder',
                                            'value_num', 'value_list', 'edit', 'des', 'create_time', 'updated_time')
                            values = (u_id, system_style, label, default_value, placeholder, value_num,
                                      json.dumps(value_list), edit, des, create_time, create_time)
                            sql = self.create_update_sql(db_name, 'fieldTable', field_fields, values, condition=condition)
                            logger.debug("FN:DbWorkspaceMgr__set_workspace update_fieldTable_sql:{}".format(sql))
                            _ = self.updete_exec(conn, sql)
                    condition = "workspace_id='%s'" % (workspace_id)
                    sql = self.create_select_sql(db_name, 'fieldTable', '*', condition=condition)
                    logger.debug("FN:DbWorkspaceMgr__set_workspace fieldTable_sql:{}".format(sql))
                    field_infos = self.execute_fetch_all(conn, sql)
                    for field_info in field_infos:
                        system_id_dict[field_info['id']] = 's' + str(field_info['id'])
            else:
                fields = (
                    'WORKSPACE_NAME', 'IT_APPROVAL', 'HEAD_APPROVAL', 'RECERTIFICATION_CYCLE', 'REGIONS', 'CREATE_TIME',
                    'DES')
                values = (workspace_name, it_approval, head_approval, cycle, json.dumps(regions), create_time, des)

                sql = self.create_insert_sql(db_name, 'workspaceTable', '({})'.format(', '.join(fields)), values)
                logger.debug("FN:DbWorkspaceMgr__set_workspace insert_workspaceTable_sql:{}".format(sql))
                workspace_id = self.insert_exec(conn, sql, return_insert_id=True)

                # insert group info
                ad_group_fields = ('GROUP_MAIL', 'CREATE_TIME', 'DES')
                for ad_group_name in group_dict:
                    role_list = list(group_dict[ad_group_name])
                    label_list = list(group_label[ad_group_name])
                    select_condition = "GROUP_MAIL='%s' " % ad_group_name
                    select_table_sql = self.create_select_sql(db_name, "adgroupTable", "*", select_condition)
                    logger.debug("FN:DbWorkspaceMgr__set_workspace adgroupTable_sql:{}".format(sql))
                    ad_group_info = self.execute_fetch_one(conn, select_table_sql)
                    if ad_group_info:
                        group_id = ad_group_info['ID']
                    else:
                        values = (ad_group_name, create_time, des)
                        sql = self.create_insert_sql(db_name, 'adgroupTable', '({})'.format(', '.join(ad_group_fields)),
                                                     values)
                        logger.debug("FN:DbWorkspaceMgr__set_workspace insert_adgroupTable_sql:{}".format(sql))
                        group_id = self.insert_exec(conn, sql, return_insert_id=True)
                    # insert workspace_to_adgroupTable
                    w2a_fields = ('WORKSPACE_ID', 'LABEL_LIST', 'AD_GROUP_ID', 'ROLE_LIST')
                    values = (workspace_id, json.dumps(label_list), group_id, json.dumps(role_list))
                    sql = self.create_insert_sql(db_name, 'workspace_to_adgroupTable',
                                                 '({})'.format(', '.join(w2a_fields)),
                                                 values)
                    logger.debug("FN:DbWorkspaceMgr__set_workspace insert_workspace_to_adgroupTable_sql:{}".format(sql))
                    self.insert_exec(conn, sql, return_insert_id=True)

                # insert region system fields
                system_id_dict = {}
                condition = "id=%s and workspace_id='%s'" % ('1', workspace_id)
                sql = self.create_select_sql(db_name, 'fieldTable', '*', condition)
                region_country_info = self.execute_fetch_one(conn, sql)
                if len(region_country_info) == 0:
                    field_fields = ('id', 'workspace_id', 'u_id', 'style', 'label', 'default_value', 'placeholder',
                                    'value_num', 'value_list', 'edit', 'des', 'create_time', 'updated_time')
                    values = ('1', workspace_id, '0', '2', 'Region / Country', '', '', 0,
                              '[]', '0', des, create_time, create_time)
                    sql = self.create_insert_sql(db_name, 'fieldTable', '({})'.format(', '.join(field_fields)), values)
                    logger.debug("FN:DbWorkspaceMgr__set_workspace insert_fieldTable_sql:{}".format(sql))
                    self.insert_exec(conn, sql, return_insert_id=True)
                system_id_dict['s1'] = 's1'

                # insert group info
                field_fields = ('workspace_id', 'u_id', 'style', 'label', 'default_value', 'placeholder',
                                'value_num', 'value_list', 'edit', 'des', 'create_time', 'updated_time')
                # for system_style in system:
                #     for system_item in system[system_style]:
                #         # if 's' in system_item['id']:
                #         #     continue
                #         default_value = system_item.get('default', '')
                #         des = system_item.get('des', '')
                #         edit = system_item.get('edit', 1)
                #         label = system_item['label']
                #         placeholder = system_item.get('placeholder', '')
                #         u_id = int(system_item['id'].replace('s', '').replace('u', ''))
                #         value_list = system_item.get('options', [])
                #         value_num = len(value_list)
                #
                #         values = (workspace_id, u_id, system_style, label, default_value, placeholder, value_num,
                #                   json.dumps(value_list), edit, des, create_time, create_time)
                #         sql = self.create_insert_sql(db_name, 'fieldTable', '({})'.format(', '.join(field_fields)),
                #                                      values)
                #         logger.debug("FN:DbWorkspaceMgr__set_workspace insert_fieldTable_sql:{}".format(sql))
                #         system_id = self.insert_exec(conn, sql, return_insert_id=True)
                #         system_id_dict[system_item['id']] = 's' + str(system_id)
            workspace_info['workspace_id'] = workspace_id
            workspace_info['system_id_dict'] = system_id_dict
            data = response_code.SUCCESS
            data['data'] = workspace_info
            return data
        except Exception as e:
            logger.error("FN:DbWorkspaceMgr__set_workspace error:{}".format(traceback.format_exc()))
            return response_code.GET_DATA_FAIL
        finally:
            conn.close()

    def __set_team_resource(self, workspace_id, resource_list):

        insert_resource = []
        update_resource = []
        delete_resource = []
        create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for resource_info in resource_list:
            logger.debug("FN:DbWorkspaceMgr__set_team_resource resource_info:{}".format(resource_info))
            if 'resource' not in resource_info or len(resource_info['resource']) < 4:
                continue
            else:
                owner_group = resource_info['resource'][0]
                team_group = resource_info['resource'][1]
                service_account = resource_info['resource'][2]
                label = resource_info['resource'][3]
                items = ','.join(resource_info['resource'][4:])
                # print('resource_info owner_group:', owner_group)
                if ('id' not in resource_info or resource_info['id'] in (None, '')) or ('option' in resource_info and resource_info['option'] == 0):
                    values = (workspace_id, owner_group, team_group, service_account, label, items, create_time)
                    # print('insert_resource item:', values)
                    insert_resource.append(values)
                elif 'id' in resource_info and 'option' in resource_info and resource_info['option'] == 2 and 'available' in resource_info and resource_info['available'] == 1:
                    delete_resource.append(resource_info['id'])
                elif 'id' in resource_info and 'option' in resource_info and resource_info['option'] == 1 and 'available' in resource_info and resource_info['available'] == 1:
                    update_record = {'id': resource_info['id'],
                                    'values': (workspace_id, owner_group, team_group, service_account, label, items, create_time)}
                    update_resource.append(update_record)
                else:
                    pass
        conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            logger.debug("FN:DbWorkspaceMgr__set_team_resource insert_resource:{}".format(insert_resource))
            # sql, insert_data = self.create_batch_insert_sql(db_name, 'usecaseResourceTable', insert_resource)
            # insert
            for values in insert_resource:
                fields = ('WORKSPACE_ID', 'OWNER_GROUP', 'TEAM_GROUP', 'SERVICE_ACCOUNT', 'LABEL', 'ITEMS', 'CREATE_TIME')
                sql = self.create_insert_sql(db_name, 'usecaseResourceTable', '({})'.format(', '.join(fields)), values)
                logger.debug("FN:DbWorkspaceMgr__set_team_resource insert_usecaseResourceTable_sql:{}".format(sql))
                _ = self.insert_exec(conn, sql)
            # update
            for update_record in update_resource:
                resource_id = update_record['id']
                values = update_record['values']
                fields = ('WORKSPACE_ID', 'OWNER_GROUP', 'TEAM_GROUP', 'SERVICE_ACCOUNT', 'LABEL', 'ITEMS', 'CREATE_TIME')
                sql = self.create_update_sql(db_name, 'usecaseResourceTable', fields, values, condition="ID='%s'" % resource_id)
                logger.debug("FN:DbWorkspaceMgr__set_team_resource update_usecaseResourceTable_sql:{}".format(sql))
                _ = self.updete_exec(conn, sql)
            # delete
            condition = "WORKSPACE_ID='%s' and AVAILABLE=1 and ID in ('%s')" % (workspace_id, "', '".join(delete_resource))
            delete_table_sql = self.create_delete_sql(db_name, "usecaseResourceTable", condition)
            self.delete_exec(conn, delete_table_sql)


        except Exception as e:
            logger.error("FN:DbWorkspaceMgr__set_team_resource error:{}".format(traceback.format_exc()))
            return response_code.GET_DATA_FAIL
        finally:
            conn.close()

        pass

    def __delete_groups(self, id):
        pass

    def __delete_system_fields(self, id):
        conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()

            condition = "workspace_id='%s'" % id
            sql = self.create_delete_sql(db_name, "fieldTable", condition)
            logger.debug("FN:DbWorkspaceMgr__delete_system_fields delete_fieldTable_sql:{}".format(sql))
            self.delete_exec(conn, sql)
            return response_code.SUCCESS
        except Exception as e:
            logger.error("FN:DbWorkspaceMgr__delete_system_fields error:{}".format(traceback.format_exc()))
            return response_code.DELETE_DATA_FAIL
        finally:
            conn.close()

    def __update_system_fields(self, id):
        conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()

            condition = "workspace_id='%s'" % id
            sql = self.create_update_sql(db_name, "fieldTable", condition)
            logger.debug("FN:DbWorkspaceMgr__update_system_fields update_fieldTable_sql:{}".format(sql))
            self.delete_exec(conn, sql)
            return response_code.SUCCESS
        except Exception as e:
            logger.error("FN:DbWorkspaceMgr__update_system_fields error:{}".format(traceback.format_exc()))
            return response_code.DELETE_DATA_FAIL
        finally:
            conn.close()

    def __delete_2ad_to_workspace(self, id):
        conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()

            condition = "WORKSPACE_ID='%s'" % id
            # select_table_sql = self.create_select_sql(db_name, "workspace_to_adgroupTable", '*', condition)
            # wp_ad_info = self.delete_exec(conn, select_table_sql)
            # for wp_ad in wp_ad_info:
            #     ad_group_id = wp_ad['AD_GROUP_ID']
            #     ad_condition = "ID=%s" % ad_group_id
            #     delete_table_sql = self.create_delete_sql(db_name, "adgroupTable", ad_condition)
            #     self.delete_exec(conn, delete_table_sql)

            sql = self.create_delete_sql(db_name, "workspace_to_adgroupTable", condition)
            logger.debug("FN:DbWorkspaceMgr__delete_2ad_to_workspace delete_workspace_to_adgroupTable_sql:{}".format(sql))
            self.delete_exec(conn, sql)
            return response_code.SUCCESS
        except Exception as e:
            logger.error("FN:DbWorkspaceMgr__delete_2ad_to_workspace error:{}".format(traceback.format_exc()))
            return response_code.DELETE_DATA_FAIL
        finally:
            conn.close()

    def add_new_workspace_setting(self, workspace):
        conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()

            workspace_info = {}
            workspace_name = workspace['ws_name']
            workspace_info['des'] = workspace['ws_des']
            approval_item = workspace['approval'].split(',')
            workspace_info['head_approval'] = ''
            workspace_info['it_approval'] = ''
            for item_info in approval_item:
                if 'Head' in item_info:
                    workspace_info['head_approval'] = item_info
                if 'IT' in item_info:
                    workspace_info['it_approval'] = item_info
            workspace_info['cycle'] = workspace['cycle']
            workspace_info['group_dict'] = {}
            workspace_info['group_label'] = {}
            group_mapping = [
                (workspace['ws_team_group'], 'USER', 'ws_team_group'),
                (workspace['dg_group'], 'GOVERNOR', 'dg_group'),
                (workspace['it_group'], 'IT', 'it_group'),
                (workspace['ws_owner_group'], 'GOVERNOR', 'ws_owner_group'),
            ]
            for group_item in group_mapping:
                ad_group = group_item[0]
                role = group_item[1]
                label = group_item[2]
                if ad_group not in workspace_info['group_dict']:
                    workspace_info['group_dict'][ad_group] = set([role])
                else:
                    workspace_info['group_dict'][ad_group].add(role)
                if ad_group not in workspace_info['group_label']:
                    workspace_info['group_label'][ad_group] = set([label])
                else:
                    workspace_info['group_label'][ad_group].add(label)
            # workspace_info['group_dict'] = {workspace['ws_team_group']: ['admin'],
            #                                 workspace['dg_group']: ['GOVERNOR'],
            #                                 workspace['it_group']: ['IT'],
            #                                 workspace['ws_owner_group']: ['visitor']}
            # workspace_info['group_label'] = {workspace['ws_team_group']: 'ws_team_group',
            #                                  workspace['dg_group']: 'dg_group',
            #                                  workspace['it_group']: 'it_group',
            #                                  workspace['ws_owner_group']: 'ws_owner_group'}
            workspace_info['regions'] = workspace['regions']
            workspace_info['system'] = workspace['system']
            # workspace_info['gcp_project'] = workspace['gcp_project']
            # workspace_info['admin_sa'] = workspace['admin_sa']
            # workspace_info['admin_sa_path'] = workspace['admin_sa_path']
            workspace_info['workspace_name'] = workspace_name
            create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            workspace_info['create_time'] = create_time

            condition = 'WORKSPACE_NAME="%s"' % workspace_name
            sql = self.create_select_sql(db_name, 'workspaceTable', '*', condition)
            logger.debug("FN:DbWorkspaceMgr_add_new_workspace_setting workspaceTable_sql:{}".format(sql))
            workspace_infos = self.execute_fetch_all(conn, sql)
            if workspace_infos:
                data = response_code.ADD_DATA_FAIL
                data['msg'] = 'workspace exists.'
                return data

            workspace_insert = self.__set_workspace(workspace_info)
            team_resource = workspace.get('groupArr', [])
            logger.debug("FN:DbWorkspaceMgr_add_new_workspace_setting team_resource:{}".format(team_resource))
            _ = self.__set_team_resource(workspace_insert['data']['workspace_id'], team_resource)

            data = response_code.SUCCESS
            workspace['ws_id'] = workspace_insert['data']['workspace_id']
            data['data'] = workspace
            return data
        except Exception as e:
            logger.error("FN:DbWorkspaceMgr_add_new_workspace_setting error:{}".format(traceback.format_exc()))
            return response_code.GET_DATA_FAIL
        finally:
            conn.close()

    # get workspace info
    def get_workspace_info_by_ad_group(self, account_id):
        conn = MysqlConn()
        try:
            ad_group_list = Ldap.get_member_ad_group(account_id, Status.offline_flag)
            logger.debug("FN:DbWorkspaceMgr_get_workspace_info_by_ad_group ad_group_list:{}".format(ad_group_list))
            db_name = configuration.get_database_name()

            # check if the user is org admin
            org_admin = False
            for ad_group in ad_group_list:
                condition = 'GROUP_MAIL="%s"' % ad_group
                ad_group_fields = '*'
                sql = self.create_select_sql(db_name, 'adgroupTable', ad_group_fields, condition=condition)
                logger.debug("FN:DbWorkspaceMgr_get_workspace_info_by_ad_group adgroupTable_sql:{}".format(sql))
                ad_group_info = self.execute_fetch_one(conn, sql)
                if not ad_group_info:
                    continue
                # print('adgroup:', ad_group)
                ad_group_id = ad_group_info['ID']

                # get org permissions
                utils_role_set, permissions = user_mgr.__get_util_permission(ad_group_id, 'org_to_adgroupTable', 'ORG_ID',
                                                                         db_name, conn)
                # if 'admin' in utils_role_set:
                #     role_set = set(['admin'])
                # else:
                if 'admin' in utils_role_set:
                    org_admin = True
            if not org_admin:
                workspace_id_set = set()
                for ad_group_name in ad_group_list:
                    condition = "GROUP_MAIL='%s' " % (ad_group_name)
                    relations = [{"table_name": "workspace_to_adgroupTable",
                                  "join_condition": "workspace_to_adgroupTable.AD_GROUP_ID=adgroupTable.ID"}]
                    sql = self.create_get_relation_sql(db_name, 'adgroupTable', '*', relations, condition)
                    logger.debug("FN:DbWorkspaceMgr_get_workspace_info_by_ad_group workspace_to_adgroupTable_sql:{}".format(sql))
                    wp_ad_info = self.execute_fetch_all(conn, sql)
                    workspace_id_set = workspace_id_set | set([str(wp_ad['WORKSPACE_ID']) for wp_ad in wp_ad_info])
                if 'None' in workspace_id_set:
                    workspace_id_set.remove('None')
                if not workspace_id_set:
                    return response_code.GET_DATA_FAIL
                logger.debug("FN:DbWorkspaceMgr_get_workspace_info_by_ad_group workspace_id_set:{}".format(workspace_id_set))
                condition = 'ID in ({})'.format(','.join(workspace_id_set))

            else:
                condition = '1=1'
            db_name = configuration.get_database_name()
            sql = self.create_select_sql(db_name, 'workspaceTable', 'ID,WORKSPACE_NAME,REGIONS, CREATE_TIME', condition)
            logger.debug("FN:DbWorkspaceMgr_get_workspace_info_by_ad_group workspaceTable_sql:{}".format(sql))
            workspace_infos = self.execute_fetch_all(conn, sql)
            return_infos = []
            for index, workspace_info in enumerate(workspace_infos):
                workspace_id = workspace_info['ID']

                one_workspace = {'id': workspace_id, 'workspace_name': workspace_info['WORKSPACE_NAME'],
                                 'regions': json.loads(workspace_info['REGIONS']),
                                 'create_time': workspace_info['CREATE_TIME']}
                # db_name = configuration.get_database_name()
                condition = "WORKSPACE_ID='%s' " % (workspace_id)
                relations = [{"table_name": "adgroupTable",
                              "join_condition": "adgroupTable.ID=workspace_to_adgroupTable.AD_GROUP_ID"}]
                sql = self.create_get_relation_sql(db_name, 'workspace_to_adgroupTable', '*', relations, condition)
                logger.debug("FN:DbWorkspaceMgr_get_workspace_info_by_ad_group workspace_to_adgroupTable_sql:{}".format(sql))
                ad_group_infos = self.execute_fetch_all(conn, sql)
                for ad_group_info in ad_group_infos:
                    label_list = json.loads(ad_group_info['LABEL_LIST'])
                    for label in label_list:
                        one_workspace[label] = ad_group_info['GROUP_MAIL']
                return_infos.append(one_workspace)
                # workspace_infos[index]['AD_GROUP_LIST'] = ad_group_info

            data = response_code.SUCCESS
            data['data'] = return_infos
            return data
        except Exception as e:
            logger.error("FN:DbWorkspaceMgr_get_workspace_info_by_ad_group error:{}".format(traceback.format_exc()))
            return response_code.GET_DATA_FAIL
        finally:
            conn.close()

    # get workspace info
    def get_workspace_info_by_id(self, id):
        conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            condition = "ID=%s " % (id)
            sql = self.create_select_sql(db_name, 'workspaceTable', '*', condition)
            logger.debug("FN:DbWorkspaceMgr_get_workspace_info_by_id workspaceTable_sql:{}".format(sql))
            workspace_info = self.execute_fetch_one(conn, sql)
            if workspace_info:
                data = response_code.SUCCESS
                data['data'] = workspace_info
            else:
                data = response_code.GET_DATA_FAIL
            return data
        except Exception as e:
            logger.error("FN:DbWorkspaceMgr_get_workspace_info_by_id error:{}".format(traceback.format_exc()))
            return response_code.GET_DATA_FAIL
        finally:
            conn.close()

    # modify workspace info
    def update_workspace_info(self, workspace):
        conn = MysqlConn()
        try:
            workspace_id = workspace['id']
            data = self.get_workspace_info_by_id(workspace_id)
            if data['code'] != 200:
                data = response_code.UPDATE_DATA_FAIL
                data['msg'] = 'the workspace does not exists, update failed'
                return data

            workspace_info = {}
            workspace_name = workspace['ws_name']
            workspace_info['des'] = workspace['ws_des']

            workspace_approval = str(workspace['approval']).split(',')
            if len(workspace_approval) > 0:
                # There are 2 approvals
                for sentence in workspace_approval:
                    words = sentence.split(" ")
                    if words[2] == "IT":
                        workspace_info['it_approval'] = "Need workspace IT approval"
                        workspace_info['head_approval'] = ""
                    else:
                        workspace_info['it_approval'] = ""
                        workspace_info['head_approval'] = "Need workspace Head approval"

            else:
                # there are only one approval
                words = workspace_approval.split(" ")
                if len(words) > 0:
                    if words[2] == "IT":
                        workspace_info['it_approval'] = "Need workspace IT approval"
                        workspace_info['head_approval'] = ""
                    else:
                        workspace_info['it_approval'] = ""
                        workspace_info['head_approval'] = "Need workspace Head approval"
                else:
                    workspace_info['it_approval'] = ""
                    workspace_info['head_approval'] = ""
                
            # workspace_info['it_approval'], workspace_info['head_approval'] = str(workspace['approval']).split(',')
            workspace_info['cycle'] = workspace['cycle']
            workspace_info['group_dict'] = {}
            workspace_info['group_label'] = {}
            group_mapping = [
                (workspace['ws_team_group'], 'USER', 'ws_team_group'),
                (workspace['dg_group'], 'GOVERNOR', 'dg_group'),
                (workspace['it_group'], 'IT', 'it_group'),
                (workspace['ws_owner_group'], 'GOVERNOR', 'ws_owner_group'),
            ]
            for group_item in group_mapping:
                ad_group = group_item[0]
                role = group_item[1]
                label = group_item[2]
                if ad_group not in workspace_info['group_dict']:
                    workspace_info['group_dict'][ad_group] = set([role])
                else:
                    workspace_info['group_dict'][ad_group].add(role)
                if ad_group not in workspace_info['group_label']:
                    workspace_info['group_label'][ad_group] = set([label])
                else:
                    workspace_info['group_label'][ad_group].add(label)
            # workspace_info['group_dict'] = {workspace['ws_team_group']: ['admin'],
            #                                 workspace['dg_group']: ['GOVERNOR'],
            #                                 workspace['it_group']: ['IT'],
            #                                 workspace['ws_owner_group']: ['visitor']}
            # workspace_info['group_label'] = {workspace['ws_team_group']: 'ws_team_group',
            #                                  workspace['dg_group']: 'dg_group',
            #                                  workspace['it_group']: 'it_group',
            #                                  workspace['ws_owner_group']: 'ws_owner_group'}
            workspace_info['regions'] = workspace['regions']
            workspace_info['system'] = workspace['system']
            # workspace_info['gcp_project'] = workspace['gcp_project']
            # workspace_info['admin_sa'] = workspace['admin_sa']
            # workspace_info['admin_sa_path'] = workspace['admin_sa_path']
            workspace_info['workspace_name'] = workspace_name
            create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            workspace_info['create_time'] = create_time

            # Clear old AD records
            self.__delete_2ad_to_workspace(workspace_id)

            workspace_insert = self.__set_workspace(workspace_info, workspace_id)
            team_resource = workspace.get('groupArr', [])
            _ = self.__set_team_resource(workspace_id, team_resource)

            data = response_code.SUCCESS
            workspace['workspace_id'] = workspace_insert['data']['workspace_id']
            data['data'] = workspace
            return data
        except Exception as e:
            logger.error("FN:DbWorkspaceMgr_update_workspace_info error:{}".format(traceback.format_exc()))
            return response_code.GET_DATA_FAIL
        finally:
            conn.close()

    def delete_workspace_info(self, workspace):
        conn = MysqlConn()
        try:
            workspace_id = workspace['id']
            data = self.get_workspace_info_by_id(workspace_id)
            if data['code'] != 200:
                data = response_code.UPDATE_DATA_FAIL
                data['msg'] = 'the workspace does not exists, update failed'
                return data
            workspace['ws_name'] = data['data']['WORKSPACE_NAME']
            self.__delete_2ad_to_workspace(workspace_id)
            # self.__delete_workspace(workspace_id)
            # delete
            self.__delete_system_fields(workspace_id)
            data = response_code.SUCCESS
            data['data'] = workspace
            return data
        except Exception as e:
            logger.error("FN:DbWorkspaceMgr_delete_workspace_info error:{}".format(traceback.format_exc()))
            return response_code.GET_DATA_FAIL
        finally:
            conn.close()

    def get_workspace_details_info_by_id(self, workspace_id):
        from db.form.db_form_mgr import form_mgr
        conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            data = self.get_workspace_info_by_id(workspace_id)
            if data['code'] != 200:
                return response_code.GET_DATA_FAIL
            # # print(workspace_id_set)
            # print('data', data)
            logger.debug("FN:DbWorkspaceMgr_get_workspace_details_info_by_id data:{}".format(data))
            workspace_info = data['data']
            return_info = {}
            workspace_id = workspace_info['ID']
            return_info['id'] = workspace_id
            return_info['ws_name'] = workspace_info['WORKSPACE_NAME']
            return_info['ws_des'] = workspace_info['DES']
            return_info['cycle'] = workspace_info['RECERTIFICATION_CYCLE']
            IT_APPROVAL = workspace_info['IT_APPROVAL']
            HEAD_APPROVAL = workspace_info['HEAD_APPROVAL']
            approval_item = []
            if int(IT_APPROVAL) == 1:
                IT_APPROVAL = 'Need workspace IT approval'
                approval_item.append(IT_APPROVAL)
            if int(HEAD_APPROVAL) == 1:
                HEAD_APPROVAL = 'Need workspace Head approval'
                approval_item.append(HEAD_APPROVAL)
            return_info['approval'] = ','.join(approval_item)
            return_info['regions'] = json.loads(workspace_info['REGIONS'])
            # db_name = configuration.get_database_name()
            logger.debug("FN:DbWorkspaceMgr_get_workspace_details_info_by_id return_info:{}".format(return_info))
            condition = "WORKSPACE_ID='%s' " % (workspace_id)
            relations = [{"table_name": "adgroupTable",
                          "join_condition": "adgroupTable.ID=workspace_to_adgroupTable.AD_GROUP_ID"}]
            sql = self.create_get_relation_sql(db_name, 'workspace_to_adgroupTable', '*', relations, condition)
            logger.debug("FN:DbWorkspaceMgr_get_workspace_details_info_by_id workspace_to_adgroupTable_sql:{}".format(sql))
            ad_group_infos = self.execute_fetch_all(conn, sql)
            for ad_group_info in ad_group_infos:
                label_list = json.loads(ad_group_info['LABEL_LIST'])
                for label in label_list:
                    return_info[label] = ad_group_info['GROUP_MAIL']

            # # print(sql)
            system = {1: [], 2: [], 3: [], 4: [], 5: [], 6: []}
            dynamic = {1: [], 2: [], 3: [], 4: [], 5: [], 6: []}
            templateTypeList = form_mgr.get_field_template(0, workspace_id)
            # print('templateTypeList:', templateTypeList['data']['templateTypeList'][0]['fieldlist'])
            logger.debug("FN:DbWorkspaceMgr_get_workspace_details_info_by_id templateTypeList:{}".format(templateTypeList))
            for index, field_info in enumerate(templateTypeList['data']['templateTypeList'][0]['fieldlist']):
                field_style = int(field_info['style'])
                if field_style not in system:
                    system[field_style] = []
                system[field_style].append(field_info)
            for index, field_info in enumerate(templateTypeList['data']['templateTypeList'][-1]['fieldlist']):
                field_style = int(field_info['style'])
                if field_style not in dynamic:
                    dynamic[field_style] = []
                dynamic[field_style].append(field_info)
            return_info['system'] = system
            return_info['dynamic'] = dynamic

            # get usecase resource
            condition = "usecaseResourceTable.WORKSPACE_ID='%s' " % (workspace_id)
            relations = [
                {"table_name": "usecaseTable", "join_condition": "usecaseTable.id=usecaseResourceTable.USECASE_ID"}]
            sql = self.create_get_relation_sql(db_name, 'usecaseResourceTable', 'usecaseResourceTable.*, usecaseTable.USECASE_NAME',
                                               relations=relations, condition=condition)
            logger.debug("FN:DbWorkspaceMgr_get_workspace_details_info_by_id usecaseResourceTable_sql:{}".format(sql))
            return_uc_infos = self.execute_fetch_all(conn, sql)
            resource_infos = []
            for return_uc_info in return_uc_infos:
                resource_info = {'resource': None}
                # resource_json = {}
                for key in return_uc_info:
                    # if key.lower() == 'id':
                    #     resource_info['id'] = return_uc_info[key]
                    resource_info[key.lower()] = return_uc_info[key]
                # resource_info['resource'] = resource_json
                resource_list = [resource_info['OWNER_GROUP'.lower()],
                                 resource_info['TEAM_GROUP'.lower()],
                                 resource_info['SERVICE_ACCOUNT'.lower()],
                                 resource_info['LABEL'.lower()]]
                try:
                    del resource_info['OWNER_GROUP'.lower()]
                    del resource_info['TEAM_GROUP'.lower()],
                    del resource_info['SERVICE_ACCOUNT'.lower()],
                    del resource_info['LABEL'.lower()]
                except:
                    pass
                resource_info['resource'] = resource_list
                if resource_info['id'] != None:
                    resource_infos.append(resource_info)
            return_info['groupArr'] = resource_infos
            logger.debug("FN:DbWorkspaceMgr_get_workspace_details_info_by_id return_info:{}".format(return_info))
            data = response_code.SUCCESS
            data['data'] = return_info
            return data
        except Exception as e:
            logger.error("FN:DbWorkspaceMgr_get_workspace_details_info_by_id error:{}".format(traceback.format_exc()))
            return response_code.GET_DATA_FAIL
        finally:
            conn.close()

    def get_policy_tags_info(self, workspace_id):

        conn = MysqlConn()
        try:
            data = workspace_mgr.get_workspace_info_by_id(workspace_id)
            if data['code'] != 200:
                data = response_code.GET_DATA_FAIL
                data['msg'] = 'the workspace does not exists, get data failed'
                return data

            db_name = configuration.get_database_name()
            sql = self.create_select_sql(db_name, 'taxonomyTable', '*', condition='workspace_id="%s"' % workspace_id)
            logger.debug("FN:DbWorkspaceMgr_get_policy_tags_info taxonomyTable_sql:{}".format(sql))
            taxonomy_infos = self.execute_fetch_all(conn, sql)
            taxonomy_dict = {}
            for taxonomy_info in taxonomy_infos:
                local_taxonomy_id = taxonomy_info['id']
                if local_taxonomy_id not in taxonomy_dict:
                    taxonomy_info['taxonomy_display_name'] = taxonomy_info['display_name']
                    del taxonomy_info['display_name']
                    taxonomy_dict[local_taxonomy_id] = copy.deepcopy(taxonomy_info)
                    taxonomy_dict[local_taxonomy_id]['policy_tags_list'] = []
                sql = self.create_select_sql(db_name, 'policyTagsTable', '*',
                                             condition='local_taxonomy_id=%s order by id' % local_taxonomy_id)
                logger.debug("FN:DbWorkspaceMgr_get_policy_tags_info policyTagsTable_sql:{}".format(sql))
                policy_tags_infos = self.execute_fetch_all(conn, sql)
                # ret = []
                # o = {}
                # def add_node(ret, o, data):
                #     obj = data.copy()
                #     obj['sub_tags'] = []
                #     o[data['id']] = obj
                #     ret.append(obj)
                #     return ret, o
                #
                #
                # for edge in policy_tags_infos:
                #     if edge['parent_local_id'] in o:
                #         # print('11111111111111111', o)
                #         o[edge['parent_local_id']]['sub_tags'], o = add_node(o[edge['parent_local_id']]['sub_tags'], o, edge)
                #     else:
                #         ret, o = add_node(ret, o, edge)
                policy_tags_tree = []
                policy_tags_nodes = {}

                def add_node(tree, nodes, data):
                    obj = copy.deepcopy(data)
                    obj['taxonomy_display_name'] = taxonomy_info['taxonomy_display_name']
                    # obj['gcp_taxonomy_id'] = taxonomy_info['gcp_taxonomy_id']
                    del obj['parent_local_id']
                    del obj['local_taxonomy_id']
                    obj['sub_tags'] = []
                    nodes[data['id']] = obj
                    tree.append(obj)
                    return tree, nodes

                for policy_tags_info in policy_tags_infos:
                    logger.debug("FN:DbWorkspaceMgr_get_policy_tags_info policy_tags_info:{}".format(policy_tags_info))
                    if policy_tags_info['parent_local_id'] in policy_tags_nodes:
                        policy_tags_nodes[policy_tags_info['parent_local_id']]['sub_tags'], \
                        policy_tags_nodes = add_node(policy_tags_nodes[policy_tags_info['parent_local_id']]['sub_tags'],
                                                     policy_tags_nodes,
                                                     policy_tags_info)
                    else:
                        policy_tags_tree, policy_tags_nodes = add_node(policy_tags_tree,
                                                                       policy_tags_nodes,
                                                                       policy_tags_info)
                # new_policy_tags_nodes = policy_tags_nodes.copy()
                # for key in new_policy_tags_nodes:
                #     del new_policy_tags_nodes[key]['sub_tags']
                taxonomy_dict[local_taxonomy_id]['policy_tags_list'] = policy_tags_tree
                taxonomy_dict[local_taxonomy_id]['policy_tags_dict'] = policy_tags_nodes
            data = response_code.SUCCESS
            taxonomy_list = []
            for local_taxonomy_id in taxonomy_dict:
                taxonomy_list.append(taxonomy_dict[local_taxonomy_id])
            data['data'] = taxonomy_list

            return data
        except Exception as e:
            logger.error("FN:DbWorkspaceMgr_get_policy_tags_info error:{}".format(traceback.format_exc()))
            return response_code.GET_DATA_FAIL
        finally:
            conn.close()

    # def add_new_policy_tags(self, policy_tags):
    #
    #     conn = MysqlConn()
    #     try:
    #         workspace_id = policy_tags['workspace_id']
    #         data = workspace_mgr.get_workspace_info_by_id(workspace_id)
    #         if data['code'] != 200:
    #             data = response_code.UPDATE_DATA_FAIL
    #             data['msg'] = 'the workspace does not exists, update failed'
    #             return data
    #
    #         db_name = configuration.get_database_name()
    #         policy_tags_info = {'parent_local_id': '', 'gcp_policy_tag_id': '',
    #                             'input_form_id': policy_tags['input_form_id']}
    #         display_name = policy_tags['policy_name']
    #         policy_tags_info['workspace_id'] = policy_tags['workspace_id']
    #         policy_tags_info['ad_group'] = policy_tags['policy_approval_ad_group']
    #         policy_tags_info['display_name'] = display_name
    #         policy_tags_info['creator_id'] = policy_tags['creator_id']
    #         policy_tags_info['description'] = policy_tags['policy_description']
    #
    #         create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #         policy_tags_info['create_time'] = create_time
    #
    #         group_mapping = [
    #             (policy_tags['uc_team_group'], 'vistor', 'uc_team_group'),
    #             (policy_tags['uc_owner_group'], 'admin', 'uc_owner_group'),
    #         ]
    #         for group_item in group_mapping:
    #             ad_group = group_item[0]
    #             role = group_item[1]
    #             label = group_item[2]
    #             if ad_group not in policy_tags_info['group_dict']:
    #                 policy_tags_info['group_dict'][ad_group] = [role]
    #             else:
    #                 policy_tags_info['group_dict'][ad_group].append(role)
    #             if ad_group not in policy_tags_info['group_label']:
    #                 policy_tags_info['group_label'][ad_group] = [label]
    #             else:
    #                 policy_tags_info['group_label'][ad_group].append(label)
    #
    #         condition = 'display_name="%s"' % display_name
    #         sql = self.create_select_sql(db_name, 'policyTagsTable', '*', condition)
    #         # print('policy_tagsTable: ', sql)
    #         policy_tags_infos = self.execute_fetch_all(conn, sql)
    #         if policy_tags_infos:
    #             data = response_code.ADD_DATA_FAIL
    #             data['msg'] = 'policy tags already existed'
    #             return data
    #         # print("policy_tags_info: ", policy_tags_info)
    #         policy_tags_insert = self.__set_policy_tags(policy_tags_info)
    #         data = response_code.SUCCESS
    #         policy_tags['policy_tags_id'] = policy_tags_insert['data']['policy_tags_id']
    #         data['data'] = policy_tags
    #         return data
    #     except Exception as e:
    #         lg.error(e)
    #         import traceback
    #         # print(traceback.format_exc())
    #         return response_code.GET_DATA_FAIL
    #     finally:
    #         conn.close()

    def get_tag_template_info(self, workspace_id):

        conn = MysqlConn()
        try:
            data = workspace_mgr.get_workspace_info_by_id(workspace_id)
            if data['code'] != 200:
                data = response_code.UPDATE_DATA_FAIL
                data['msg'] = 'the workspace does not exists, get tag template failed'
                return data

            db_name = configuration.get_database_name()
            sql = self.create_select_sql(db_name, 'tagTemplatesTable',
                                         'input_form_id,display_name,workspace_id,tag_template_id,description,project_id,location,'
                                         'tag_template_form_id,creator_id,create_time',
                                         condition='workspace_id="%s" or workspace_id=0' % workspace_id)
            logger.debug("FN:DbWorkspaceMgr_get_tag_template_info tagTemplatesTable_sql:{}".format(sql))
            taxonomy_infos = self.execute_fetch_all(conn, sql)

            data = response_code.SUCCESS
            data['data'] = taxonomy_infos

            return data
        except Exception as e:
            logger.error("FN:DbWorkspaceMgr_get_tag_template_info error:{}".format(traceback.format_exc()))
            return response_code.GET_DATA_FAIL
        finally:
            conn.close()


    def get_usecase_resource(self, workspace_id):

        conn = MysqlConn()
        try:
            data = workspace_mgr.get_workspace_info_by_id(workspace_id)
            if data['code'] != 200:
                data = response_code.UPDATE_DATA_FAIL
                data['msg'] = 'the workspace does not exists, get tag template failed'
                return data

            db_name = configuration.get_database_name()
            sql = self.create_select_sql(db_name, 'usecaseResourceTable',
                                         '*',
                                         condition='(WORKSPACE_ID="%s" or WORKSPACE_ID=0) and AVAILABLE=1' % workspace_id)
            logger.debug("FN:DbWorkspaceMgr_get_usecase_resource usecaseResourceTable_sql:{}".format(sql))
            return_infos = self.execute_fetch_all(conn, sql)
            resource_infos = []
            for return_uc_info in return_infos:
                resource_info = {'id': None, 'resource': None}
                resource_json = {}
                for key in return_uc_info:
                    if key.lower() == 'id':
                        resource_info['id'] = return_uc_info[key]
                    resource_json[key.lower()] = return_uc_info[key]
                resource_info['resource'] = resource_json
                if resource_info['id'] != None:
                    resource_infos.append(resource_info)
            # return_info['groupArr'] = resource_infos

            data = response_code.SUCCESS
            data['data'] = resource_infos
            return data
        except Exception as e:
            logger.error("FN:DbWorkspaceMgr_get_usecase_resource error:{}".format(traceback.format_exc()))
            return response_code.GET_DATA_FAIL
        finally:
            conn.close()

workspace_mgr = DbWorkspaceMgr()
