from ldap3 import Server, Connection, ALL, SUBTREE, Tls
from common.common_crypto import prpcrypt
import traceback
from db.org.db_org_mgr import org_mgr

class Ldap():

    ldap_info = org_mgr.get_ldap_info()
    # # print('ldap_info', ldap_info)
    if ldap_info['code'] == 200:
        ldap_info = ldap_info['data']
        host = ldap_info['HOST']
        port = ldap_info['PORT']
        if int(ldap_info['USE_SSL']) == 1:
            use_ssl = True
        else:
            use_ssl = False
        ADMIN_DN = ldap_info['ADMIN_DN']
        ADMIN_PASSWORD = ldap_info['ADMIN_PWD']

        USER_SEARCH_BASE = ldap_info['USER_SEARCH_BASE']
        USER_SERACH_FILTER = ldap_info['USER_SERACH_FILTER']

        DISPLAY_NAME_LDAP_ATTRIBUTE = ldap_info['DISPLAY_NAME_LDAP_ATTRIBUTE']
        EMAIL_ADDRESS_LDAP_ATTRIBUTE = ldap_info['EMAIL_ADDRESS_LDAP_ATTRIBUTE']
        USER_ADGROUP_ATTRIBUTE = ldap_info['USER_ADGROUP_ATTRIBUTE']

        GROUP_SEARCH_BASE = ldap_info['GROUP_SEARCH_BASE']
        GROUP_SERACH_FILTER = ldap_info['GROUP_SERACH_FILTER']
        GROUP_MEMBER_ATTRIBUTE = ldap_info['GROUP_MEMBER_ATTRIBUTE']
        GROUP_EMAIL_SUFFIX = ldap_info['GROUP_EMAIL_SUFFIX']
        # GROUP_MEMBERSHIP = ldap_info['GROUP_MEMBERSHIP'] # 0 is user has memeberof attribute, 1 is user does not have.
    else:
        host = ''
        port = ''
        use_ssl = True
        ADMIN_DN = ''
        ADMIN_PASSWORD = ''

        USER_SEARCH_BASE = ''
        USER_SERACH_FILTER = ''
        USER_ADGROUP_ATTRIBUTE = ''

        GROUP_SEARCH_BASE = ''
        GROUP_SERACH_FILTER = ''
        GROUP_MEMBER_ATTRIBUTE = ''

    @staticmethod
    def __get_user(account_cn, conn):
        res = conn.search(
            search_base=Ldap.USER_SEARCH_BASE,
            search_filter='({})'.format(Ldap.USER_SERACH_FILTER.format(account_cn)),
            search_scope=SUBTREE,
            attributes=['*'],
            paged_size=5
        )
        # if not res:
        #     res = conn.search(
        #     search_base = Ldap.SEARCH_BASE,
        #     search_filter = '(userPrincipalName={username})'.format(username=username),
        #     search_scope = SUBTREE,
        #     attributes = ['cn', 'givenName', 'sAMAccountName', 'memberOf', 'name'],
        #     paged_size = 5
        #     )
        return res

    @staticmethod
    def __get_ad_group(ad_group, conn):
        res = conn.search(
            search_base=Ldap.GROUP_SEARCH_BASE,
            search_filter='({})'.format(Ldap.GROUP_SERACH_FILTER.format(ad_group)),
            search_scope=SUBTREE,
            attributes=['*'],
            paged_size=5
        )
        # if not res:
        #     res = conn.search(
        #     search_base = Ldap.SEARCH_BASE,
        #     search_filter = '(userPrincipalName={username})'.format(username=username),
        #     search_scope = SUBTREE,
        #     attributes = ['cn', 'givenName', 'sAMAccountName', 'memberOf', 'name'],
        #     paged_size = 5
        #     )
        return res

    @staticmethod
    def __get_member_ad_group(entry, conn):
        ad_groups_mails = []
        # res = Ldap.__get_user(member, conn)
        # if res:
        # entry = conn.response[0]
        # dn = entry['dn']
        attr_dict = entry['attributes']
        for ad_group_util in attr_dict[Ldap.USER_ADGROUP_ATTRIBUTE]:
            adgroup_attribute = Ldap.GROUP_SERACH_FILTER.split('=')[0]
            ad_group_name = ad_group_util.split(',')[0].replace(adgroup_attribute+'=', '')
            ad_group_name = ad_group_name.replace(adgroup_attribute.upper()+'=', '')
            # adgrou_cn = ad_group_util.split(',')[0]
            # search_base = ad_group_util.replace(adgrou_cn+',', '')
            res = conn.search(
                search_base=Ldap.GROUP_SEARCH_BASE,
                search_filter='({})'.format(Ldap.GROUP_SERACH_FILTER.format(ad_group_name)),
                search_scope=SUBTREE,
                attributes=['*']
            )
            if res:
                entry = conn.response[0]
                # adgroup_attribute = Ldap.GROUP_SERACH_FILTER.split('=')[0]
                # adgroup_name = attr_dict[adgroup_attribute][0]
                ad_group_mail = entry['attributes'][adgroup_attribute][0] + Ldap.GROUP_EMAIL_SUFFIX
                if ad_group_mail:
                    ad_groups_mails.append(ad_group_mail)

        return ad_groups_mails

    @staticmethod
    def __get_ad_group_member(entry, conn):
        member_mails = []
        # res = Ldap.__get_user(member, conn)
        # if res:
        # entry = conn.response[0]
        # dn = entry['dn']
        attr_dict = entry['attributes']
        for user_util in attr_dict[Ldap.GROUP_MEMBER_ATTRIBUTE]:
            user_attribute = Ldap.USER_SERACH_FILTER.split('=')[0]
            user_name = user_util.split(',')[0].replace(user_attribute+'=', '')
            user_name = user_name.replace(user_attribute.upper()+'=', '')

            # user_search_name = user_util
            res = conn.search(
                search_base=Ldap.USER_SEARCH_BASE,
                search_filter='({})'.format(Ldap.USER_SERACH_FILTER.format(user_name)),
                search_scope=SUBTREE,
                attributes=['*']
            )
            if res:
                entry = conn.response[0]
                # login_attribute = Ldap.USER_SERACH_FILTER.split('=')[0]
                member_mail = entry['attributes'][Ldap.EMAIL_ADDRESS_LDAP_ATTRIBUTE][0]
                # print('member_mail:', member_mail)
                if member_mail:
                    member_mails.append(member_mail)
        # # print('member_mails:', member_mails)
        return member_mails
    @staticmethod
    def __login_with_user_pwd(account_cn, password, servers):
        # return True
        # print(username, password)
        print('user cn:', '{},{}'.format(Ldap.USER_SERACH_FILTER.format(account_cn), Ldap.USER_SEARCH_BASE))
        conn = Connection(servers, '{},{}'.format(Ldap.USER_SERACH_FILTER.format(account_cn), Ldap.USER_SEARCH_BASE),
                          password, check_names=True, lazy=False, raise_exceptions=True)
        conn.open()
        conn.bind()
        if conn.result["description"] == "success":
            # print("auth success:", conn.result)
            return True
        else:
            # print("auth fail:", conn.result)
            return False

    @staticmethod
    def service_account_login(account_dn, password, host, port, use_ssl=False):
        pwd = prpcrypt.decrypt(password)
        # print('ldap info:', Ldap.host, Ldap.use_ssl, Ldap.port)
        # pwd = Ldap.__decode_pwd(Ldap.ADMIN_PASSWORD)['ldap_pwd']
        try:
            print("FN:svc_acc_login:acc{}, pw{}, host{}, port{}, use_ssl{}".format(account_dn, password, host, port, use_ssl))
            print("Check use_ssl{}".format(use_ssl==True))
            servers = Server(host, use_ssl=use_ssl, get_info=ALL, port=port)
            conn = Connection(servers, account_dn, pwd, check_names=True, lazy=False, raise_exceptions=True)
            conn.open()
            conn.bind()
            if conn.result["description"] == "success":
                # print("auth success:", conn.result)
                return True
            else:
                # print("auth fail:", conn.result)
                return False

        except:
            print(traceback.format_exc())
            return False

    @staticmethod
    def ldap_auth(account_cn, password):
        pwd = prpcrypt.decrypt(Ldap.ADMIN_PASSWORD)
        # print('ldap info:', Ldap.host, Ldap.use_ssl, Ldap.port)
        # pwd = Ldap.__decode_pwd(Ldap.ADMIN_PASSWORD)['ldap_pwd']
        try:

            servers = Server(Ldap.host, use_ssl=Ldap.use_ssl, get_info=ALL, port=Ldap.port)
            conn = Connection(servers, Ldap.ADMIN_DN, pwd, check_names=True, lazy=False, raise_exceptions=True)
            conn.open()
            conn.bind()
            # username is cn name.
            res = Ldap.__get_user(account_cn, conn)
            # ldap_server_pool = ServerPool(LDAP_SERVER_POOL)
            # conn = Connection(ldap_server_pool, user=ADMIN_DN, password=ADMIN_PASSWORD, check_names=True, lazy=False, raise_exceptions=False)
            # conn.open()
            # conn.bind()
            # exit(0)
            print('res ', account_cn, res)
            if res:
                entry = conn.response[0]
                print('entry:', entry)
                attr_dict = entry['attributes']
                # login_attribute = Ldap.USER_SERACH_FILTER.split('=')[0]
                # user_name = attr_dict[login_attribute][0]
                user_mail = attr_dict[Ldap.EMAIL_ADDRESS_LDAP_ATTRIBUTE][0]
                user_dispaly_name = attr_dict[Ldap.DISPLAY_NAME_LDAP_ATTRIBUTE][0]
                # check password by dn, get displayname and email
                login_flag = Ldap.__login_with_user_pwd(account_cn, password, servers)
                print('login_flag:', login_flag)
                if login_flag:
                    ad_group_list = Ldap.__get_member_ad_group(entry, conn)
                    return ad_group_list, (user_mail, user_dispaly_name)
                else:
                    return None, (None, None)
            else:
                return None, (None, None)
        except:
            print(traceback.format_exc())
            return None, (None, None)
    @staticmethod
    def get_member_ad_group(account_id, offline_flag=0):
        account_cn = org_mgr.get_user_cn(account_id)
        pwd = prpcrypt.decrypt(Ldap.ADMIN_PASSWORD)
        # pwd = Ldap.__decode_pwd(Ldap.ADMIN_PASSWORD)['ldap_pwd']
        try:
            if offline_flag == 0:
                servers = Server(Ldap.host, use_ssl=Ldap.use_ssl, get_info=ALL, port=Ldap.port)
                conn = Connection(servers, Ldap.ADMIN_DN, pwd, check_names=True, lazy=False, raise_exceptions=True)
                conn.open()
                conn.bind()
                res = Ldap.__get_user(account_cn, conn)
                # print('conn.result:', conn.result)
                # print('res ', res)
                if res:
                    entry = conn.response[0]
                    # print('entry:', entry)
                    # attr_dict = entry['attributes']
                    ad_group_list = Ldap.__get_member_ad_group(entry, conn)
                    return ad_group_list
                else:
                    return []
            else:
                ad_group_list = org_mgr.offline_ad_group(account_id)
                return  ad_group_list
        except:
            # print(traceback.format_exc())
            return []

    @staticmethod
    def get_ad_group_member(ad_group_mail):
        ad_group_name = ad_group_mail.replace(Ldap.GROUP_EMAIL_SUFFIX, '')
        pwd = prpcrypt.decrypt(Ldap.ADMIN_PASSWORD)
        # pwd = Ldap.__decode_pwd(Ldap.ADMIN_PASSWORD)['ldap_pwd']
        try:
            servers = Server(Ldap.host, use_ssl=Ldap.use_ssl, get_info=ALL, port=Ldap.port)
            conn = Connection(servers, Ldap.ADMIN_DN, pwd, check_names=True, lazy=False, raise_exceptions=True)
            conn.open()
            conn.bind()
            res = Ldap.__get_ad_group(ad_group_name, conn)

            # print('res ', res)
            if res:
                entry = conn.response[0]
                # print('entry:', entry)
                # attr_dict = entry['attributes']
                member_list = Ldap.__get_ad_group_member(entry, conn)
                # # print(member_list)
                return member_list, ad_group_mail
            else:
                return None, None
        except:
            # print(traceback.format_exc())
            return None, None
