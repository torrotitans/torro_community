#!/usr/bin/python
# -*- coding: UTF-8 -*


from db.workspace.db_workspace_mgr import workspace_mgr

__all__ = {"workspaceSingleton"}


class workspaceSingleton():

    def add_new_workspace_setting(self, workspace):
        """

        :return:
        """
        return workspace_mgr.add_new_workspace_setting(workspace)

    def get_workspace_info_by_ad_group(self, account_id):
        return workspace_mgr.get_workspace_info_by_ad_group(account_id)
    def get_workspace_details_info_by_id(self, id):
        return workspace_mgr.get_workspace_details_info_by_id(id)

    def update_workspace(self, workspace):
        return workspace_mgr.update_workspace_info(workspace)
    def delete_workspace(self, workspace):
        return workspace_mgr.delete_workspace_info(workspace)

    def get_policy_tags_info(self, workspace_id):
        return workspace_mgr.get_policy_tags_info(workspace_id)

    def get_tag_template_info(self, workspace_id):
        return workspace_mgr.get_tag_template_info(workspace_id)

workspace_singleton = workspaceSingleton()


