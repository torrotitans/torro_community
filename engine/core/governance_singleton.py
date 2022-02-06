#!/usr/bin/python
# -*- coding: UTF-8 -*


from db.governance.db_governance_mgr import governance_mgr

__all__ = {"governanceSingleton"}


class governanceSingleton():

    def change_status(self, user_key, account_id, inputData):

        return governance_mgr.change_status(user_key, account_id, inputData)

    def updateTask(self, user_key, account_id, input_form_id, tasks, return_msg_list):

        return governance_mgr.updateTask(user_key, account_id, input_form_id, tasks, return_msg_list)

    def add_new_usecase(self, input_form_id, form_id, user_id, workspace_id):

        return governance_mgr.add_new_usecase_setting(input_form_id, form_id, user_id, workspace_id)

    # def add_new_policy_tags(self, input_form_id, form_id, user_id, workspace_id):
    #
    #
    #     return governance_mgr.add_new_policy_tags(input_form_id, form_id, user_id, workspace_id)
governance_singleton = governanceSingleton()
