# coding = utf-8
import os
from redis import StrictRedis
DEBUG = True

SECRET_KEY = '123456'
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

# mysql配置
DIALECT = "mysql"
DRIVER = "pymysql"
USERNAME = "root"
PASSWORD = "199628"
HOST = "47.99.62.36"
PORT = "3306"
DATABASE = "new_shop"
# redis配置
REDIS_HOST = "47.99.62.36"
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

SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT,
                                                                       DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = False

# qq邮箱配置

MAIL_SERVER = 'smtp.qq.com'
MAIL_PROT = 25
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = "王贺"
MAIL_DEFAULT_SENDER = "101211070@qq.com"
MAIL_PASSWORD = "JACOB13483x"
MAIL_DEBUG = True



# 七牛云配置
# ALLOWED_EXT = set(['png', 'jpg', 'jpeg', 'bmp', 'gif'])
# QINIU_ACCESS_KEY = 你的七牛云QINIU_ACCESS_KEY
# QINIU_SECRET_KEY = 你的七牛云QINIU_ACCESS_KEY
# QINIU_BUCKET_NAME = 'lmx110522'
# QINIU_ACCESS_KEY = 你的QINIU_ACCESS_KEY
