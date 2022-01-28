#!/usr/bin/python
# -*- coding: UTF-8 -*


import configparser


class Configuration():

    def __init__(self, config_file_path='./config.ini'):
        try:
            self.config_file_path = config_file_path
            self.conf = configparser.ConfigParser()
            self.conf.read(config_file_path)
            # # print('conf: ',  self.conf.sections())
        except Exception as e:
            # 文件不存在或者读取失败
            print(str(e))

    def write_file(self):
        self.conf.write(open(self.config_file_path, 'r+'))

    def get_version(self):
        return self.conf.get('Version', 'version')

    def get_build(self):
        return self.conf.get('Version', 'build')

    def get_database_name(self, database_section='DB'):

        if self.conf.has_section(database_section):
            return self.conf.get(database_section, 'name')
        return None

    def get_option(self, section, option):

        return self.conf.get(section, option)

    def set_option(self, section, option, value):

        # 修改选项
        self.conf.set(section, option, value)
        # 保存修改
        self.write_file()

    def get_database_configuration(self, database_section):

        return {
            'name': self.conf.get(database_section, 'name'),
            'type':self.conf.get(database_section, 'type'),
            'host':self.conf.get(database_section, 'host'),
            'port':self.conf.get(database_section, 'port'),
            'user':self.conf.get(database_section, 'user'),
            'pwd': self.conf.get(database_section, 'pwd')
        }

    def get_start_config(self, section='IPCONFIG'):

        host = self.conf.get(section, 'host')
        port = self.conf.get(section, 'port')
        debug = self.conf.get(section, 'debug')

        return host, port, debug


configuration = Configuration()


class Config(object):

    DEBUG = False
    TESTING = False
    SECRET_KEY = 'USER-API-DPkzlGoXTUQzfKGxJhkcbDOg9bThYO9s'
    ###flask-session
    SESSION_TYPE = 'null'
    SESSION_KEY_PREFIX = "session:"
    ########如果设置为True的话，session的生命为 permanent_session_lifetime 秒（默认是31天）
    ########如果设置为Flase的话，那么当用户关闭浏览器时，session便被删除了。permanent_session_lifetime也会生效
    SESSION_PERMANENT = False
    PERMANENT_SESSION_LIFETIME = 60 * 60 * 24 * 31

    JOBS = [
        {
            'id': 'tasks_executor',
            'func': 'schedule_task:tasks_executor',
            'args': None,
            'trigger': 'interval',
            'seconds': 300
        }
    ]
    SCHEDULER_API_ENABLED = True

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True

    DEFAULT_BUCEKT = 'torro_landing_bucket_dev_v2'
    DEFAULT_PROJECT = 'geometric-ocean-333410'
    DEFAULT_REGION = 'asia-east2'
    DEFAULT_SA = '580079130038-compute@developer.gserviceaccount.com'
    BUCEKT_CMKE = None
    pass


class TestingConfig(Config):
    TESTING = False

    DEFAULT_BUCEKT = 'torro_ai_landing_bucket_testing'
    DEFAULT_PROJECT = 'geometric-ocean-333410'
    DEFAULT_REGION = 'asia-east2'
    DEFAULT_SA = '580079130038-compute@developer.gserviceaccount.com'
    BUCEKT_CMKE = None
    pass


class ProductionConfig(Config):
    DEBUG = False

    DEFAULT_BUCEKT = 'torro_ai_landing_bucket_prod'
    DEFAULT_PROJECT = 'geometric-ocean-333410'
    DEFAULT_REGION = 'asia-east2'
    DEFAULT_SA = '580079130038-compute@developer.gserviceaccount.com'
    BUCEKT_CMKE = None
    pass


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
