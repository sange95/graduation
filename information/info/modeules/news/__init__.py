# 新闻详情相关的业务逻辑
from flask import Blueprint
news_bul = Blueprint('news', __name__, url_prefix='/news')

from . import views