import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, g, render_template
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import generate_csrf
from pymongo import MongoClient
from redis import StrictRedis

# from config import Config
from config import config

# 初始化MySQL数据库 # 在flask很多扩展里面都可以先初始化扩展的对象，然后再去调用init_app方法去初始化


db = SQLAlchemy()
redis_store = None  # type: StrictRedis
collection = None  # type: MongoClient


def setup_log(config_name):
    # 设置日志的记录等级
    logging.basicConfig(level=config[config_name].DEBUG)  # 调试debug级
    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
    file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024 * 1024 * 100, backupCount=10)
    # 创建日志记录的格式 日志等级 输入日志信息的文件名 行数 日志信息
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flask app使用的）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)


def create_app(config_name):
    # 配置日志,并且传入配置名字，以便能获取到指定配置对应的日志文件
    setup_log(config_name)
    # 创建flask对象
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    # 通过app初始化
    db.init_app(app)
    # 初始化redis存储对象
    global redis_store
    redis_store = StrictRedis(host=config[config_name].REDIS_HOST, port=config[config_name].REDIS_PORT,
                              decode_responses=True)
    # 初始化mongodb
    global collection
    client = MongoClient(config[config_name].MONGODB_HOST, config[config_name].MONGODB_PORT)
    collection = client[config[config_name].MONGODB_NAME][config[config_name].MONGODB_SET]
    # 开启当前项目的CSRF保护
    # CSRF帮我们做了： cookie取出随机值，表单中取出随机值，进行校验，返回响应结果
    # 没有帮我们做：1，在界面加载的时候，网cookie中添加有一个csrf_token,并且在表单中添加个隐藏的csrf_token
    # 我们用的ajax，所以我们在请求的时候带上这个csrf的值
    # CSRFProtect(app)
    # 设置将session保存的位置的扩展包
    Session(app)

    from info.untils.common import user_login_data

    @app.errorhandler(404)
    @user_login_data
    def page_not_fount(e):
        user = g.user
        data = {"user": user.to_dict() if user else None}
        return render_template("news/404.html", data=data)

    @app.after_request
    def after_request(response):
        # 生成随机的csrf_token的值
        csrf_token = generate_csrf()
        # 设置一个cookie
        response.set_cookie("csrf_token", csrf_token)
        return response

    from info.modeules.index import index_blu
    app.register_blueprint(index_blu)
    # 注册蓝图
    from info.modeules.passport import passport_bul
    app.register_blueprint(passport_bul)
    from info.modeules.news import news_bul
    app.register_blueprint(news_bul)
    from info.modeules.profile import profile_blu
    app.register_blueprint(profile_blu)
    from info.modeules.admin import admin_blu
    app.register_blueprint(admin_blu, url_prefix="/admin")
    from info.modeules.rent import rent_bul
    app.register_blueprint(rent_bul)
    from info.modeules.appointment import appointment_bul
    app.register_blueprint(appointment_bul)

    return app
