import uuid

from flask import render_template, g, redirect, request, jsonify, current_app, session, abort

from info import db, constants
from info.models import User, Category, News
from info.modeules.profile import profile_blu
from info.untils.captcha.response_code import RET
from info.untils.common import user_login_data
from info.untils.image_storage import storage


@profile_blu.route("/other_news_list")
def other_news_list():
    """
    返回指定用户的发布的新闻
    :return:
    """
    # 取出参数
    other_id = request.args.get("user_id")
    page = request.args.get("p", 1)

    # 判断参数
    try:
        page = int(page)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")
    try:
        other = User.query.get(other_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据查询失败")
    if not other:
        return jsonify(errno=RET.NODATA, errmsg="当前用户不存在")

    try:
        paginate = other.news_list.paginate(page, constants.USER_COLLECTION_MAX_NEWS, False)
        # 获取当前页的数据
        news_li = paginate.items
        # 获取当前页
        current_page = paginate.page
        # 获取总页数
        total_page = paginate.pages
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据查询失败")

    news_dict_li = []

    for news_item in news_li:
        news_dict_li.append(news_item.to_basic_dict())

    data = {
        "news_list": news_dict_li,
        "total_page": total_page,
        "current_page": current_page
    }
    return jsonify(errno=RET.OK, errmsg="ok", data=data)


@profile_blu.route("/other_info")
@user_login_data
def other_info():
    """
    展示关注的人的个人主页
    :return:
    """

    # 获取登录用户的信息
    user = g.user
    # 查询其他人的用户信息
    other_id = request.args.get("user_id")

    if not other_id:
        abort(404)
    other = None
    # 查询指点id的用户信息
    try:
        other = User.query.get(other_id)
    except Exception as e:
        current_app.logger.error(e)

    if not other:
        abort(404)

    # 默认是没有关注的
    is_followed = False

    # 如果当前新闻有作者,而且当前用户已经登录,并且且当前登录的用户关注列表中有这个用户
    if other and user:
        if other in user.followed:
            is_followed = True

    data = {
            "is_followed": is_followed,
            "user": g.user.to_dict() if g.user else None,
            "other_info": other.to_dict()
            }
    return render_template("news/other.html",data=data)


@profile_blu.route("/user_follow")
@user_login_data
def user_follow():
    """
    关注的人的主页
    :return:
    """
    # 获取页数
    p = request.args.get("p", 1)
    try:
        p = int(p)
    except Exception as e:
        current_app.logger.error(e)
        p = 1

    # 获取当前的登录用户
    user = g.user

    follows = []
    current_page = 1
    total_page = 1
    try:
        paginate = user.followed.paginate(p, constants.USER_FOLLOWED_MAX_COUNT, False)
        # 获取当前页的数据
        follows = paginate.items
        # 获取当前页
        current_page = paginate.page
        # 获取总页数
        total_page = paginate.pages
    except Exception as e:
        current_page.logger.error(e)

    user_dict_li = []

    for follow_user in follows:
        user_dict_li.append(follow_user.to_dict())

    data = {
        "users": user_dict_li,
        "total_page": total_page,
        "current_page": current_page
    }

    return render_template("news/user_follow.html",
                           data=data
                           )


@profile_blu.route("/news_list")
@user_login_data
def user_news_list():
    # 获取参数
    # 获取页数
    page = request.args.get("p", 1)

    # 将页数转化为int型
    try:
        page = int(page)
    except Exception as e:
        current_app.logger.error(e)
        # 当用话传过来的参数错误的时候，我们给恢复到第一页
        page = 1
    # 获取当前用户
    user = g.user
    #
    news_list = []
    #
    total_page = 1
    #
    current_page = 1

    try:
        # 第一个参数为第几页，第二个为每页显示多少个，第三个参数？？？
        paginate = News.query.filter(News.user_id == user.id).paginate(page, constants.USER_COLLECTION_MAX_NEWS, False)
        # 获取然当前页
        current_page = paginate.page
        # 获取总页数
        total_page = paginate.pages
        # 获取分页数据
        news_list = paginate.items
    except Exception as e:
        current_app.logger.error(e)

    news_dict_li = []
    for news in news_list:
        news_dict_li.append(news.to_review_dict())

    data = {
        "news_list": news_dict_li,
        "total_page": total_page,
        "current_page": current_page,
    }

    return render_template("news/user_news_list.html",
                           data=data)


@profile_blu.route("/news_release", methods=["get", 'post'])
@user_login_data
def news_release():
    # 发布新闻页面显示
    # 若果是get请求，那么就是渲染页面
    if request.method == "GET":
        categories = []
        try:
            # 查询出所有的新闻分类
            categories = Category.query.all()
        except Exception as e:
            current_app.logger.error(e)

        category_dict_li = []
        for category in categories:
            category_dict_li.append(category)

        # 在发布新闻的时候不应该有最新这一项，所以我们给这个最新给删除
        category_dict_li.pop(0)

        return render_template("news/user_news_release.html",
                               data={
                                   "categories": category_dict_li
                               }
                               )
    # 到此处说明请方式是post请求

    # 1,先获取提交过来的的数据
    # 获取标题
    title = request.form.get("title")
    # 新闻来源
    source = "个人发布"
    # 摘要
    digest = request.form.get("digest")
    # 新闻内容
    content = request.form.get("content")
    # 索引图片
    index_image = request.files.get("index_image")
    # 分类id
    category_id = request.form.get("category_id")

    # 校验参数
    # 2.1 判断数据是否有值
    if not all([title, source, digest, content, index_image, category_id]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数有误")

    try:
        category_id = int(category_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg="参数有误")

    # 取到图片，讲图片上传到七牛云
    try:
        # 将收到的图片读取
        index_image_data = index_image.read()
        # 上传到七牛云
        # key = storage(index_image_data)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg="参数有误")
    pic_name = str(uuid.uuid1()) + ".jpg"
    # print(url)
    # print(url)
    with open("info/static/picture/" + pic_name, "wb") as f:
        f.write(index_image_data)
    # 创建一个新闻对象
    news = News()
    news.title = title
    news.source = source
    news.digest = digest
    news.content = content
    news.index_image_url = "/static/picture/"+ pic_name
    news.category_id = category_id
    news.title = title
    news.user_id = g.user.id

    # 审核状态
    news.status = 1
    try:
        db.session.add(news)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg="数据保存失败")
    return jsonify(errno=RET.OK, errmsg="OK")


@profile_blu.route("/collection")
@user_login_data
def user_collection():
    """
    对收藏的数据进行加载
    :return:
    """
    # 获取页数
    p = request.args.get("p", 1)

    # 将页数转化为int型
    try:
        page = int(p)
    except Exception as e:
        current_app.logger.error(e)
        # 当用户传过来的参数错误的时候，我们给恢复到第一页
        page = 1
    # 获取当前用户
    user = g.user
    #
    news_list1 = []
    #
    total_page = 1
    #
    current_page = 1

    try:
        # 第一个参数为第几页，第二个为每页显示多少个，第三个参数？？？
        paginate = user.collection_news.paginate(page, constants.USER_COLLECTION_MAX_NEWS, False)
        # 获取当前页
        current_page = paginate.page
        # 获取总页数
        total_page = paginate.pages
        # 获取分页数据
        news_list1 = paginate.items
    except Exception as e:
        current_app.logger.error(e)

    news_dict_li = []
    for news in news_list1:
        news_dict_li.append(news)

    data = {
        "total_page": total_page,
        "current_page": current_page,
        "news_dict_li": news_dict_li
    }

    return render_template('news/user_collection.html', data=data)


@profile_blu.route("/pass_info", methods=["get", "post"])
@user_login_data
def pass_info():
    if request.method == "GET":
        return render_template("news/user_pass_info.html")

    # 1,获取参数
    old_password = request.json.get("old_password")
    news_password = request.json.get("new_password")

    # 2,校验参数
    if not all([old_password, news_password]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    # 3,判断旧密码是否正确
    user = g.user
    if not user.check_passowrd(old_password):
        return jsonify(errno=RET.PWDERR, errmsg="原密码错误")

    # 4,设置新密码
    user.password = news_password

    return jsonify(errno=RET.OK, errmsg="ok")


@profile_blu.route('/pic_info', methods=['post', 'get'])
@user_login_data
def pic_info():
    """
    上传头像
    :return:
    """

    # 接口： avatar----> 头像 ，图片文件
    user = g.user
    if request.method == "GET":
        return render_template('news/user_pic_info.html',
                               data=({"user": user.to_dict()})
                               )


    # 1，获取文件
    try:
        avatar_file = request.files.get("avatar").read()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg="读取文件出错")
    print(avatar_file)
    pic_name = str(uuid.uuid1())+".jpg"
    # print(url)
    # print(url)
    with open("info/static/picture/"+pic_name, "wb") as f:
        f.write(avatar_file)
    # 2，将文件上传到七牛云
    # try:
    #     url = storage(avatar_file)
    # except Exception as e:
    #     current_app.logger.error(e)
    #     return jsonify(errno=RET.THIRDERR, errmsg="上传图片失败")

    # 3，更新用户模型中的头像信息

    # 设置用户模型的的相关数据
    user.avatar_url = "/static/picture/"+pic_name
    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg="保存失败")

    # 4，返回响应，讲文件的路径返回
    return jsonify(errno=RET.OK, errmsg="ok", data={
        "avatar_url": user.avatar_url
    })


@profile_blu.route('/base_info', methods=['post', 'get'])
@user_login_data
def base_info():
    """
    用户基本信息
    1. 获取用户登录信息
    2. 获取到传入参数
    3. 更新并保存数据
    4. 返回结果
    :return:
    """
    user = g.user
    if request.method == "GET":
        return render_template('news/user_base_info.html',
                               data=({"user": g.user.to_dict()})
                               )
    # 更改后的昵称
    nick_name = request.json.get("nick_name")
    # 签名
    signature = request.json.get("signature")
    # 性别
    gender = request.json.get("gender")
    # 校验参数

    if not all(["nick_name", 'signature', 'gender']):
        return jsonify(errno=RET.DATAERR, errmsg="数据错误")
    # 校验性别
    if gender not in ("MAN", "WOMAN"):
        return jsonify(errno=RET.DATAERR, errmsg="数据错误")
    # 更新并保存数据
    user.nick_name = nick_name
    user.signature = signature
    user.gender = gender
    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="修改失败")
    session["nick_name"] = nick_name
    data = {
        "user": user.to_dict() if user else None,
    }

    return jsonify(errno=RET.OK, errmsg="ok", data=data)


@profile_blu.route('/info')
@user_login_data
def user_info():
    user = g.user
    if not user:
        return redirect('/')
    data = {"user": user.to_dict()}
    return render_template("news/user.html",
                           data=data
                           )