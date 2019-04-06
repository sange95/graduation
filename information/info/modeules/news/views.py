from flask import render_template, current_app, session, g, abort, request, jsonify, json

from info import constants, db
from info.models import News, User, Comment, CommentLike, Category
from info.modeules.news import news_bul
from info.untils.captcha.response_code import RET
from info.untils.common import user_login_data


@news_bul.route("/followed_user", methods=["post"])
@user_login_data
def followed_user():
    """
    关注或者取消关注用户
    :return:
    """
    # 取到当前用户的登录信息
    user = g.user
    if not user:
        return jsonify(errno=RET.SESSIONERR, errmsg="未登录")

    # 取参数
    user_id = request.json.get("user_id")
    print(type(user_id))
    action = request.json.get("action")

    if not all([user_id, action]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    # 对参数进行判断
    if action not in ("follow", "unfollow"):
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")
    try:
        user_id = int(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    # 根据传过来的被关注的用户id,查询有没有这个.
    try:
        other = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据查询错误")
    if not other:
        return jsonify(errno=RET.NODATA, errmsg="未查询到数据")
    if action == "follow":
        if other not in user.followed:
            # 当前用户的关注列表添加一个值
            user.followed.append(other)
        else:
            return jsonify(errno=RET.DATAEXIST, errmsg="当前用户已经被关注")
    else:
        # 取消关注
        if other in user.followed:
            user.followed.remove(other)
        else:
            return jsonify(errno=RET.DATAEXIST, errmsg="当前用户已经未被关注")
    return jsonify(errno=RET.OK, errmsg="ok")


@news_bul.route("/comment_like", methods=["post"])
@user_login_data
def comment_like():
    """
    点赞评论
    :return:
    """
    # 验证用户是否登录
    user = g.user
    if not user:
        return jsonify(errno=RET.SESSIONERR, errmsg="用户未登录")
    #
    # news_id = request.json.get("news_id")
    # 获取评论的id
    comment_id = request.json.get("comment_id")
    # 点赞操作类型：add(点赞)，remove(取消点赞)
    action = request.json.get("action")
    # 判断操作类型，点赞或者取消点赞
    if not all([comment_id, action]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")
    # 判断传过来的参数action，是否是正确的参数
    if action not in ['add', "remove"]:
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")
    try:
        # 将评论的id转化为int类型
        comment_id = int(comment_id)
        # news_id = int(news_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")
    try:
        # 查询id为comment_id的评论
        comment = Comment.query.get(comment_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据查询错误")
    # 如果没有这个评论
    if not comment:
        return jsonify(errno=RET.NODATA, errmsg="评论不存在")
    # 如果是添加的操作
    if action == "add":
        #
        comment_like_model = CommentLike.query.filter(CommentLike.user_id == user.id,
                                                      CommentLike.comment_id == comment.id).first()

        #
        if not comment_like_model:
            comment_like_model = CommentLike()
            comment_like_model.user_id = user.id
            comment_like_model.comment_id = comment.id
            db.session.add(comment_like_model)
            comment.like_count += 1

    else:
        #
        comment_like_model = CommentLike.query.filter(CommentLike.user_id == user.id,
                                                      CommentLike.comment_id == comment.id).first()
        if comment_like_model:
            db.session.delete(comment_like_model)
            comment.like_count -= 1
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据操作失败")
    return jsonify(errno=RET.OK, errmsg="OK")


@news_bul.route("/news_comment", methods=["post"])
@user_login_data
def comment_news():
    """
    评论新闻或者回复指定的评论
    :return:
    """
    user = g.user
    if not user:
        return jsonify(errno=RET.SESSIONERR, errmsg="用户未登录")
    #
    news_id = request.json.get("news_id")
    comment_content = request.json.get("comment")
    parent_id = request.json.get("parent_id")
    #
    if not all([news_id, comment_content]):
        return jsonify(errno=RET.PARAMERR, errmsg="+++参数错误++++")

    try:
        news_id = int(news_id)
        if parent_id:
            parent_id = int(parent_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")
    #
    comment = Comment()
    comment.user_id = user.id
    comment.news_id = news_id
    comment.content = comment_content
    if parent_id:
        comment.parent_id = parent_id
    #
    try:
        # 此处为什么要自己commit？
        db.session.add(comment)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
    # 为什么要传comment?
    return jsonify(errno=RET.OK, errmsg="OK", data=comment.to_dict())


# 利用装饰器，对传进来的id在数据库中查询对应的作user,保存在g中
@news_bul.route('/news_collect', methods=["post"])
@user_login_data
def collect_news():
    """
    收藏新闻
    1,接收参数
    2.判断参数
    :return:
    """
    # 从应用上下文g中取出user（g为全局变量）
    user = g.user
    # 判断用户是否登录
    if not user:
        return jsonify(errno=RET.SESSIONERR, errmsg="用户未登录")

    # 1, 接收参数
    # print(type(request.data))
    # print(request.data)
    # 到这一步说明用户已经登陆了，开始取出数据：news_id-->新闻的id，action--->收藏或者是取消收藏
    # action（'collect', 'cancel_collect'）--->收藏或者是取消收藏
    news_id = json.loads(request.data).get("news_id")
    action = json.loads(request.data).get("action")
    # 2.判断参数
    # 判断是否为空
    if not all([news_id, action]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")
    # 判断请求的参数是不是收藏或者取消收藏
    if action not in ["collect", "cancel_collect"]:
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")
    try:
        # 给新闻id进行处理，转成int类型
        news_id = int(news_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")
    # 查询新闻，并判断新闻是否存在
    try:
        # 根据新闻id查询新闻
        news = News.query.get(news_id)
    except Exception as e:
        return jsonify(errno=RET.DBERR, errmsg="数据查询错误")
    # 如果没有查询到新闻
    if not news:
        return jsonify(errno=RET.NODATA, errmsg="未查询到新闻数据")
    # 取消收藏
    if action == 'cancel_collect':
        if news in user.collection_news:
            user.collection_news.remove(news)
    else:
        # 收藏
        if news not in user.collection_news:
            # 添加到用户的新闻收藏列表
            user.collection_news.append(news)

    return jsonify(errno=RET.OK, errmsg="操作成功")


@news_bul.route('/<int:news_id>')
@user_login_data
def news_detail(news_id):
    """
    新闻详情
    :param news_id:
    :return:
    """
    # 查询登录
    user = g.user
    # 排行榜实现
    news_list = []
    try:
        news_list = News.query.order_by(News.clicks.desc()).limit(constants.CLICK_RANK_MAX_NEWS)
    except Exception as e:
        current_app.logger.error(e)

    news_dict_li = []
    # 遍历对象列表
    for newss in news_list:
        # print(news)
        news_dict_li.append(newss.to_basic_dict())

    # 查询新闻数据
    news = None
    try:
        news = News.query.get(news_id)
    except Exception as e:
        current_app.logger.error(e)
    if not news:
        # 后续处理404错误页面
        abort(404)

    #  更新新闻的点击次数
    news.clicks += 1

    # 是否是收藏
    is_collected = False
    # if 用户已经登录：
    #     判断用户是否收藏当前新闻，如果收藏：
    #         is_collected = Ture

    if user:
        if news in user.collection_news:
            is_collected = True

    comments = []

    # 查询评论数据
    try:
        comments = Comment.query.filter(Comment.news_id == news_id).order_by(Comment.create_time.desc()).all()
    except Exception as e:
        current_app.logger.error(e)
    comment_like_ids = []
    if g.user:
        try:
            # 需求：查询当前用户在当前新闻里面点赞了哪些评论
            # 1，查询出当前新闻的所有评论（【COMMENT】）取到的所有的评论id[1,2,3,4,5]
            comment_ids = [comment.id for comment in comments]
            # 2,查询当前评论中那些评论被当前用户所点赞（【CommentLike】）查询comment_id在第一步的评论id列表内的所有数据
            comment_likes = CommentLike.query.filter(CommentLike.comment_id.in_(comment_ids),
                                                     CommentLike.user_id == g.user.id).all()
            # 3, 取到所有被点赞的评论id，第二步查询出来是一个【CommentLike】--->【3,5】
            comment_like_ids = [comment_like.comment_id for comment_like in comment_likes]
        except Exception as e:
            current_app.logger.error(e)

    # print(comments)
    comment_dict_li = []
    for comment_ in comments:
        comment_dict = comment_.to_dict()
        # 代表没有点赞
        comment_dict["is_like"] = False
        if comment_.id in comment_like_ids:
            comment_dict["is_like"] = True
        comment_dict_li.append(comment_dict)

    is_followed = False
    if news.user and user:
        if news.user in user.followed:
            is_followed = True

    categories = Category.query.all()
    category_li = []
    for category in categories:
        category_li.append(category)
    print(category_li)
    data = {
        "user": user.to_dict() if user else None,
        "news_dict_li": news_dict_li,
        "news": news.to_dict(),
        "is_collected": is_collected,
        "is_followed": is_followed,
        "comments": comment_dict_li,
        "category_li": category_li
    }
    print(data)

    return render_template("news/detail.html",
                           data=data
                           )
