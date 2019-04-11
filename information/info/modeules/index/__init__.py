from flask import Blueprint

# 创建蓝图对象
index_blu = Blueprint('index', __name__)

# 注册路由
from . import views