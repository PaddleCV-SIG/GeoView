import os
import sys

from flask import Flask
from flask_cors import CORS

from applications.api import system_api
from applications.common.scripts import init_script
from applications.configs import config
from applications.extensions import init_plugs

# 将项目附带的PaddleRS路径添加到sys.path
_curr_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.normpath(os.path.join(_curr_dir, '../../PaddleRS')))


def create_app(config_name=None):
    app = Flask(
        os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

    if not config_name:
        # 尝试从本地环境中读取
        config_name = os.getenv('FLASK_CONFIG', 'development')

    # 引入数据库配置
    app.config.from_object(config[config_name])

    # 注册各种插件
    init_plugs(app)

    # 初始化数据库
    init_script(app)

    # 注册路由
    system_api(app)

    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['JSON_AS_ASCII'] = False
    CORS(app, supports_credentials=True)  # 设置跨域

    return app
