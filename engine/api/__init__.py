#!/usr/bin/python
# -*- coding: UTF-8 -*

from flask import Flask
from flask_cors import CORS
from flask_docs import ApiDoc
from api.resource import api
from config import config, Config
from flask_apscheduler import APScheduler
import logging

# Get the logger specified in the file
logger = logging.getLogger("main." + __name__)

def create_app(config_name):
    
    logger.info("FLASK:Initiating Torro Engine Start Sequence")
    logger.info("")
    logger.info("            ______                        ___    ____")
    logger.info("           /_  __/___  ______________    /   |  /  _/")
    logger.info("            / / / __ \/ ___/ ___/ __ \  / /| |  / /  ")
    logger.info("           / / / /_/ / /  / /  / /_/ / / ___ |_/ /   ")
    logger.info("          /_/  \____/_/  /_/   \____(_)_/  |_/___/   ")
    logger.info("")
    
    app = Flask(__name__)
    # 验证
    CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    ###初始化数据库
    # db.init_app(app)
    scheduler = APScheduler()
    # 返回数据中response为中文
    app.config['JSON_AS_ASCII'] = False
    app.config['SESSION_COOKIE_SAMESITE'] = 'None'
    # app.config['SESSION_COOKIE_SECURE'] = True

    scheduler.init_app(app)
    scheduler.start()
    ###初始化日志###
    api.init_app(app)
    ApiDoc(app)
    logger.info("FLASK:Torro Engine is up and running!")

    return app
