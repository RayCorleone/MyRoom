# -*- coding: utf-8 -*-
"""
    @File   :   forms.auth.py
    @Usage  :   授权表单
    @Author :   Ray
    @Version:   1.0
"""

from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length
from wtforms import StringField, PasswordField, SubmitField, BooleanField


class LoginForm(FlaskForm):
    number = StringField('学号/工号', validators=[DataRequired(), Length(1, 10)])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('自动登录')
    submit = SubmitField('登  录')
