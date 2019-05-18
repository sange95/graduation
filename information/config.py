import logging

from redis import StrictRedis
from pymongo import MongoClient


class Config(object):
    """项目配置"""
    DEBUG = True

    SECRET_KEY = '123456'
    # mysql数据库的配置
    SQLALCHEMY_DATABASE_URI = "mysql://root:199628@47.99.62.36:3306/information"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 在请求结束的时候，如果指定此配置为True，那么SQLAlchemy会自动执行一次db.session.commit()操作
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    # Redis的配置
    REDIS_HOST = '47.99.62.36'
    REDIS_PORT = 6379
    # Session保存位置
    SESSION_TYPE = 'redis'
    # 是剖session签名
    SESSION_USE_SIGNER = True
    # 指定session保存的redis
    SESSION_REDIS = StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    # 设置需要过期
    SESSION_PERMANENT = False
    # 设置过期时间
    PERMANENT_SESSION_LIFETIME = 86400 * 2

    # 设置日志等级
    LOG_LEVEL = logging.DEBUG
    # mongodb的配置
    MONGODB_HOST = "47.99.62.36"
    MONGODB_PORT = 27017
    MONGODB_NAME = 's'
    MONGODB_SET = 's'


class DevelopmentConfig(Config):
    """开发环境下的配置"""
    DEBUG = True
    # 设置日志等级
    LOG_LEVEL = logging.ERROR


class ProductionConfig(Config):
    """生产环境下的配置"""
    DEBUG = False
    # SQLALCHEMY_DATABASE_URI = "mysql://root:mysql@localhost:3306/information"


class TestingConfig(Config):
    DEBUG = True
    TESTING = True


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig
}
