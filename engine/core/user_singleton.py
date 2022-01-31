#!/usr/bin/python
# -*- coding: UTF-8 -*


from db.user.db_user_mgr import user_mgr

__all__ = {"userSingleton"}


class userSingleton():


    def get_all_base_user(self, form_id):
        return user_mgr.get_all_base_user_by_form_id(form_id)

    def get_details_user(self, user_id):
        return user_mgr.get_detail_user_by_user_id(user_id)

    def get_all_stages(self):

        return user_mgr.get_all_stages()

    def delete_user(self, user):

        return user_mgr.delete_user(user)

    def add_new_user(self, user):

        return user_mgr.add_new_user(user)

    def update_user(self, user):

        return user_mgr.update_user(user)

    # def get_stages_by_(self, value):
    #     """
    #     获取所有的fields信息
    #     :return:
    #     """
    #     return user_mgr.get_stages_with_condition(value)
    
    def fetch_user_info(self, user_key, wp_id=0):

        return user_mgr.fetch_user_info(user_key, wp_id)
    
userSingleton_singleton = userSingleton()


