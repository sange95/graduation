
import os

DEBUG = True

SECRET_KEY = '123456'

DIALECT = 'mysql'
DRIVER = 'pymysql'
HOST = '47.99.62.36'
PORT = '3306'
USERNAME = 'root'
PASSWORD = '199628'
DATABASE = 'zhi_hu'

SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(DIALECT, DRIVER,
                                                                       USERNAME, PASSWORD, HOST, PORT, DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = False