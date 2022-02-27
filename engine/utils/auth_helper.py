#!/usr/bin/python
# -*- coding: UTF-8 -*
import json
import sys

import datetime
import jwt
import time
from flask import abort
from common.common_crypto import prpcrypt
from common.common_hash_key import secret_key
from utils.smtp_helper import Smtp
from utils.ldap_helper import Ldap
import api
from db.user.db_user_mgr import user_mgr
from utils.status_code import response_code
import traceback
import logging

logger = logging.getLogger("main.utils." + __name__)

class Auth(object):
    """
    Authorization and token support
    """
    # host = "23.101.10.96"
    # port = 636
    # ADMIN_DN = "admin@torro.ai"
    # ADMIN_PASSWORD = "LSr2go1gifBc5Nk6F+qM2A=="
    # ADMIN_PASSWORD = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJsZGFwX3B3ZCI6IjQ3NDU1RGdkZWVAIn0.Xg-iseNmc7efidKM-THSrxC34-GuNq-e2JBp4i3W8vI"
    # SEARCH_BASE = "ou=AADDC Users,dc=torro,dc=ai"

    @staticmethod
    def ldap_auth(username, password):

        return Ldap.ldap_auth(username, password)

    @staticmethod
    def service_account_login(account_dn, password, host, port, use_ssl=True):

        return Ldap.service_account_login(account_dn, password, host, port, use_ssl)

    @staticmethod
    def __encode_pwd(pwd):
        pwd = jwt.encode(
            pwd,
            api.Config.SECRET_KEY,
            algorithm='HS256'
        )
        return pwd

    @staticmethod
    def __decode_pwd(pwd):
        pwd = jwt.decode(pwd, api.Config.SECRET_KEY)
        return pwd

    def __encode_auth_token(self, user_key, account_id, permissions, role_list, role, workspace_list, workspace_id, login_time):
        """
        Token Generation
        :param USER_KEY: int
        :param login_time: int(timestamp)
        :return: string
        """
        try:
            ##exp: 过期时间
            ##nbf: 表示当前时间在nbf里的时间之前，则Token不被接受
            ##iss: token签发者
            ##aud: 接收者
            ##iat: 发行时间
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=60*60*1000),
                'iat': datetime.datetime.utcnow(),
                'iss': 'ken',
                'data': {
                    'user_key': user_key,
                    'account_id': account_id,
                    'permissions': permissions,
                    'role_list': role_list,
                    'user_role': role,
                    'workspace_list': workspace_list,
                    'workspace_id': workspace_id,
                    'login_time': login_time
                }
            }
            # print ('pyaload', payload)
            return jwt.encode(
                payload,
                api.Config.SECRET_KEY,
                algorithm='HS256'
            )
        except Exception as e:
            return e

    def __decode_auth_token(self, auth_token):
        """
        Verify Token
        :param auth_token:
        :return: integer|string
        """
        try:
            ###30分钟无访问token过期
            # payload = jwt.decode(auth_token, api.Config.SECRET_KEY, leeway=datetime.timedelta(seconds=60*60*1000))
            # # print("payload:", payload)
            # 取消过期时间验证
            payload = jwt.decode(auth_token, api.Config.SECRET_KEY, options={'verify_exp': False})
            if ('data' in payload and 'user_key' in payload['data'] and 'permissions' in payload['data']):
                return payload
            else:
                raise jwt.InvalidTokenError
        except jwt.ExpiredSignatureError:
            return 'Token Expired'
        except jwt.InvalidTokenError:
            return 'Invalid Token'
        except TypeError:
            return 'Token Error'
        except:
            logger.error(sys.exc_info()[1])

    @classmethod
    def get_offline_password(cls, username):
        try:
            user = user_mgr.get_user_by_name(username)
            user_base_data = user.get('data', None)
            mail_host = "smtp.gmail.com"  # Set Mail Server

            mail_user = "torroai@gmail.com"  # Set User Name
            mail_pass = ""  # Password
            sender = 'torroai@gmail.com' # Set Sender

            if user_base_data:
                new_password = secret_key(username, 32)
                data = user_mgr.update_user_password(username, new_password)
                return_count = data.get('data', {'count': 0})['count']
                if return_count > 0:
                    smtp_obj = Smtp(mail_host, mail_user, mail_pass, sender)
                    smtp_obj.send_email('TorroAi Login Info', 'Your offline password is: {}'.format(new_password),
                                        mail_user,  [username], 'TorroAi')
                return True
            else:
                return False
        except:
            # print(traceback.format_exc())
            return False
    @classmethod
    def authenticate(cls, username, password, offline_flag):
        """
        When user login, successful login will return the token, and the login time will be inserted into DB.
        If login failed, return the login failure reason.
        :param password:
        :return: json
        """
        
        password = prpcrypt.decrypt(password)
        # ldap:
        if username == 'TorroAdmin':
            user = user_mgr.get_user_by_name(username)
            user_base_data = user.get('data')
            if user_base_data and password == user_base_data['PASS_WORD']:
                logger.info('FN:AnthN login_user:torro_admin')
                data = response_code.SUCCESS
                data['msg'] = '[ORG_SETTING]'
                data['token'] = prpcrypt.encrypt('[SETTING]')
                return data
            else:
                return response_code.LOGIN_FAIL
        if offline_flag == 1:
            ad_group_list, ldap_usernames = user_mgr.offline_login(username, password)
            logger.info("FN:AnthN login_mode:offline user:{}".format(ldap_usernames))
        else:
            ad_group_list, ldap_usernames = Auth.ldap_auth(username, password)
            logger.info("FN:AnthN login_mode:ldap  user:{}".format(ldap_usernames))
            
        if ldap_usernames[0] is not None:
            user = user_mgr.get_user_by_name(username, ldap_usernames, ad_group_list)
        else:
            user = user_mgr.get_user_by_name(username)
        user_base_data = user.get('data')
        logger.debug('FN:authenticate user_base_data:{}{}'.format(user_base_data, user))
        
        # Check if this user exists
        if (user_base_data is None):
            return response_code.LOGIN_FAIL
        if user_base_data:
            # print('ad_group_list', ad_group_list)
            if not ad_group_list:
                return response_code.LOGIN_IS_FAIL
            user_data = user_mgr.get_user_permissions(user_base_data['ID'], ad_group_list)
            # # print('user_data', user_data)
            # # print('role_list', user_data['role_list'])
            # 登录时间
            login_time = int(time.time())
            # # print('user_data', user_data)
            # 生成token
            token = cls.__encode_auth_token(cls, user_data.get('ID'), user_data.get('ACCOUNT_ID'), user_data.get('permissions'),
                                            user_data['role_list'], user_data['user_role'],
                                            user_data['workspace_list'], str(user_data['workspace_id']),
                                            login_time)
            # print('token', token)
            user_data['ad_group_list'] = user_data['GROUP_LIST']
            user_data.pop('GROUP_LIST')
            user_data.pop('PASS_WORD')
            user_data.pop('permissions')
            dict_user = user_data
            dict_user['token'] = token.decode()
            return dict_user
        else:
            return response_code.LOGIN_IS_FAIL

    @staticmethod
    def __check_permission(user_role, permissions, request_id, api_endpoint, method):
        # print('permissions:', permissions)
        api_permission = '{}-{}'.format(api_endpoint, method)
        all_method_permission = '*-{}'.format(method)
        all_endpoint_permission = '{}-*'.format(api_endpoint)
        all_permission = '*-*'
        permission_allow = 0
        # logger.info('FN:_check_permissions user_role:{}'.format(user_role))
        if user_role == '':
            user_role = 'viewer'
        # logger.debug('FN:_check_permissions default user_role:{}'.format(user_role))
        # logger.debug('FN:_check_permissions permissions:{}'.format(permissions))
        # logger.info('FN:_check_permissions api_endpoint:{}{}{}'.format(request_id, api_endpoint, method))
        for id in permissions:
            if (request_id is None or id == request_id) and user_role in permissions[id]:
                if all_permission in permissions[id][user_role] or api_permission in \
                        permissions[id][user_role] or all_method_permission in \
                        permissions[id][user_role] or all_endpoint_permission in \
                        permissions[id][user_role]:
                    permission_allow = 1
                    break
        return permission_allow
    @classmethod
    def refresh_token(cls, request, role_name, workspace_id, new_workspace_id_dict=None, remove_workspace_id_dict=None):
        # workspace_item_list: all the worksapce
        # role list: all the role list
        # role_name: chosen role
        # workspace_id: chosen workspace id
        # workspace_list: the workspace list under chosen role
        login_time = int(time.time())
        auth_token = request.cookies.get('token')
        # # print('auth_token', auth_token)
        payload = cls.__decode_auth_token(cls, auth_token)
        logger.debug('FN:refresh_token payload:{}'.format(payload))
        # role_list = payload['data']['role_list']
        old_role = payload['data']['user_role']
        old_workspace_id = payload['data']['workspace_id']
        workspace_item_list = payload['data']['workspace_list']
        workspace_permissions = payload['data']['permissions']['workspace']

        # update workspace when add/delete workspace
        # add workspace
        if new_workspace_id_dict and 'value' in new_workspace_id_dict:
            workspace_item_list.append(new_workspace_id_dict)
            # change new workspace
            workspace_id = new_workspace_id_dict['value']
            # create workspace and get the admin role
            payload['data']['permissions']['workspace'][str(workspace_id)] = {'admin': ['*-*']}
        # delete workspace
        remove_workspace_index_list = []
        remove_workspace_list = []
        if remove_workspace_id_dict:
            # set role and workspace to None
            old_workspace_id = None
            old_role = None
            remove_workspace_list.append(remove_workspace_id_dict['value'])
            logger.debug('FN:refresh_token workspace_item_list:{}'.format(workspace_item_list))
            for index, workspace in enumerate(workspace_item_list):
                if workspace['value'] in remove_workspace_list:
                    remove_workspace_index_list.append(index)
            for i in range(len(remove_workspace_index_list) - 1, -1, -1):
                workspace_item_list.pop(remove_workspace_index_list[i])
            role_name_list = []
            if len(workspace_item_list) > 0:
                workspace_id = str(workspace_item_list[0]['value'])
                for wp_role_name in workspace_permissions[workspace_id]:
                    role_name_list.append(wp_role_name)

            else:
                workspace_id = None
            if len(role_name_list)> 0:
                role_name = role_name_list[0]
            else:
                role_name = None

        logger.debug('FN:refresh_token workspace_id:{}'.format(workspace_id))
        # get default role&workspace
        if workspace_id is None and role_name is None:
            role_name = old_role
            workspace_id = old_workspace_id
        if workspace_id is not None:
            workspace_id = str(workspace_id)
        # choose workspace id

        # workspace_name_list = []
        # print('-1workspace_item_list:', workspace_item_list)
        # get all workspace id
        # for item_id in workspace_permissions:
        #     workspace_name_list.append(str(item_id))
        # get workspace id
        if workspace_id is None or workspace_id not in workspace_permissions:
            if old_workspace_id:
                workspace_id = old_workspace_id
            else:
                workspace_id = ''

        logger.debug('FN:refresh_token workspace id:{}{}'.format(workspace_id, workspace_permissions))
        # # choose role
        role_name_list = []
        if workspace_id is not None and workspace_id in workspace_permissions:
            logger.info('FN:refresh_token '.format())
            for wp_role_name in workspace_permissions[workspace_id]:
                logger.debug('FN:refresh_tolen wp_role_name:'.format(wp_role_name))

                role_name_list.append(wp_role_name)
        logger.debug('FN:refresh_token role_name_list:{} role_name:{}'.format(role_name_list, role_name))

        # print('2workspace_item_list:', workspace_item_list)
        # workspace_name_list = list(set(workspace_name_list))
        # print(role_name, role_list)
        # print(workspace_id, workspace_name_list)
        # fix error role&workspace selection
        if role_name is None or role_name not in role_name_list:
            if len(role_name_list) == 1:
                role_name = role_name_list[0]
            else:
                role_name = ''


        # print(role_name, role_list)
        # print(workspace_id, workspace_name_list)
        token = cls.__encode_auth_token(cls, payload['data']['user_key'], payload['data']['account_id'], payload['data']['permissions'],
                                        role_name_list, role_name,
                                        workspace_item_list, workspace_id, login_time)
        logger.debug('FN:refresh_token token:{}'.format(token))

        return token.decode(), role_name, role_name_list, workspace_id, workspace_item_list


    @classmethod
    def identify(cls, request):
        """
        Identify User
        :return: list
        """
        auth_token = request.cookies.get('token')
        # logger.debug('FN:identify auth_token:{}'.format(auth_token))
        if (auth_token):
            # Bearer cjidsfjsfi
            # workspace_id = request.cookies.get('workspace_id', '1')
            # usecase_id = request.cookies.get('usecase_id', '1')
            # team_id = request.cookies.get('team_id', '1')
            if not auth_token:
                data = response_code.TOKEN_ERROR
                data['msg'] = 'Your login status has expired. Please login again'
                return data, None, None
            else:
                payload = cls.__decode_auth_token(cls, auth_token)
                # logger.debug('FN:identify payload:{}'.format(payload))
                if not isinstance(payload, str):
                    user_id = payload['data']['user_key']
                    account_id = payload['data']['account_id']
                    workspace_id = payload['data']['workspace_id']
                    user_role = payload['data']['user_role']
                    # team_permissions = payload['data']['permissions']['team']
                    usecase_permissions = payload['data']['permissions']['usecase']
                    workspace_permissions = payload['data']['permissions']['workspace']
                    org_permissions = payload['data']['permissions']['org']
                    # check if user exist
                    userInfo = user_mgr.get_user_by_id(user_id)

                    api_endpoint = request.endpoint
                    method = request.method
                    logger.debug('FN:identify payload:{}{}'.format( payload, api_endpoint))
                    
                    if (userInfo is None):
                        abort(401, 'user not found')
                    else:
                        # print('org permission:')
                        permission_allow = Auth.__check_permission(user_role, org_permissions, None, api_endpoint, method)
                        # logger.debug('FN:identify org permission_allow:{}'.format(permission_allow))
                        if permission_allow == 0:
                            # print('workspace permission:')
                            permission_allow = Auth.__check_permission(user_role, workspace_permissions, workspace_id, api_endpoint, method)
                        # if permission_allow == 0:
                        #     # print('usecase permission:')
                        #     permission_allow = Auth.__check_permission(user_role, usecase_permissions, usecase_id, api_endpoint, method)
                        # if permission_allow == 0:
                        #     # print('team permission:')
                        #     permission_allow = Auth.__check_permission(user_role, team_permissions, team_id, api_endpoint, method)
                            # logger.debug('FN:identify wp permission_allow:{}'.format(permission_allow))
                        if permission_allow == 1:
                            return user_id, account_id, workspace_id
                        else:
                            data = response_code.TOKEN_ERROR
                            data['msg'] = 'Permission denied.'
                            return data, None, None
                else:
                    data = response_code.TOKEN_ERROR
                    data['msg'] = 'Payload error'
                    return data, None, None
        else:
            data = response_code.TOKEN_ERROR
            data['msg'] = 'Your login status has expired. Please login again'
            return data, None, None
