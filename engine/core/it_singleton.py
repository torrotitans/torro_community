#!/usr/bin/python
# -*- coding: UTF-8 -*


from db.it.db_it_mgr import it_mgr

__all__ = {"itSingleton"}


class itSingleton():

    def get_cmd_sql(self, sql):

        return it_mgr.get_cmd_sql(sql)

it_singleton = itSingleton()
