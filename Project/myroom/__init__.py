# -*- coding: utf-8 -*-
"""
    @File   :   __init__.py
    @Usage  :   程序包的构造文件
    @Author :   Ray
    @Version:   1.0
"""

import os
import click

from flask import Flask
from flask_login import current_user

from myroom.blueprints.auth import auth_bp
from myroom.blueprints.main import main_bp
from myroom.blueprints.user import user_bp
from myroom.blueprints.admin import admin_bp
from myroom.blueprints.search import search_bp
from myroom.blueprints.booking import booking_bp

from myroom.settings import config
from myroom.extensions import db,login_manager,bootstrap,moment,csrf
from myroom.models import Building,Room,Department,Course,User,Event,OpenCourse


## 工厂函数
def create_app(config_name = None):
    # 加载配置
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')    

    # 创建实例
    app = Flask('myroom')
    app.config.from_object(config[config_name])

    # 相关注册
    register_extensions(app)        #注册扩展
    register_blueprints(app)        #注册蓝本
    register_commands(app)          #注册自定义命令
    register_errors(app)            #注册错误处理
    register_shell_context(app)     #注册shell上下文处理
    register_template_context(app)  #注册模板上下文处理

    return app


## 注册扩展函数
def register_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    moment.init_app(app)
    csrf.init_app(app)


## 注册蓝本函数
def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(search_bp, url_prefix='/search')
    app.register_blueprint(booking_bp, url_prefix='/booking')


## 注册shell上下文处理函数
def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db, Building=Building, Room=Room,
            Department=Department, Course=Course, User=User,
            Event=Event, OpenCourse=OpenCourse)


## 注册模板上下文处理函数
def register_template_context(app):
    @app.context_processor
    def make_template_context():
        if current_user.is_authenticated:
            pass
        return dict()


## 注册错误处理函数
def register_errors(app):
    pass


## 注册命令行窗口的命令
def register_commands(app):
    # 显示作者信息指令
    @app.cli.command()
    @click.option('--age', is_flag=True, help='Show author\'s age.')
    @click.option('--height', is_flag=True, help='Show author\'s height.')
    @click.option('--status', is_flag=True, help='Show author\'s marital status.')
    @click.option('--wechat', is_flag=True, help='Show author\'s wechat ID.')
    def author(age, height, status, wechat):
        click.echo('@Name: Ray')
        if age:
            click.echo('@Age: (Sorry, but it\'s a SECRET)')
        if height:
            click.echo('@Height: 170 ~ 180 cm')
        if status:
            click.echo('@Status: Available')
        if wechat:
            click.echo('@Wechat: RayHuC')
        click.echo('@Page: https://github.com/RayCorleone')

    # 初始化数据库指令
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        if drop:
            click.confirm('This operation will delete the database, do you want to continue?', abort=True)
            db.drop_all()
            click.echo('Drop tables.')
        db.create_all()
        click.echo('Initialized database.')

    # 加载原始数据指令
    @app.cli.command()
    def initdata():
        from myroom.fakes import fake_building,fake_room,fake_department,fake_course,fake_admin,fake_user,fake_open_course,fake_event

        db.drop_all()
        db.create_all()

        click.echo('Generating 6 buildings...')
        fake_building()
        click.echo('Generating 360 rooms...')
        fake_room()
        click.echo('Generating 7 departments...')
        fake_department()
        click.echo('Generating 1000 courses...')
        fake_course()
        click.echo('Generating the administrator...')
        fake_admin()
        click.echo('Generating 400 users...')
        fake_user()
        click.echo('Generating 2300 opencourses...')
        fake_open_course()
        click.echo('Generating 50 events...')
        fake_event()

        click.echo('Done.')
