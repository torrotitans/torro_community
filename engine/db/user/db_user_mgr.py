#!/usr/bin/python
# -*- coding: UTF-8 -*

from utils.ldap_helper import Ldap
from db.base import DbBase
from db.connection_pool import MysqlConn
import traceback
from utils.status_code import response_code
from config import configuration
from werkzeug.security import generate_password_hash, check_password_hash
import json
import traceback
import logging

logger = logging.getLogger("main." + __name__)

class DbUserMgr(DbBase):
    """
    DB operation for user related
    """
    '''
    0.Default has an admin account from the org table
    1.Login with the default admin account
    2.Setup the org with LDAP login
    3.Log onto role selection page；
    4.Select the role for the current operation；
    5.Depends on the role selection，calling api will determine the privilege based on the role ；
    
    1. ui ->org login_type
    2. api-> role_list+token
    3. token+role ->permisson+token
    '''
    manager_role = ['IT', 'GOVERNOR', 'ADMIN']
    # login then return org info + user role + user token
    def get_org_info(self):
        pass

    def get_user_role(self):
        pass

    def get_user_permisson_by_role_id(self):
        pass

    def get_user_by_id(self, id):
        # logger.debug("FN:get_user_by_id user_id:{}".format(id))
        conn = MysqlConn()
        try:
            condition = "id='%s'" % id
            db_name = configuration.get_database_name()
            sql = self.create_select_sql(db_name, 'userTable', '*', condition=condition)
            # logger.debug("FN:get_user_by_id sql:".format(sql))
            data = response_code.SUCCESS
            user_info = self.execute_fetch_one(conn, sql)
            data['data'] = user_info
            return data
        except Exception as e:
            logger.error("FN:get_user_by_id error:{}".format(traceback.format_exc()))
            return response_code.GET_DATA_FAIL
        finally:
            conn.close()

    def get_user_by_name(self, cn_name, ldap_usernames=(None,None), ad_group_list=None):

        logger.debug("FN:get_user_by_name account_cn:".format(cn_name))
        conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            # db_name2 = configuration.get_database_name('DB')
            user_mail = ldap_usernames[0]
            user_display_name = ldap_usernames[1]
            condition = 'ACCOUNT_CN="%s"' % cn_name
            user_fields = '*'
            sql = self.create_select_sql(db_name, 'userTable', user_fields, condition=condition)
            logger.debug("FN:get_user_by_name sql:".format(sql))
            user_info = self.execute_fetch_one(conn, sql)
            logger.debug('FN:get_user_by_name user_info:{} ad_group_list:{}'.format(user_info, ad_group_list))

            # if exist, update ad_group_list
            user_id = None
            if user_info and ad_group_list:
                user_id = user_info['ID']
                fields = ('GROUP_LIST',)
                values = (json.dumps(ad_group_list).replace('\\', '\\\\'),)
                # update recount
                sql = self.create_update_sql(db_name, 'userTable', fields, values, condition)
                logger.debug("FN:get_user_by_name update_sql:".format(sql))
                return_count = self.updete_exec(conn, sql)

            if (not user_info) and user_mail:
                import datetime
                if not ad_group_list:
                    ad_group_list = []
                now = str(datetime.datetime.today())
                user_info = {'ACCOUNT_NAME': user_display_name, 'ACCOUNT_ID': ldap_usernames[0], 'PASS_WORD': 'ldap_login',
                             'ACCOUNT_CN': cn_name,
                             'CREATE_TIME': now, 'DES': 'new user'}
                fields = list(user_info.keys())
                values = tuple(user_info.values())
                sql = self.create_insert_sql(db_name, 'userTable', '({})'.format(', '.join(fields)), values)
                logger.debug("FN:get_user_by_name userTable_insert_sql:".format(sql))
                user_id = self.insert_exec(conn, sql, return_insert_id=True)
                user_info['ID'] = user_id
            # add ad_group
            if ad_group_list is not None and user_id is not None:
                condition = 'USER_ID="%s"' % user_id
                sql = self.create_delete_sql(db_name, 'user_to_adgroupTable', condition=condition)
                logger.debug('FN:get_user_by_name user_to_adgroupTable_delete_sql:{}'.format(sql))
                _ = self.execute_del_data(conn, sql)
                ad_group_id_list = []
                for ad_group in ad_group_list:
                    condition = 'GROUP_MAIL="%s"' % ad_group
                    ad_group_fields = '*'
                    sql = self.create_select_sql(db_name, 'adgroupTable', ad_group_fields, condition=condition)
                    logger.debug("FN:get_user_by_name getAdGroupById_sql:{}".format(sql))
                    ad_group_info = self.execute_fetch_one(conn, sql)
                    if ad_group_info:
                        ad_group_id_list.append(ad_group_info['ID'])
                for ad_group_id in ad_group_id_list:
                    fields = ('USER_ID', 'AD_GROUP_ID')
                    values = (user_id, ad_group_id)
                    user_to_adgroup_insert_sql = self.create_insert_sql(db_name, 'user_to_adgroupTable', '({})'.format(', '.join(fields)), values)
                    logger.debug('FN:get_user_by_name user_to_adgroup_insert_sql:{}'.format(user_to_adgroup_insert_sql))
                    self.insert_exec(conn, user_to_adgroup_insert_sql, return_insert_id=True)
            data = response_code.SUCCESS
            data['data'] = user_info
            return data
        except Exception as e:
            logger.error("FN:get_user_by_name error:{}".format(traceback.format_exc()))
            return response_code.GET_DATA_FAIL
        finally:
            conn.close()

    def update_user_password(self, name, new_password):

        conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            # db_name2 = configuration.get_database_name('DB')
            condition = 'ACCOUNT_CN="%s"' % name
            fields = ('PASS_WORD',)
            values = (new_password,)
            # update workflow
            sql = self.create_update_sql(db_name, 'userTable', fields, values, condition)
            logger.debug('FN:update_user_password update_sql:{}'.format(sql))
            return_count = self.updete_exec(conn, sql)
            data = response_code.SUCCESS
            data['data'] = {'count': return_count}
            return data
        except Exception as e:
            logger.error("FN:update_user_password error:{}".format(traceback.format_exc()))
            return response_code.GET_DATA_FAIL
        finally:
            conn.close()

    def __get_util_permission(self, ad_group_id, table_name, table_id_field_name, db_name, conn):
        condition = 'AD_GROUP_ID="%s"' % ad_group_id
        utils_fields = '*'
        sql = self.create_select_sql(db_name, table_name, utils_fields, condition=condition)
        logger.debug('FN:__get_util_permission sql:{}'.format(sql))
        utils_info = self.execute_fetch_one(conn, sql)
        if utils_info:
            utils_permissions = {}
            utils_id = str(utils_info[table_id_field_name])
            role_list = json.loads(utils_info['ROLE_LIST'], strict=False)
            utils_permissions[utils_id] = {}
            for role_name in role_list:
                condition = 'NAME="%s"' % role_name
                role_fields = '*'
                sql = self.create_select_sql(db_name, 'roleTable', role_fields, condition=condition)
                logger.debug('FN:__get_util_permission roleTable_sql:{}'.format(sql))
                role_info = self.execute_fetch_one(conn, sql)
                api_permission_list = json.loads(role_info['API_PERMISSION_LIST'], strict=False)
                for i in range(len(api_permission_list)):
                    api_permission_list[i] = api_permission_list[i].lower()
                utils_permissions[utils_id][role_name] = api_permission_list
            return set(role_list), utils_permissions
        else:
            return set(), {}

    def get_user_permissions(self, id, ad_group_list):

        conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            # db_name2 = configuration.get_database_name('DB')
            condition = 'ID="%s"' % id
            user_fields = '*'
            sql = self.create_select_sql(db_name, 'userTable', user_fields, condition=condition)
            logger.debug('FN:get_user_permissions userTable_sql:{}'.format(sql))
            user_info = self.execute_fetch_one(conn, sql)
            user_info['permissions'] = {'usecase': {}, 'workspace': {}, 'org': {}}
            org_admin = False
            role_set = set()
            workspace_id_set = set()

            if user_info:
                condition = 'USER_ID="%s"' % id
                relation_tables = [
                    {'table_name': 'adgroupTable', 'join_condition': 'adgroupTable.ID=user_to_adgroupTable.AD_GROUP_ID'}
                ]
                sql = self.create_get_relation_sql(db_name, 'user_to_adgroupTable', 'GROUP_MAIL', relations=relation_tables, condition=condition)
                ad_group_infos = self.execute_fetch_all(conn, sql)
                group_list = []
                for ad_group in ad_group_infos:
                    group_list.append(ad_group['GROUP_MAIL'])
                user_info['GROUP_LIST'] = group_list
                logger.debug('FN:get_user_permissions group_list:{}'.format(group_list))

                for ad_group in ad_group_list:
                    condition = 'GROUP_MAIL="%s"' % ad_group
                    ad_group_fields = '*'
                    sql = self.create_select_sql(db_name, 'adgroupTable', ad_group_fields, condition=condition)
                    logger.debug('FN:get_user_permissions adgroupTable_sql:{}'.format(sql))
                    ad_group_info = self.execute_fetch_one(conn, sql)
                    if not ad_group_info:
                        continue

                    ad_group_id = ad_group_info['ID']

                    # get org permissions
                    utils_role_set, permissions = self.__get_util_permission(ad_group_id, 'org_to_adgroupTable', 'ORG_ID', db_name, conn)
                    # if 'admin' in utils_role_set:
                    #     role_set = set(['admin'])
                    # else:
                    role_set = utils_role_set | role_set
                    if 'admin' in role_set:
                        org_admin = True
                        
                    logger.debug('FN:get_user_permissions org_permission:{}'.format(permissions))

                    for item_id in permissions:
                        item_id = str(item_id)
                        if item_id in user_info['permissions']['org']:
                            for role_name in permissions[item_id]:
                                role_permissions = user_info['permissions']['org'][item_id].get(role_name, [])
                                role_permissions = list(set(role_permissions + permissions[item_id][role_name]))
                                user_info['permissions']['org'][item_id][role_name] = role_permissions
                        else:
                            user_info['permissions']['org'][item_id] = permissions[item_id]
                    if org_admin:
                        # get workspace id
                        condition = '1=1'
                        workspace_id_field = 'WORKSPACE_ID'
                        sql = self.create_select_sql(db_name, 'workspace_to_adgroupTable', workspace_id_field,
                                                     condition=condition)
                        logger.debug('FN:get_user_permissions org_admin_workspace_to_adgroupTable_sql:{}'.format(sql))
                        workspace_id_dict = self.execute_fetch_all(conn, sql)
                        logger.debug('FN:get_user_permissions org_admin_workspace_id_dict:{}'.format(workspace_id_dict))
                        workspace_id_set = workspace_id_set | set([item['WORKSPACE_ID'] for item in workspace_id_dict])
                        
                        # workspace permissions up to all
                        logger.debug('FN:get_user_permissions org_admin_workspace_permissions:{}'.format(permissions))
                        for item_id in workspace_id_set:
                            item_id = str(item_id)
                            if item_id not in user_info['permissions']['workspace']:
                                user_info['permissions']['workspace'][item_id] = {'admin': ['*-*']}

                    else:
                        # get workspace id
                        condition = 'AD_GROUP_ID="%s"' % ad_group_id
                        workspace_id_field = 'WORKSPACE_ID'
                        sql = self.create_select_sql(db_name, 'workspace_to_adgroupTable', workspace_id_field, condition=condition)
                        logger.debug('FN:get_user_permissions non_org_admin_workspace_to_adgroupTable_sql:{}'.format(sql))
                        workspace_id_dict = self.execute_fetch_all(conn, sql)
                        logger.debug('FN:get_user_permissions non_org_admin_workspace_id_dict:{}'.format(workspace_id_dict))
                        workspace_id_set = workspace_id_set | set([item['WORKSPACE_ID'] for item in workspace_id_dict])

                        # get workspace permissions
                        logger.debug("fn:get_user_permissions id:{}, ad_group_id:{}".format(id,ad_group_id))
                        utils_role_set, permissions = self.__get_util_permission(ad_group_id, 'workspace_to_adgroupTable', 'WORKSPACE_ID', db_name, conn)
                        # role_set = utils_role_set | role_set
                        logger.debug('FN:get_user_permissions non_org_admin_workspace_permissions:{}'.format(permissions))
                        for item_id in permissions:
                            item_id = str(item_id)
                            if item_id in user_info['permissions']['workspace']:
                                for role_name in permissions[item_id]:
                                    role_permissions = user_info['permissions']['workspace'][item_id].get(role_name, [])
                                    role_permissions = list(set(role_permissions + permissions[item_id][role_name]))
                                    user_info['permissions']['workspace'][item_id][role_name] = role_permissions
                            else:
                                user_info['permissions']['workspace'][item_id] = permissions[item_id]
                    # get usecase permissions
                    utils_role_set, permissions = self.__get_util_permission(ad_group_id, 'usecase_to_adgroupTable', 'USECASE_ID', db_name, conn)
                    # role_set = utils_role_set | role_set
                    logger.debug('FN:get_user_permissions usecase_to_adgroupTable_permissions:{}'.format(permissions))
                    for item_id in permissions:
                        item_id = str(item_id)
                        if item_id in user_info['permissions']['usecase']:
                            for role_name in permissions[item_id]:
                                role_permissions = user_info['permissions']['usecase'][item_id].get(role_name, [])
                                role_permissions = list(set(role_permissions + permissions[item_id][role_name]))
                                user_info['permissions']['usecase'][item_id][role_name] = role_permissions
                        else:
                            user_info['permissions']['usecase'][item_id] = permissions[item_id]

                logger.debug('FN:get_user_permissions workspace_id_set:{}'.format(workspace_id_set))
                workspace_list = list(workspace_id_set)
                logger.debug('FN:get_user_permissions workspace_list:{}'.format(workspace_list))
                
                if len(workspace_list) != 0:
                    user_info['workspace_list'] = []
                    user_info['workspace_id'] = str(workspace_list[0])
                    condition = 'ID in (%s)' % ','.join([str(w) for w in workspace_list])
                    workspace_info_field = 'ID,WORKSPACE_NAME'
                    sql = self.create_select_sql(db_name, 'workspaceTable', workspace_info_field, condition=condition)
                    logger.debug('FN:get_user_permissions workspaceTable_sql:{}'.format(sql))
                    workspace_name_dict = self.execute_fetch_all(conn, sql)
                    for workspace in workspace_name_dict:
                        user_info['workspace_list'].append({'label': workspace['WORKSPACE_NAME'],
                                                            'value': workspace['ID']})
                    workspace_id = str(user_info['workspace_id'])
                    user_info['role_list'] = []
                    user_info['user_role'] = ''
                    if workspace_id in user_info['permissions']['workspace']:
                        for role_name in user_info['permissions']['workspace'][workspace_id]:
                            user_info['role_list'].append(role_name)
                        if len(user_info['role_list']) == 0:
                            user_info['user_role'] = ''
                        elif len(user_info['role_list']) == 1:
                            user_info['user_role'] = user_info['role_list'][0]
                else:

                    user_info['workspace_id'] = ''
                    user_info['workspace_list'] = []
                    user_info['role_list'] = []
                    user_info['user_role'] = ''


                if org_admin:
                    user_info['role_list'] = ['admin']
                    user_info['user_role'] = 'admin'
                # else:
                #     if len(role_set) == 1:
                #         user_info['user_role'] = user_info['role_list'][0]
                #     else:
                #         user_info['user_role'] = ''
                #         # no need the viewer role
                #         if 'viewer' in user_info['role_list']:
                #             user_info['role_list'].remove('viewer')

                logger.debug("FN:get_user_permissions user_info['workspace_list']: {}".format(user_info['workspace_list']))
                return user_info
            else:
                return {}
        except Exception as e:
            logger.error("FN:get_user_permissions error:{}".format(traceback.format_exc()))
            return response_code.GET_DATA_FAIL
        finally:
            conn.close()

    def fetch_user_info(self, user_key, wp_id=0, ad_group_list=None):
        conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            # db_name2 = configuration.get_database_name('DB')
            condition = 'ID="%s"' % user_key
            user_fields = '*'
            sql = self.create_select_sql(db_name, 'userTable', user_fields, condition=condition)
            user_info = self.execute_fetch_one(conn, sql)
            if ad_group_list is None:
                ad_group_list = []
                condition = 'USER_ID="%s"' % user_key
                relation_tables = [
                    {'table_name': 'user_to_adgroupTable', 'join_condition': 'adgroupTable.ID=user_to_adgroupTable.AD_GROUP_ID'},
                ]
                sql = self.create_get_relation_sql(db_name, 'adgroupTable', 'GROUP_MAIL',
                                                   relations=relation_tables, condition=condition)
                logger.debug('FN:fetch_user_info create_get_relation_sql:{}'.format(sql))
                ad_group_infos = self.execute_fetch_all(conn, sql)
                for ad_group in ad_group_infos:
                    ad_group_list.append(ad_group['GROUP_MAIL'])
            logger.debug('FN:fetch_user_info ad_group_list:{}'.format(ad_group_list))
            permissions = {'org': {}, 'usecase': {}, 'workspace': {}}
            logger.debug('FN:fetch_user_info user_info:{}'.format(user_info))

            user_set = set()
            user_set.add(str(user_key))
            user_fields = 'ID'
            if user_info:
                for ad_group in ad_group_list:
                    condition = 'GROUP_MAIL="%s"' % ad_group
                    ad_group_fields = '*'
                    sql = self.create_select_sql(db_name, 'adgroupTable', ad_group_fields, condition=condition)
                    logger.debug('FN:fetch_user_info adgroupTable_sql:{}'.format(sql))
                    ad_group_info = self.execute_fetch_one(conn, sql)
                    ad_group_id = ad_group_info['ID']
                    # get org permissions
                    utils_role_set, org_permissions = self.__get_util_permission(ad_group_id, 'org_to_adgroupTable', 'ORG_ID', db_name, conn)
                    logger.debug('FN:fetch_user_info org_permissions:{}'.format(org_permissions))
                    permissions['org'] = org_permissions
                    for org_id in org_permissions:
                        for role in org_permissions[org_id]:
                            if role in self.manager_role:
                                sql = self.create_select_sql(db_name, 'userTable', user_fields)
                                logger.debug('FN:fetch_user_info userTable_sql:{}'.format(sql))
                                users_info = self.execute_fetch_all(conn, sql)
                                sub_user_set = set([str(user['ID']) for user in users_info])
                                user_set = user_set | sub_user_set
                                break
                    # get workspace permissions
                    utils_role_set, workspace_permissions = self.__get_util_permission(ad_group_id, 'workspace_to_adgroupTable', 'WORKSPACE_ID', db_name, conn)
                    permissions['workspace'] = workspace_permissions
                    if wp_id in permissions['workspace']:
                        for role in permissions['workspace'][wp_id]:
                            if role in self.manager_role:
                                GROUP_MAIL = ad_group_info['GROUP_MAIL']
                                memeber_list, _ = Ldap.get_ad_group_member(GROUP_MAIL)
                                user_condiction = 'ACCOUNT_NAME in ("%s")' % '","'.join(memeber_list)
                                sql = self.create_select_sql(db_name, 'userTable', user_fields, user_condiction)
                                logger.debug('FN:fetch_user_info userTable_sql:{}'.format(sql))
                                users_info = self.execute_fetch_all(conn, sql)
                                sub_user_set = set([str(user['ID']) for user in users_info])
                                user_set = user_set | sub_user_set
                                break
                    # # get usecase permissions
                    # utils_role_set, usecase_permissions = self.__get_util_permission('usecase_to_adgroupTable', ad_group_id, db_name, conn)
                    # permissions['usecase'] = usecase_permissions
                    # if uc_id in permissions['usecase'] and permissions['usecase'][wp_id] in (
                    #         'IT', 'GOVERNOR', 'admin'):
                    #     GROUP_MAIL = ad_group_info['GROUP_MAIL']
                    #     memeber_list, _ = Ldap.get_ad_group_member(GROUP_MAIL)
                    #     user_condiction = 'ACCOUNT_NAME in ("%s")' % '","'.join(memeber_list)
                    #     sql = self.create_select_sql(db_name, 'userTable', user_fields, user_condiction)
                    #     users_info = self.execute_fetch_all(conn, sql)
                    #     sub_user_set = set([str(user['ID']) for user in users_info])
                    #     user_set = user_set | sub_user_set

                # for org_id in permissions['org']:
                #     if permissions['org'][org_id] in ('IT', 'GOVERNOR', 'admin'):
                #         sql = self.create_select_sql(db_name, 'userTable', user_fields)
                #         users_info = self.execute_fetch_all(conn, sql)
                #         sub_user_set = set([str(user['ID']) for user in users_info])
                #         user_set = user_set | sub_user_set
                #         break
                # # for workspace_id in permissions['workspace']:
                # #     if permissions['workspace'][workspace_id] in ('IT', 'GOVERNOR', 'admin'):
                # if wp_id in permissions['workspace'] and permissions['workspace'][wp_id] in ('IT', 'GOVERNOR', 'admin'):
                #         user_condiction = 'WORKSPACE_ID="%s"' % wp_id
                #         sql = self.create_select_sql(db_name, 'userTable', user_fields, user_condiction)
                #         users_info = self.execute_fetch_all(conn, sql)
                #         sub_user_set = set([user['ID'] for user in users_info])
                #         user_set = user_set | sub_user_set
                # # for usecase_id in permissions['usecase']:
                # #     if permissions['usecase'][usecase_id] in ('IT', 'GOVERNOR', 'admin'):
                # if uc_id in permissions['usecase'] and permissions['usecase'][wp_id] in (
                #         'IT', 'GOVERNOR', 'admin'):
                #         user_condiction = 'USECASE_ID="%s"' % uc_id
                #         sql = self.create_select_sql(db_name, 'userTable', user_fields, user_condiction)
                #         users_info = self.execute_fetch_all(conn, sql)
                #         sub_user_set = set([user['ID'] for user in users_info])
                #         user_set = user_set | sub_user_set
                logger.debug('FN:fetch_user_info user_set:{}'.format(user_set))
                user_condiction = 'ID in(%s)' % ','.join(user_set)
                user_fields = '*'
                sql = self.create_select_sql(db_name, 'userTable', user_fields, user_condiction)
                logger.debug('FN:fetch_user_info userTable_sql:{}'.format(sql))
                users_info = self.execute_fetch_all(conn, sql)
                for i in range(len(users_info)):
                    user_id = users_info[i]['ID']
                    ad_group_list = []
                    condition = 'USER_ID="%s"' % user_id
                    relation_tables = [
                        {'table_name': 'user_to_adgroupTable',
                         'join_condition': 'adgroupTable.ID=user_to_adgroupTable.AD_GROUP_ID'},
                    ]
                    sql = self.create_get_relation_sql(db_name, 'adgroupTable', 'GROUP_MAIL',
                                                       relations=relation_tables, condition=condition)
                    ad_group_infos = self.execute_fetch_all(conn, sql)
                    for ad_group in ad_group_infos:
                        ad_group_list.append(ad_group['GROUP_MAIL'])
                    users_info[i]['GROUP_LIST'] = ad_group_list
                    del users_info[i]['PASS_WORD']
                data = response_code.SUCCESS
                data['data'] = users_info
                return data
            else:
                return response_code.GET_DATA_FAIL
        except Exception as e:
            logger.error("FN:fetch_user_info error:{}".format(traceback.format_exc()))
            return response_code.GET_DATA_FAIL
        finally:
            conn.close()

    def offline_login(self, username, password):
        conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            # db_name2 = configuration.get_database_name('DB')
            condition = 'ACCOUNT_ID="%s" and PASS_WORD="%s"' % (username, password)
            user_fields = '*'
            sql = self.create_select_sql(db_name, 'userTable', user_fields, condition=condition)
            user_info = self.execute_fetch_one(conn, sql)
            if not user_info:
                return None, (None, None)
            ad_group_list = json.loads(user_info.get('GROUP_LIST', '[]'), strict=False)
            ldap_username = user_info.get('ACCOUNT_NAME', None)
            user_mail = user_info.get('ACCOUNT_ID', None)

            return ad_group_list, (user_mail, ldap_username)
        except Exception as e:
            import traceback
            logger.error("FN:offline_login error:{}".format(traceback.format_exc()))
            return None, (None, None)
        finally:
            conn.close()


user_mgr = DbUserMgr()
