# -*- coding: utf-8 -*-
"""
    @File   :   decorators.py
    @Usage  :   装饰器文件
    @Author :   Ray
    @Version:   1.0
"""

from functools import wraps
from flask import Markup, flash, abort
from flask_login import current_user

from myroom.utils import redirect_back


## 需要管理员权限(flash信息)
def admin_required_flash(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            message = Markup('Only Administrator can access these data.')
            flash(message, 'warning')
            return redirect_back()
        return func(*args, **kwargs)
    return decorated_function


## 不允许管理员访问(flash信息)
def not_admin_required_flash(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.is_admin:
            message = Markup('Administrator can\'t use these function.')
            flash(message, 'warning')
            return redirect_back()
        return func(*args, **kwargs)
    return decorated_function


# 需要管理员权限(403界面)
def admin_required_403(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            abort(403)
        return func(*args, **kwargs)
    return decorated_function
