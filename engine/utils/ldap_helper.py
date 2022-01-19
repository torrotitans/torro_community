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
        if int(ldap_info['USE_SLL']) == 1:
            use_sll = True
        else:
            use_sll = False
        ADMIN_DN = ldap_info['ADMIN']
        ADMIN_PASSWORD = ldap_info['ADMIN_PWD']
        SEARCH_BASE = ldap_info['SEARCH_BASE']
    else:
        host = ''
        port = ''
        use_sll = True
        ADMIN_DN = ''
        ADMIN_PASSWORD = ''
        SEARCH_BASE = ''

    @staticmethod
    def __get_user(username, conn):
        res = conn.search(
            search_base=Ldap.SEARCH_BASE,
            search_filter='(uid={username})'.format(username=username),
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
            search_base="ou=Group,dc=torro,dc=ai",
            search_filter='(cn={ad_group})'.format(ad_group=ad_group),
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
        for ad_group in attr_dict['sn']:
            name = ad_group.split(',')[0].replace('cn=', '')
            name = name.replace('CN=', '')
            res = conn.search(
                search_base="ou=Group,dc=torro,dc=ai",
                search_filter='(cn={})'.format(name),
                search_scope=SUBTREE,
                attributes=['*']
            )
            if res:
                entry = conn.response[0]
                ad_groups_mail = entry['attributes']['cn'][0]
                if ad_groups_mail:
                    ad_groups_mails.append(ad_groups_mail)

        return ad_groups_mails

    @staticmethod
    def __get_ad_group_member(entry, conn):
        member_mails = []
        # res = Ldap.__get_user(member, conn)
        # if res:
        # entry = conn.response[0]
        # dn = entry['dn']
        attr_dict = entry['attributes']
        for ad_group in attr_dict['member']:
            name = ad_group.split(',')[0].replace('cn=', '')
            name = name.replace('CN=', '')
            res = conn.search(
                search_base=Ldap.SEARCH_BASE,
                search_filter='(cn={})'.format(name),
                search_scope=SUBTREE,
                attributes=['*']
            )
            if res:
                entry = conn.response[0]
                member_mail = entry['attributes']['uid'][0]
                # print('member_mail:', member_mail)
                if member_mail:
                    member_mails.append(member_mail)
        # # print('member_mails:', member_mails)
        return member_mails
    @staticmethod
    def __login_with_user_pwd(username, password, servers):
        # return True
        # print(username, password)
        conn = Connection(servers, username, password, check_names=True, lazy=False, raise_exceptions=True)
        conn.open()
        conn.bind()
        if conn.result["description"] == "success":
            # print("auth success:", conn.result)
            return True
        else:
            # print("auth fail:", conn.result)
            return False

    @staticmethod
    def ldap_auth(username, password):
        pwd = prpcrypt.decrypt(Ldap.ADMIN_PASSWORD)
        # print('ldap info:', Ldap.host, Ldap.use_sll, Ldap.port)
        # pwd = Ldap.__decode_pwd(Ldap.ADMIN_PASSWORD)['ldap_pwd']
        try:

            servers = Server(Ldap.host, use_ssl=Ldap.use_sll, get_info=ALL, port=Ldap.port)
            conn = Connection(servers, 'uid={},ou=system'.format(Ldap.ADMIN_DN), pwd, check_names=True, lazy=False, raise_exceptions=True)
            conn.open()
            conn.bind()
            res = Ldap.__get_user(username, conn)
            # ldap_server_pool = ServerPool(LDAP_SERVER_POOL)
            # conn = Connection(ldap_server_pool, user=ADMIN_DN, password=ADMIN_PASSWORD, check_names=True, lazy=False, raise_exceptions=False)
            # conn.open()
            # conn.bind()
            # exit(0)
            # print('res ', res)
            if res:
                entry = conn.response[0]
                # print('entry:', entry)
                attr_dict = entry['attributes']
                user_name = attr_dict['cn'][0]
                # check password by dn
                login_flag = Ldap.__login_with_user_pwd(entry['dn'], password, servers)
                if login_flag:
                    ad_group_list = Ldap.__get_member_ad_group(entry, conn)
                    return ad_group_list, user_name
                else:
                    return None, None
            else:
                return None, None
        except:
            # print(traceback.format_exc())
            return None, None
    @staticmethod
    def get_member_ad_group(username, offline_flag=0):
        pwd = prpcrypt.decrypt(Ldap.ADMIN_PASSWORD)
        # pwd = Ldap.__decode_pwd(Ldap.ADMIN_PASSWORD)['ldap_pwd']
        try:
            if offline_flag == 0:
                servers = Server(Ldap.host, use_ssl=Ldap.use_sll, get_info=ALL, port=Ldap.port)
                conn = Connection(servers, 'uid={},ou=system'.format(Ldap.ADMIN_DN), pwd, check_names=True, lazy=False, raise_exceptions=True)
                conn.open()
                conn.bind()
                res = Ldap.__get_user(username, conn)
                # print('conn.result:', conn.result)
                # print('res ', res)
                if res:
                    entry = conn.response[0]
                    # print('entry:', entry)
                    attr_dict = entry['attributes']
                    ad_group_list = Ldap.__get_member_ad_group(entry, conn)
                    return ad_group_list
                else:
                    return []
            else:
                ad_group_list = org_mgr.offline_ad_group(username)
                return  ad_group_list
        except:
            # print(traceback.format_exc())
            return []

    @staticmethod
    def get_ad_group_member(ad_group):
        pwd = prpcrypt.decrypt(Ldap.ADMIN_PASSWORD)
        # pwd = Ldap.__decode_pwd(Ldap.ADMIN_PASSWORD)['ldap_pwd']
        try:
            servers = Server(Ldap.host, use_ssl=Ldap.use_sll, get_info=ALL, port=Ldap.port)
            conn = Connection(servers, 'uid={},ou=system'.format(Ldap.ADMIN_DN), pwd, check_names=True, lazy=False, raise_exceptions=True)
            conn.open()
            conn.bind()
            res = Ldap.__get_ad_group(ad_group, conn)

            # print('res ', res)
            if res:
                entry = conn.response[0]
                # print('entry:', entry)
                # attr_dict = entry['attributes']
                member_list = Ldap.__get_ad_group_member(entry, conn)
                # # print(member_list)
                return member_list, ad_group
            else:
                return None, None
        except:
            # print(traceback.format_exc())
            return None, None