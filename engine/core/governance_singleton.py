#!/usr/bin/python
# -*- coding: UTF-8 -*


from db.governance.db_governance_mgr import governance_mgr

__all__ = {"governanceSingleton"}


class governanceSingleton():

    def change_status(self, user_key, account_id, workspace_id, inputData, system_approval_flag=False, no_approval=False):

        return governance_mgr.change_status(user_key, account_id, workspace_id, inputData, system_approval_flag, no_approval)

    def system_approval_trigger(self, user_key, account_id,  inputData):

        return governance_mgr.system_approval_trigger(user_key, account_id, inputData)

    def updateTask(self, user_key, account_id, input_form_id, workspace_id, tasks, return_msg_list):

        return governance_mgr.updateTask(user_key, account_id, input_form_id, workspace_id, tasks, return_msg_list)

    # def add_new_usecase(self, input_form_id, form_id, user_id, workspace_id):

    #     return governance_mgr.add_new_usecase_setting(input_form_id, form_id, user_id, workspace_id)

    def get_admin_user_info(self):

        return governance_mgr.get_admin_user_info()
    # def add_new_policy_tags(self, input_form_id, form_id, user_id, workspace_id):
    #
    #
    #     return governance_mgr.add_new_policy_tags(input_form_id, form_id, user_id, workspace_id)
governance_singleton = governanceSingleton()
