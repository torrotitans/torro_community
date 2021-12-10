#!/usr/bin/python
# -*- coding: UTF-8 -*

from db.org.db_org_mgr import org_mgr
from db.comment.db_comment_mgr import comment_mgr
from utils.smtp_helper import Smtp
__all__ = {"commentSingleton"}


class commentSingleton():

    def add_new_comment(self, user_id, account_id, request):

        return comment_mgr.add_new_comment(user_id, account_id, request)


    def delete_comment(self, user_id, request):

        return comment_mgr.delete_comment(user_id, request)

    def update_comment(self):
        pass

comment_singleton = commentSingleton()
