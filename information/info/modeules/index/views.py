from info.models import User, News, Category
from info.untils.captcha.response_code import RET
from info.untils.common import user_login_data
from . import index_blu
from flask import render_template, current_app, session, request, jsonify, g
from info import collection


@index_blu.route('/news_list')
def news_list():
    """o
    获取参数
    :return:
    """

    # 1，获取参数
    # 新闻的分类id

    cid = request.args.get("cid", "1")
    page = request.args.get("page", "1")
    per_page = request.args.get("per_page", "10")
    print(cid)
    # 2, 校验参数
    try:
        page = int(page)
        cid = int(cid)
        per_page = int(per_page)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(error=RET.PARAMERR, errmsg="参数")

    filters = [News.status == 0]
    if cid != 1:  # 查询的不是最近的数据
        # 需要添加条件
        filters.append(News.category_id == cid)

    # 3，查询数据
    try:
        paginate = News.query.filter(*filters).order_by(News.create_time.desc()).paginate(page, per_page, False)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据查询错误")
    # 取到当前数据
    news_model_list = paginate.items  # 模型对象列表
    total_page = paginate.pages
    current_page = paginate.page
    news_dict_li = []
    # 将模型列表转化为字典列表
    for news in news_model_list:
        news_dict_li.append(news.to_basic_dict())

    data = {
        "total_page": total_page,
        "current_page": current_page,
        "news_dict_li": news_dict_li
    }
    return jsonify(errno=RET.OK, errmsg="ok", data=data)


@index_blu.route('/new_index')
@user_login_data
def index():
    # redis_store.set('name', 'huanghaibo')
    """
    显示首页
    1,如果用户已经登录，将当前登录用户的数据传到模板中，显示
    :return:
    """
    user_id = session.get('user_id', None)
    user = None
    if user_id:
        try:
            user = User.query.get(user_id)
            print(user)
        except Exception as e:
            current_app.logger.error(e)
    user = g.user
    #  右侧新闻排行逻辑
    news_list = []
    cid = request.args.get("cid", "1")
    try:
        news_list = News.query.order_by(News.clicks.desc()).limit(6)
    except Exception as e:
        current_app.logger.error(e)

    news_dict_li = []
    # 遍历对象列表
    for news in news_list:
        # print(news)
        news_dict_li.append(news.to_basic_dict())
    # 查询分类数据， 通过末班形式展示出来
    categories = Category.query.all()
    category_li = []
    for category in categories:
        category_li.append(category)

    data = {
        "user": user.to_dict() if user else None,
        "news_dict_li": news_dict_li,
        "category_li": category_li,
        "cid": cid
    }
    return render_template('news/index.html',
                           data=data,
                           )


# 打开网页，浏览器会默认去请求根路径+favicon.ico做网站的标签头标
# send_static_file是flask去查找指定的静态文件所用的方法
@index_blu.route('/favicon.ico')
def favicon():
    # print(current_app.name)
    return current_app.send_static_file('news/favicon.ico')


@index_blu.route('/cluster')
def cluster():
    print('hhhhhhhhhhhhh')
    return jsonify({"hahha": "hahahh"})


@index_blu.route('/')
@user_login_data
def supindex():
    # redis_store.set('name', 'huanghaibo')
    """
    显示首页
    1,如果用户已经登录，将当前登录用户的数据传到模板中，显示
    :return:
    """
    user_id = session.get('user_id', None)
    user = None
    if user_id:
        try:
            user = User.query.get(user_id)
            print(user)
        except Exception as e:
            current_app.logger.error(e)
    user = g.user
    # mongo查询数据

    result = collection.find().limit(5)
    rent_data = []
    for data in result:
        rent_data.append({
            "_id": data["_id"],
            "area": data["local"],
            "apart": data["xiaoqu_name"][0],
            "square": data["jianzumianji"] if data["jianzumianji"] else 0,
            "price": data["money"] if data["money"] else 0,
            "house_type": data["huxing"] if data["huxing"] else "一室一厅",
        })
    data = {
        "user": user.to_dict() if user else None,
    }
    return render_template('supindex.html',
                           data=data,
                           )
