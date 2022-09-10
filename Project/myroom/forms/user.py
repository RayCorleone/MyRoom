# -*- coding: utf-8 -*-
"""
    @File   :   forms.user.py
    @Usage  :   个人空间表单
    @Author :   Ray
    @Version:   1.0
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('旧密码', validators=[DataRequired()])
    password = PasswordField('新密码', validators=[DataRequired(), Length(8, 128), EqualTo('password2')])
    password2 = PasswordField('确认密码', validators=[DataRequired()])
    submit = SubmitField('修改')


class ProfileForm(FlaskForm):
    number = StringField('学号/工号')   #工号/学号
    name = StringField('姓名')  #姓名
    type = StringField('职务')  #类型(Student,Teacher,Admin)
    dp = StringField('学院')    #学院