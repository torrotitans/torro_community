#!/usr/bin/python
# -*- coding: UTF-8 -*


from db.it.db_it_mgr import it_mgr

__all__ = {"itSingleton"}


class itSingleton():

    def sql_execute(self, text):

        return it_mgr.sql_execute(text)

it_singleton = itSingleton()
