# -*- coding: utf-8 -*-
"""
    @File   :   auth.py
    @Usage  :   登录授权视图函数
    @Author :   Ray
    @Version:   1.0
"""

from flask import Blueprint, redirect, flash, url_for, render_template
from flask_login import login_user, logout_user, login_required, current_user

from myroom.models import User
from myroom.forms.auth import LoginForm

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        num = form.number.data
        pwd = form.password.data
        rmb = form.remember_me.data

        user = User.query.filter_by(number=num).first()
        if user is not None:
            if user.validate_password(pwd):
                login_user(user, rmb)
                flash('Login success.', 'info')
                return redirect(url_for('main.index'))
            else:
                flash('Invalid password.', 'warning')
        else:
            flash('Invalid number.', 'warning')
    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout success.', 'info')
    return redirect(url_for('main.index'))
