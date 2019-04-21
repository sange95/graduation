import json
from pprint import pprint

from info import collection
from info.models import User
from info.untils.common import user_login_data
from ..rent import rent_bul
from flask import render_template, session, current_app, g, request, jsonify


@rent_bul.route("/detail", methods=["get"])
@user_login_data
def detail():
    # print("ccccccccccccc")
    # data = "ccc"
    """
    详情页
    :return:
    """
    user_id = session.get('user_id', None)
    user = None
    if user_id:
        try:
            user = User.query.get(user_id)
            # print(user)
        except Exception as e:
            current_app.logger.error(e)
    user = g.user
    house_id = request.args.get("house_id", None)
    print(house_id)
    info = collection.find_one({"_id": int(house_id)})
    # for info in data:
    #     data = info
    # print(data)
    # return jsonify(data)
    data = {
        "user": user,
        "info": info
    }
    return render_template("rent/detail.html", data=data)


@rent_bul.route("/index", methods=["get"])
@user_login_data
def index():
    # print("ccccccccccccc")
    # data = "ccc"
    """
    将数据库中的数据所有查询出来,返回前端
    :return:
    """
    user_id = session.get('user_id', None)
    user = None
    if user_id:
        try:
            user = User.query.get(user_id)
            # print(user)
        except Exception as e:
            current_app.logger.error(e)
    user = g.user
    local = request.args.get("local", None)
    if local:
        data = collection.find({"local": local})
    else:
        data = collection.find()
    j = 1
    # print(5555)
    # 放置所有的房子信息
    a_list = list()
    for i in data:
        j += 1
        pprint(i)
        a_list.append(i)

        if j == 6:
            break
    # print(a_list)
    data = {
        "user": user,
        "info": a_list
    }
    # return jsonify(data)
    return render_template("rent/index.html", data=data)


@rent_bul.route("/sort", methods=["POST"])
# @user_login_data
def sort():
    print("ccccccccccccc")
    # data = "ccc"
    """
    将数据库中的数据所有查询出来,返回前端
    :return:
    """
    # user_id = session.get('user_id', None)
    # user = None
    # if user_id:
    #     try:
    #         user = User.query.get(user_id)
    #         # print(user)
    #     except Exception as e:
    #         current_app.logger.error(e)
    # user = g.user
    # local = request.args.get("local", None)
    # if local:
    #     data = collection.find({"local": local})
    # else:
    local = request.args.get("local", None)
    print(local)
    print(type(local))
    if local:

        data = collection.find({"local": local})
        j = 1
        # print(5555)
        # 放置所有的房子信息
        a_list = list()
        for i in data:
            j += 1
            # pprint(i)
            a_list.append(i)

            if j == 6:
                break
        # print(a_list)
        data = {
            # "user": user,
            "info": a_list
        }
        # return jsonify(data)
        return jsonify(data=data)
    else:
        abort(404)
#
# @rent_bul.route("/detail", methods=["get"])
# def detail():
#     print("这是租房的详情页")
#     data = "ccc"
#     return render_template("rent/detail.html", data=data)

# @rent_bul.route("/detail", methods=["get"])
# @user_login_data
# def detail():
#     user_id = session.get('user_id', None)
#     user = None
#     if user_id:
#         try:
#             user = User.query.get(user_id)
#             # print(user)
#         except Exception as e:
#             current_app.logger.error(e)
#     user = g.user
#     data = {
#         "user": user,
#     }
#     return render_template('rent/detail.html', data=data)
