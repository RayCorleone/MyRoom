# -*- coding: utf-8 -*-
"""
    @File   :   wsgi.py
    @Usage  :   Flask程序入口
    @Author :   Ray
    @Version:   1.0
"""

import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

from myroom import create_app

# development-开发  production-部署  testing-测试
app = create_app('development')