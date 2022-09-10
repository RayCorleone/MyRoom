# -*- coding: utf-8 -*-
"""
    @File   :   user.py
    @Usage  :   用户界面视图函数
    @Author :   Ray
    @Version:   1.0
"""

from flask_login import login_required, current_user, logout_user
from flask import render_template, flash, redirect, url_for, Blueprint

from myroom.extensions import db
from myroom.forms.user import ProfileForm, ChangePasswordForm

user_bp = Blueprint('user', __name__)


@user_bp.route('/profile')
@login_required
def index():
    form = ProfileForm()

    type = '学生'
    if current_user.type == 'Teacher':
        type = '老师'
    elif current_user.type == 'Admin':
        type = '管理员'
    else:
        type = '学生'

    form.number.data = current_user.number
    form.name.data = current_user.name
    form.type.data = type
    form.dp.data = current_user.department.name

    return render_template('user/profile.html', form=form)


@user_bp.route('/change-password', methods=['GET', 'POST'])
def change_pwd():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.validate_password(form.old_password.data):
            current_user.set_password(form.password.data)
            db.session.commit()
            flash('Password updated.', 'success')
            logout_user()
            return redirect(url_for('auth.login'))
        else:
            flash('Old password is incorrect.', 'warning')
    return render_template('user/change_pwd.html', form=form)
