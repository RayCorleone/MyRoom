# -*- coding: utf-8 -*-
"""
    @File   :   settings.py
    @Usage  :   配置参数文件
    @Author :   Ray
    @Version:   1.0
"""

import os
import sys

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

## SQLite URI 配置
WIN = sys.platform.startswith('win')
if WIN: #数据库在win下
    prefix = 'sqlite:///'
else:   #数据库在linux下
    prefix = 'sqlite:////'


## 基配置
class BaseConfig:
    # 基本参数
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret string')

    # 数据库警告信息
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True

    # BootStrap 资源本地化
    BOOTSTRAP_SERVE_LOCAL = True


## 开发配置
class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = prefix + os.path.join(basedir, 'data-dev.db')
    # REDIS_URL = "redis://localhost"


## 测试配置
class TestingConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # in-memory database


## 部署配置
class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', prefix + os.path.join(basedir, 'data.db'))


## 配置实例
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}
