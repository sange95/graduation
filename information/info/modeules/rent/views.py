import json
import re
from pprint import pprint

from info import collection
from info.models import User
from info.untils.common import user_login_data
from ..rent import rent_bul
from flask import render_template, session, current_app, g, request, jsonify, abort


@rent_bul.route("/detail", methods=["get"])
@user_login_data
def detail():
    # print("ccccccccccccc")
    # data = "ccc"
    """
    详情页
    :return:
    """
    house_id = request.args.get("house_id",None)
    print(house_id)
    # house_id = json.loads(house_id)
    # print(house_id)
    user_id = session.get('user_id', None)

    user = None
    if user_id:
        try:
            user = User.query.get(user_id)
            # print(user)
        except Exception as e:
            current_app.logger.error(e)
    user = g.user
    if house_id:
        info = collection.find_one({"_id": house_id})
        print(info)
        data = {
            "user": user,
            "info": info
        }
        return render_template("rent/detail.html", data=data)
    else:
        data={
            "user": user
        }
        return render_template('news/404.html', data=data)


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
    # local = request.args.get("local", None)
    # if local:
    #     data = collection.find({"local": local})
    # else:
    data = collection.find()
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
        "user": user,
        "info": a_list
    }
    # return jsonify(data)
    # print(data)
    print(len(data["info"]))
    return render_template("rent/index.html", data=data)


@rent_bul.route("/sort", methods=["POST"])
# @user_login_data
def sort():
    # print("ccccccccccccc")
    # data = "ccc"
    """
    按照条件查询
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
    # 这个字符串
    # 字符串
    page = request.form.get("page", 1)
    xiaoquname = request.form.get("tiaojian", None)
    # print(json.loads(xiaoquname))
    # 这下边的都是json
    local = request.form.get("area", None)
    # print(json.loads(local))
    # money = request.form.get("price", "")
    # 合租 用json.loads()转换
    chuzufangshi = request.form.get("rentype", None)
    # 两室
    huxing = request.form.get("hometype", None)

    # print(huxing)
    info_list = list()
    if local:
        local = json.loads(local)
    else:
        local = ["金水区"]
    if chuzufangshi:
        chuzufangshi = json.loads(chuzufangshi)[0]
        # print(chuzufangshi)
        # print(local)
        if huxing:
            huxing = json.loads(huxing)[0]
            if huxing == '一室':
                huxing = '1室'
            elif huxing == '二室':
                huxing = '2室'
            elif huxing == '三室':
                huxing = '3室'
            elif huxing == '四室':
                huxing = '4室'
            else:
                huxing = '10室'
            if huxing != '10室':
                r = ".*{}.*".format(huxing)
                # print(r)
                str = re.compile(r)
                # print(str)
                # str = re.compile(".*3室.*")
                # print(str)
                a_lists = collection.find({"local": {"$in": local}, "huxing": {"$regex": str}, "chuzufangshi": chuzufangshi}).skip((page-1)*5).limit(5)
            else:

                str = re.compile( (r'.*[5-9]{1}室.*'))
                a_lists = collection.find({"local": {"$in": local}, "huxing": {"$regex": str}, "chuzufangshi": chuzufangshi}).skip((page-1)*5).limit(5)
            # a_lists = collection.find({"local":{"$in":local},"huxing": {"$regex":".*?"+huxing+".*?"}, "chuzufangshi": chuzufangshi})

        else:
            a_lists = collection.find({"local":{"$in": local}, "chuzufangshi": chuzufangshi}).skip((page-1)*5).limit(5)

        for i in a_lists:
            info_list.append(i)
    else:
       if huxing:
           huxing = json.loads(huxing)[0]
           print(huxing)
           if huxing == '一室':
               huxing = '1室'
           elif huxing == '二室':
               huxing = '2室'
           elif huxing == '三室':
               # print(111)
               huxing = '3室'
           elif huxing == '四室':
               huxing = '4室'
           else:
               huxing = '10室'
           if huxing != '10室':
               # print(huxing)
               r = ".*{}.*".format(huxing)
               # print(r)
               str = re.compile(r)
               # print(str)
               # str = re.compile(".*3室.*")
               # print(str)
               a_lists = collection.find(
                   {"local": {"$in": local}, "huxing": {"$regex": str}}).skip((page-1)*5).limit(5)
           else:
               str = re.compile((r'.*[5-9]{1}室.*'))
               a_lists = collection.find(
                   {"local": {"$in": local}, "huxing": {"$regex": str}}).skip((page-1)*5).limit(5)

       else:
           a_lists = collection.find({"local": {"$in": local}}).skip((page-1)*5).limit(5)

       for i in a_lists:
           info_list.append(i)

    data = {
        # "user": user,
        "info": info_list
    }
     # return jsonify(data)
    return jsonify(data=data)
