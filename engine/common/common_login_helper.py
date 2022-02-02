#!/usr/bin/python
# -*- coding: UTF-8 -*

from functools import wraps
from os import abort
from flask import request, g
from utils.auth_helper import Auth

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user_key, account_id, workspace_id = Auth.identify(request)
        print('FN:Login_requred: func: 'func.__name__,' user_key: ', user_key, account_id, workspace_id)
        if user_key > 0:
            g.user_key = user_key
            g.account_id = account_id
            g.workspace_id = workspace_id
            ###token验证，服务于restful
            return func(*args, **kwargs)
        else:
            abort(401)

    return wrapper


###权限验证装饰器
def login_super(func):
    @wraps(func)
    def wrapper():
        if g.user_key != 1:
            abort(403)
        return func()

    return wrapper
