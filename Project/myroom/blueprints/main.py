# -*- coding: utf-8 -*-
"""
    @File   :   main.py
    @Usage  :   主页面视图函数
    @Author :   Ray
    @Version:   1.0
"""

from flask import render_template, Blueprint

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    return render_template('main/index.html')
