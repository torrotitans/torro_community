#!/usr/bin/python
# -*- coding: UTF-8 -*


from db.org.db_org_mgr import org_mgr

__all__ = {"orgSingleton"}


class orgSingleton():

    def add_new_org_setting(self, org):
        """

        :return:
        """
        return org_mgr.add_new_org_setting(org)

    def get_org_info(self):
        return org_mgr.get_org_info()

    def update_org(self, org):
        return org_mgr.update_org_info(org)

    def get_roles_info(self):
        return org_mgr.get_roles_info()
orgSingleton_singleton = orgSingleton()


