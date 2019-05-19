import time
from datetime import datetime, timedelta

from flask import render_template, request, current_app, session, redirect, url_for, g, jsonify, abort

from info import constants, db
from info.models import User, News, Category
from info.modeules.admin import admin_blu
from info.untils.captcha.response_code import RET
from info.untils.common import user_login_data
from info.untils.image_storage import storage


@admin_blu.route("/news_type", methods=["get", "post"])
def news_type():
    """
    新闻分类管理
    :return:
    """
    # 如果是get请求,那么就是渲染模板
    if request.method == "GET":
        # 查询分类数据
        try:
            # 查询所有的新闻分类
            categories = Category.query.all()
        except Exception as e:
            current_app.logger.error(e)
            return render_template("admin/news_type.html", errmsg="数据查询错误")

        category_dict_li = []

        # 将分类对象转化为字典
        for category in categories:
            # 转化为字典
            cate_dict = category.to_dict()
            category_dict_li.append(cate_dict)

        # 将最新类 这个分类删除(即不展示出来)
        category_dict_li.pop(0)
        data = {
            "categories": category_dict_li
        }

        return render_template("admin/news_type.html",
                               data=data
                               )

    # 此时说明是post请求,那么就是对数据进行操作

    # 取出参数cname, 这个就是修改后的数据,或者是新添加的数据
    cname = request.json.get("name")
    # 取出cid,如果传了的话就是修改已有的分类,如果没传的话就是新添加数据
    cid = request.json.get("id")

    # 判断参数
    if not cname:
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    # 判断是否传过来cid
    if cid:
        # 说明是修改分类
        try:
            # 将cid装换为int
            cid = int(cid)
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

        # 查询有没有这个新闻分类
        try:
            categories = Category.query.get(cid)
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

        if not categories:
            return jsonify(errno=RET.NODATA, errmsg="未查询到分类数据")

        # 将这个新闻分类的名字改为修改过得名字
        categories.name = cname

    # 此时就是没有cid,也就是说新增加新闻分类
    else:
        # 重新创建一个分类对象
        category = Category()
        category.name = cname
        db.session.add(category)

    return jsonify(errno=RET.OK, errmsg="ok")


@admin_blu.route("/news_edit_detail", methods=["get", "post"])
def news_edit_detail():
    """
    新闻编辑详情页
    编辑后跳转
    :return:
    """
    if request.method == "GET":
        #  查询点击的新闻的相关数据并传入到模板中
        news_id = request.args.get("news_id")

        # 检查数据
        if not news_id:
            abort(404)

        # 将news_id转换为int类型
        try:
            news_id = int(news_id)
        except Exception as e:
            current_app.logger.error(e)
            return render_template("admin/news_edit_detail.html", errmsg="参数错误")

        # 根据新闻id查询新闻
        try:
            news = News.query.get(news_id)
        except Exception as e:
            current_app.logger.error(e)
            return render_template("admin/news_edit_detail.html", errmsg="查询数据错误")

        if not news:
            return render_template("admin/news_edit_detail.html", errmsg="未查询数据")

        # 查询分类数据
        try:
            # 查询所有的分类
            categories = Category.query.all()
        except Exception as e:
            current_app.logger.error(e)
            return render_template("admin/news_edit_detail.html", errmsg="查询数据错误")
        category_dict_li = []
        # 对所有分类进行分类,转化为字典对象加入列表
        for category in categories:
            cate_dict = category.to_dict()
            if category.id == news.category_id:
                # 如果是当前新闻的分类，就给当前分类做一个标记
                cate_dict["is_selected"] = True
            category_dict_li.append(cate_dict)

        # 将分类中的“最新这一分类给删除”
        category_dict_li.pop(0)

        data = {
            "news": news.to_dict(),
            "categories": category_dict_li
        }

        return render_template("admin/news_edit_detail.html", data=data)

    # 取到表单提交过来的数据（post）

    # 新闻id
    news_id = request.form.get("news_id")
    # 新闻的标题
    title = request.form.get("title")
    # 新闻的摘要
    digest = request.form.get("digest")
    # 新闻的的内容
    content = request.form.get("content")
    # 新闻的图片
    index_image = request.files.get("index_image")
    # 新闻的分类id
    category_id = request.form.get("category_id")

    # 判断数据是否有值
    if not all([title, digest, content, category_id]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数有误")
    # 查询指定id的 新闻
    try:
        news = News.query.get(news_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据查询失败")
    if not news:
        return jsonify(errno=RET.NODATA, errmsg="未查询到新闻数据")

    # 读取图片
    if index_image:
        try:
            index_image = index_image.read()
        except Exception as e:
            current_app.logger.error(e)
            jsonify(errno=RET.PARAMERR, errmsg="参数有误")
        # 读取成功,将图片上传到七牛云
        try:
            key = storage(index_image)
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(errno=RET.THIRDERR, errmsg="上传图片错误")
        #
        news.index_image_url = constants.QINIU_DOMIN_PREFIX + key

        #
    news.title = title
    news.digest = digest
    news.content = content
    news.category_id = category_id
    return jsonify(errno=RET.OK, errmsg="ok")


@admin_blu.route("/news_edit")
def news_edit():
    """
    编辑新闻页面
    :return:
    """
    page = request.args.get("p", 1)
    # 获取搜索的内容
    keywords = request.args.get("keywords", None)
    # 转化为int类型
    try:
        page = int(page)
    except Exception as e:
        current_app.logger.error(e)

    # 用来保存待审核的新闻对象
    news_list = []
    # 当前页面，给一个初始值
    current_page = 1
    # 总页数
    total_page = 1
    # 过滤掉已经通过审核的新闻
    filters = [News.status == 0]
    # contains(str)包含后边字符串
    if keywords:
        filters.append(News.title.contains(keywords))
    try:
        paginate = News.query.filter(*filters).order_by(News.create_time.desc()).paginate(page,
                                                                                          constants.ADMIN_NEWS_PAGE_MAX_COUNT,
                                                                                          False)
        # 新闻内容，对象列表
        news_list = paginate.items
        # 当前页数
        current_page = paginate.page
        # 总页数
        total_page = paginate.pages
    except Exception as e:
        current_app.logger.error(e)

    # 保存新闻字典
    news_dict_list = []

    for news in news_list:
        news_dict_list.append(news.to_basic_dict())

    context = {
        "total_page": total_page,
        "current_page": current_page,
        "news_list": news_dict_list
    }
    return render_template('admin/news_edit.html', data=context)


@admin_blu.route("/news_review_action", methods=["get", "post"])
def news_review_action():
    """
    新闻审核实现
    :return:
    """
    # 1,接收参数
    news_id = request.json.get("news_id")
    action = request.json.get("action")

    # 参数校验
    if not all([news_id, action]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")
    if action not in ("accept", "reject"):
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    # 查询指定的新闻数据
    try:
        news = News.query.get(news_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据查询失败")
    if not news:
        return jsonify(errno=RET.NODATA, errmsg="未查询到数据")

    if action == "accept":
        # 代表通过审核
        news.status = 0
    else:
        # 代表没通过
        reason = request.json.get("reason")
        if not reason:
            return jsonify(errno=RET.PARAMERR, errmsg="请输入拒绝的原因")
        news.status = -1
        news.reason = reason
    return jsonify(errno=RET.OK, errmsg="ok")


@admin_blu.route("/news_review_detail/<int:news_id>")
def news_review_detail(news_id):
    # 通过id查询新闻
    news = None
    try:
        news = News.query.get(news_id)
    except Exception as e:
        current_app.logger.error(e)
    if not news:
        return render_template("admin/news_review_detail.html", data={"errmsg": "未查询此新闻"})

    return render_template("admin/news_review_detail.html", data={"news": news.to_dict()})


@admin_blu.route("/news_review")
def news_review():
    # 审核功能
    # 获取页数
    page = request.args.get("p", 1)
    # 获取搜索的内容
    keywords = request.args.get("keywords", None)
    # 转化为int类型
    try:
        page = int(page)
    except Exception as e:
        current_app.logger.error(e)

    # 用来保存待审核的新闻对象
    news_list = []
    # 当前页面，给一个初始值
    current_page = 1
    # 总页数
    total_page = 1
    # 过滤掉已经通过审核的新闻
    filters = [News.status != 0]
    # contains(str)包含后边字符串
    if keywords:
        filters.append(News.title.contains(keywords))
    try:
        paginate = News.query.filter(*filters).order_by(News.create_time.desc()).paginate(page,
                                                                                          constants.ADMIN_NEWS_PAGE_MAX_COUNT,
                                                                                          False)
        # 新闻内容，对象列表
        news_list = paginate.items
        # 当前页数
        current_page = paginate.page
        # 总页数
        total_page = paginate.pages
    except Exception as e:
        current_app.logger.error(e)

    # 保存新闻字典
    news_dict_list = []

    for news in news_list:
        news_dict_list.append(news.to_review_dict())

    context = {
        "total_page": total_page,
        "current_page": current_page,
        "news_list": news_dict_list
    }
    return render_template('admin/news_review.html', data=context)


@admin_blu.route("/user_list")
def user_list():
    # 用户列表
    page = request.args.get("page", 1)
    try:
        page = int(page)
    except Exception as  e:
        current_app.logger.error(e)
    users = []
    current_page = 1
    total_page = 1
    try:
        paginate = User.query.filter(User.is_admin == False).paginate(page, constants.ADMIN_NEWS_PAGE_MAX_COUNT, False)
        users = paginate.items
        current_page = paginate.page
        total_page = paginate.pages
    except Exception as e:
        current_app.logger.error(e)

    user_dict_li = []
    for user in users:
        user_dict_li.append(user.to_admin_dict())

    data = {
        "users": user_dict_li,
        "total_page": total_page,
        "current_page": current_page
    }

    return render_template('admin/user_list.html',
                           data=data
                           )


@admin_blu.route("/user_count")
def user_count():
    # 显示人数图表
    # 总人数
    total_count = 0
    try:
        total_count = User.query.filter(User.is_admin == False).count()
    except Exception as e:
        current_app.logger.error(e)
    # 月增长数
    mon_count = 0
    # 获取当前时间
    t = time.localtime()
    # 当前年，当前月
    begin_mon_date_str = "%d-%02d-01" % (t.tm_year, t.tm_mon)
    # 将字符串转化为datatime对象
    begin_mon_date = datetime.strptime(begin_mon_date_str, "%Y-%m-%d")
    try:
        mon_count = User.query.filter(User.is_admin == False, User.create_time > begin_mon_date).count()
    except Exception as e:
        current_app.logger.error(e)

    # 日增加量
    day_count = 0
    begin_day_date = datetime.strptime("%d-%02d-%02d" % (t.tm_year, t.tm_mon, t.tm_mday), "%Y-%m-%d")
    try:
        day_count = User.query.filter(User.is_admin == False, User.create_time > begin_day_date).count()
    except Exception as e:
        current_app.logger.error(e)

    # 折线图数据
    active_time = []
    active_count = []
    begin_today_date = datetime.strptime(("%d-%02d-%02d" % (t.tm_year, t.tm_mon, t.tm_mday)), "%Y-%m-%d")

    for i in range(0, 31):
        begin_date = begin_today_date - timedelta(days=i)
        end_date = begin_today_date - timedelta(days=i - 1)
        count = User.query.filter(User.is_admin == False, User.last_login >= begin_date,
                                  User.last_login < end_date).count()
        active_count.append(count)
        active_time.append(begin_date.strftime("%Y-%m-%d"))
    active_count.reverse()
    active_time.reverse()

    data = {
        "total_count": total_count,
        "mon_count": mon_count,
        "day_count": day_count,
        "active_time": active_time,
        "active_count": active_count
    }

    return render_template("admin/user_count.html",
                           data=data
                           )


@admin_blu.route("/index")
@user_login_data
def index():
    user = g.user
    return render_template("admin/index.html",
                           user=user.to_dict()
                           )


@admin_blu.route("/login", methods=["get", "post"])
def login():
    if request.method == "GET":
        user_id = session.get("user_id", None)
        is_admin = session.get("is_admin", False)
        if user_id and is_admin:
            return redirect(url_for("admin.index"))
        return render_template("admin/login.html")
    # 取到登录参数
    username = request.form.get("username")
    password = request.form.get("password")

    # 判断参数
    if not all([username, password]):
        return render_template("admin/login.html", errmsg="参数错误")
    print(username, password)
    # 查询当前用户
    try:
        user = User.query.filter(User.mobile == username, User.is_admin == True).first()
    except Exception as e:
        current_app.logger.error(e)
        return render_template("admin/login.html", errmsg="用户信息查询失败")

    if not user:
        return render_template("admin/login.html", errmsg="未查询到用户信息")

    if not user.check_passowrd(password):
        return render_template("admin/login.html", errmsg="用户名或者密码错误")

    # 保存用户的登录信息
    session["user_id"] = user.id
    session["mobile"] = user.mobile
    session["nick_name"] = user.nick_name
    session["is_admin"] = user.is_admin

    # 跳转后台管理首页
    return redirect(url_for("admin.index"))


@admin_blu.route("/logout", methods=["get"])
def logout():
    session.clear()
    return jsonify(errno="OK")
