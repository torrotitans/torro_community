#!/usr/bin/python
# -*- coding: UTF-8 -*

from utils.ldap_helper import Ldap
from db.base import DbBase
from db.connection_pool import MysqlConn
from utils.log_helper import lg
import traceback
from utils.status_code import response_code
from config import configuration

from werkzeug.security import generate_password_hash, check_password_hash
import json

class DbUserMgr(DbBase):
    """
    用户相关数据库表操作类
    """
    '''
    0.为用户配置一个最初的admin账号，且orgTable表有一条除id和admin_id外全为空的record；（开启后端时首先判断一下user和org表是否存在，不存在创建并插入default的record）
    1.进入登录界面：
    *第一次用给定的admin账号和密码登录；
    2.前端获取org_name名字并设置在导航页面：
    如果org_name为空，则立即跳转到org设置页面配置：
          -- 填写org基本信息
          -- 选择密码登录/ldap
          -- 重新创建admin账号/配置ldap+设置admin email
          -- 删除默认账号
    如果org_name不为空，判断login_type：
        if login_type is base，login旁出现注册按钮，可供用户注册填写信息并获得最基本的viewer账号；
        if login_type is ladp，login旁没有注册按钮，登录后自动获得基本viewer权限，且根据ldap ADDITIONAL_SEARCH_FILTER_FIELD_LIST拿到用户信息；
        if login_type is github outh，......
    3.登录到选择角色界面；
    4.选择角色后设置当前角色并获得角色权限列表；
    5.根据角色名显示页面，call api时根据权限列表判断权限；
    
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
        """
        通过id获取用户
        :return:
        """
        conn = MysqlConn()
        try:
            condition = "id='%s'" % id
            db_name = configuration.get_database_name()
            sql = self.create_select_sql(db_name, 'userTable', '*', condition=condition)
            data = response_code.SUCCESS
            user_info = self.execute_fetch_one(conn, sql)
            data['data'] = user_info
            return data
        except Exception as e:
            lg.error(e)
            return response_code.GET_DATA_FAIL
        finally:
            conn.close()

    def get_user_by_name(self, cn_name, ldap_usernames=(None,None), ad_group_list=None):
        """
        get user info through account_name
        :param cn_name:
        :return:
        """
        conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            # db_name2 = configuration.get_database_name('DB')
            user_mail = ldap_usernames[0]
            user_display_name = ldap_usernames[1]
            condition = 'ACCOUNT_CN="%s"' % cn_name
            user_fields = '*'
            sql = self.create_select_sql(db_name, 'userTable', user_fields, condition=condition)
            user_info = self.execute_fetch_one(conn, sql)
            print('FN:get_user_by_name user_info:', user_info)
            print('FN:get_user_by_name ad_group_list: ', ad_group_list)
            # print((user_info and ad_group_list), (user_info and ldap_username))
            # if exist, update ad_group_list
            user_id = None
            if user_info and ad_group_list:
                user_id = user_info['ID']
                # fields = ('GROUP_LIST',)
                # values = (json.dumps(ad_group_list),)
                # # update workflow
                # sql = self.create_update_sql(db_name, 'userTable', fields, values, condition)
                # print('update_sql: ', sql)
                # return_count = self.updete_exec(conn, sql)
                # # print('return_count: ', return_count)
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
                print('FN:get_user_by_name userTable_insert_sql:', sql)
                user_id = self.insert_exec(conn, sql, return_insert_id=True)
                user_info['ID'] = user_id
            # add ad_group
            if ad_group_list is not None and user_id is not None:
                condition = 'USER_ID="%s"' % user_id
                sql = self.create_delete_sql(db_name, 'user_to_adgroupTable', condition=condition)
                print('FN:get_user_by_name user_to_adgroupTable_delete_sql:', sql)
                _ = self.execute_del_data(conn, sql)
                ad_group_id_list = []
                for ad_group in ad_group_list:
                    print("FN:get_user_by_name getAdGroupById:",ad_group)
                    condition = 'GROUP_MAIL="%s"' % ad_group
                    ad_group_fields = '*'
                    # # print('131232sql', sql)
                    sql = self.create_select_sql(db_name, 'adgroupTable', ad_group_fields, condition=condition)
                    print("FN:get_user_by_name getAdGroupById_sql:",sql)
                    ad_group_info = self.execute_fetch_one(conn, sql)
                    if ad_group_info:
                        ad_group_id_list.append(ad_group_info['ID'])
                for ad_group_id in ad_group_id_list:
                    print("FN:get_user_by_name update_user_to_adgroup")
                    fields = ('USER_ID', 'AD_GROUP_ID')
                    values = (user_id, ad_group_id)
                    user_to_adgroup_insert_sql = self.create_insert_sql(db_name, 'user_to_adgroupTable', '({})'.format(', '.join(fields)), values)
                    print('FN:get_user_by_name user_to_adgroup_insert_sql:', user_to_adgroup_insert_sql)
                    self.insert_exec(conn, user_to_adgroup_insert_sql, return_insert_id=True)
            data = response_code.SUCCESS
            data['data'] = user_info
            return data
        except Exception as e:
            lg.error(traceback.format_exc())
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
            # print('update_sql: ', sql)
            return_count = self.updete_exec(conn, sql)
            # print('return_count: ', return_count)
            data = response_code.SUCCESS
            data['data'] = {'count': return_count}
            return data
        except Exception as e:
            lg.error(e)
            return response_code.GET_DATA_FAIL
        finally:
            conn.close()

    def __get_util_permission(self, ad_group_id, table_name, table_id_field_name, db_name, conn):
        condition = 'AD_GROUP_ID="%s"' % ad_group_id
        utils_fields = '*'
        sql = self.create_select_sql(db_name, table_name, utils_fields, condition=condition)
        # print(table_name+' sql :', sql)
        utils_info = self.execute_fetch_one(conn, sql)
        if utils_info:
            utils_permissions = {}
            utils_id = str(utils_info[table_id_field_name])
            role_list = json.loads(utils_info['ROLE_LIST'])
            utils_permissions[utils_id] = {}
            for role_name in role_list:
                condition = 'NAME="%s"' % role_name
                role_fields = '*'
                sql = self.create_select_sql(db_name, 'roleTable', role_fields, condition=condition)
                print('FN:__get_util_permission roleTable_sql:', sql)
                role_info = self.execute_fetch_one(conn, sql)
                utils_permissions[utils_id][role_name] = json.loads(role_info['API_PERMISSION_LIST'])
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
            user_info = self.execute_fetch_one(conn, sql)
            user_info['permissions'] = {'usecase': {}, 'workspace': {}, 'org': {}}
            org_admin = False
            role_set = set()
            workspace_id_set = set()
            # # print('user_info', user_info)
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
                # # print('group_list:', group_list)
                # exit(0)
                for ad_group in ad_group_list:
                    condition = 'GROUP_MAIL="%s"' % ad_group
                    ad_group_fields = '*'
                    sql = self.create_select_sql(db_name, 'adgroupTable', ad_group_fields, condition=condition)
                    # # print('131232sql', sql)
                    ad_group_info = self.execute_fetch_one(conn, sql)
                    if not ad_group_info:
                        continue
                    # print('adgroup:', ad_group)
                    ad_group_id = ad_group_info['ID']

                    # get org permissions
                    utils_role_set, permissions = self.__get_util_permission(ad_group_id, 'org_to_adgroupTable', 'ORG_ID', db_name, conn)
                    # if 'admin' in utils_role_set:
                    #     role_set = set(['admin'])
                    # else:
                    role_set = utils_role_set | role_set
                    if 'admin' in role_set:
                        org_admin = True
                    # print('org_to_adgroupTable:', permissions)
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
                        # # print('2222', sql)
                        workspace_id_dict = self.execute_fetch_all(conn, sql)
                        # # print('1111111', workspace_id_dict)
                        workspace_id_set = workspace_id_set | set([item['WORKSPACE_ID'] for item in workspace_id_dict])

                        # workspace permissions up to all
                        # print('workspace_to_adgroupTable:', permissions)
                        for item_id in workspace_id_set:
                            item_id = str(item_id)
                            if item_id not in user_info['permissions']['workspace']:
                                user_info['permissions']['workspace'][item_id] = {'admin': ['*-*']}

                    else:
                        # get workspace id
                        condition = 'AD_GROUP_ID="%s"' % ad_group_id
                        workspace_id_field = 'WORKSPACE_ID'
                        sql = self.create_select_sql(db_name, 'workspace_to_adgroupTable', workspace_id_field, condition=condition)
                        print('2222', sql)
                        workspace_id_dict = self.execute_fetch_all(conn, sql)
                        print('1111111', workspace_id_dict)
                        workspace_id_set = workspace_id_set | set([item['WORKSPACE_ID'] for item in workspace_id_dict])

                        # get workspace permissions
                        print("fn:get_user_permissions id:{}, ad_group_id:{}".format(id,ad_group_id))
                        utils_role_set, permissions = self.__get_util_permission(ad_group_id, 'workspace_to_adgroupTable', 'WORKSPACE_ID', db_name, conn)
                        # role_set = utils_role_set | role_set
                        # print('workspace_to_adgroupTable:', permissions)
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
                    # print('usecase_to_adgroupTable:', permissions)
                    for item_id in permissions:
                        item_id = str(item_id)
                        if item_id in user_info['permissions']['usecase']:
                            for role_name in permissions[item_id]:
                                role_permissions = user_info['permissions']['usecase'][item_id].get(role_name, [])
                                role_permissions = list(set(role_permissions + permissions[item_id][role_name]))
                                user_info['permissions']['usecase'][item_id][role_name] = role_permissions
                        else:
                            user_info['permissions']['usecase'][item_id] = permissions[item_id]
                # print('workspace_id_set:', workspace_id_set)
                workspace_list = list(workspace_id_set)
                print('FN:get_user_permissions workspace_list:', workspace_list)
                if len(workspace_list) != 0:
                    user_info['workspace_list'] = []
                    user_info['workspace_id'] = str(workspace_list[0])
                    condition = 'ID in (%s)' % ','.join([str(w) for w in workspace_list])
                    workspace_info_field = 'ID,WORKSPACE_NAME'
                    sql = self.create_select_sql(db_name, 'workspaceTable', workspace_info_field, condition=condition)
                    # print('workspace sql: ', sql)
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
                    # print('workspace sql: 1111')
                    user_info['workspace_id'] = ''
                    user_info['workspace_list'] = []
                    user_info['role_list'] = []
                    user_info['user_role'] = ''

                # print('role_set:', role_set)
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

                print("FN:get_user_permissions user_info['workspace_list']: ",  user_info['workspace_list'])
                return user_info
            else:
                return {}
        except Exception as e:
            lg.error(traceback.format_exc())
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
                # print('create_get_relation_sql:', sql)
                ad_group_infos = self.execute_fetch_all(conn, sql)
                for ad_group in ad_group_infos:
                    ad_group_list.append(ad_group['GROUP_MAIL'])
            # print('ad_group_list:', ad_group_list)
            permissions = {'org': {}, 'usecase': {}, 'workspace': {}}
            # print('user_info', user_info)
            user_set = set()
            user_set.add(str(user_key))
            user_fields = 'ID'
            if user_info:
                for ad_group in ad_group_list:
                    condition = 'GROUP_MAIL="%s"' % ad_group
                    ad_group_fields = '*'
                    sql = self.create_select_sql(db_name, 'adgroupTable', ad_group_fields, condition=condition)
                    # # print('sql', sql)
                    ad_group_info = self.execute_fetch_one(conn, sql)
                    ad_group_id = ad_group_info['ID']
                    # get org permissions
                    utils_role_set, org_permissions = self.__get_util_permission(ad_group_id, 'org_to_adgroupTable', 'ORG_ID', db_name, conn)
                    # # print('org_permissions:', org_permissions)
                    permissions['org'] = org_permissions
                    for org_id in org_permissions:
                        for role in org_permissions[org_id]:
                            if role in self.manager_role:
                                sql = self.create_select_sql(db_name, 'userTable', user_fields)
                                # print('userTable:', sql)
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
                                # print('workspace account sql:', sql)
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
                # print('user_set: ', user_set)
                user_condiction = 'ID in(%s)' % ','.join(user_set)
                user_fields = '*'
                sql = self.create_select_sql(db_name, 'userTable', user_fields, user_condiction)
                # print('user info sql:', sql)
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
            lg.error(traceback.format_exc())
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
            ad_group_list = json.loads(user_info.get('GROUP_LIST', '[]'))
            ldap_username = user_info.get('ACCOUNT_NAME', None)
            user_mail = user_info.get('ACCOUNT_ID', None)

            return ad_group_list, (user_mail, ldap_username)
        except Exception as e:
            import traceback
            lg.error(traceback.format_exc())
            return None, (None, None)
        finally:
            conn.close()


user_mgr = DbUserMgr()
