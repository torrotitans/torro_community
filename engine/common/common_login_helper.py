#!/usr/bin/python
# -*- coding: UTF-8 -*

from functools import wraps
from os import abort
from flask import request, g
from utils.auth_helper import Auth
import logging

logger = logging.getLogger("main.common." + __name__)

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user_key, account_id, workspace_id = Auth.identify(request)
        logger.info('FN:Login_requred func:{} user_key:{} account_id:{} workspace_id:{}'.format(func.__name__,user_key, account_id, workspace_id))
        
        if user_key > 0:
            g.user_key = user_key
            g.account_id = account_id
            g.workspace_id = workspace_id
            # AuthN token
            return func(*args, **kwargs)
        else:
            abort(401)

    return wrapper


# AuthN Decorator
def login_super(func):
    @wraps(func)
    def wrapper():
        if g.user_key != 1:
            abort(403)
        return func()

    return wrapper
