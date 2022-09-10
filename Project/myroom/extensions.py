# -*- coding: utf-8 -*-
"""
    @File   :   extensions.py
    @Usage  :   实例化扩展类
    @Author :   Ray
    @Version:   1.0
"""

from flask_moment import Moment
from flask_wtf import CSRFProtect
from flask_bootstrap import Bootstrap4
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, AnonymousUserMixin

db = SQLAlchemy()               # 数据库
moment = Moment()               # 日期处理
csrf = CSRFProtect()            # CSRF认证
bootstrap = Bootstrap4()        # Bootstrap框架
login_manager = LoginManager()  # 登录管理


@login_manager.user_loader
def load_user(user_id):
    from myroom.models import User
    user = User.query.get(int(user_id))
    return user


login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'warning'
login_manager.refresh_view = 'auth.re_authenticate'
login_manager.needs_refresh_message_category = 'warning'


## 准备匿名用户(未登录用户)
class Guest(AnonymousUserMixin):
    @property
    def is_admin(self):
        return False

login_manager.anonymous_user = Guest
