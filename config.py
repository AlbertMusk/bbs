# encoding: utf-8
# author = 'Albert_Musk'

import os

DEBUG = True
SECRET_KEY = os.urandom(24)
TEMPLATE_AUTO_UPDATE = True

# 数据库config
DIALECT = 'mysql'
DRIVER = 'pymysql'
HOSTNAME = '127.0.0.1'
PORT = 3306
DATABASE = 'zlbbs'
USERNAME = 'root'
PASSWORD = 'root'
SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(DIALECT,DRIVER,USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)

SQLALCHEMY_TRACK_MODIFICATIONS = False


# 常量
CMS_USER_ID = ''

# mail配置
MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
# MAIL_USE_SSL = False
MAIL_USERNAME = '744205975@qq.com'
MAIL_PASSWORD = 'rjxcabktszmmbeef'
MAIL_DEFAULT_SENDER = '744205975@qq.com'

# 阿里大于配置
ALIDAYU_APP_KEY = 'LTAIH91wWNsskcWf'
ALIDAYU_APP_SECRET = 'TnGqCINFXqw6P2hTFvopAVkiCmmHPW'
ALIDAYU_SIGN_NAME = 'python论坛'
ALIDAYU_TEMPLATE_CODE = 'SMS_130846017'