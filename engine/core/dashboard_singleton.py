#!/usr/bin/python
# -*- coding: UTF-8 -*


from db.dashboard.db_dashboard_mgr import dashboard_mgr

__all__ = {"dashboardSingleton"}


class dashboardSingleton():

    def get_data(self, user_id, condiction_dict, workspace_id):

        return dashboard_mgr.get_data(user_id, condiction_dict, workspace_id)

    def get_options(self, user_id, workspace_id):

        return dashboard_mgr.get_options(user_id, workspace_id)

    def get_notify(self, account_id, is_read=None):

        return dashboard_mgr.get_notify(account_id, is_read)

    def read_notify(self, account_id, notify_id, is_read=None):
        return dashboard_mgr.read_notify(account_id, notify_id, is_read)

dashboard_singleton = dashboardSingleton()
