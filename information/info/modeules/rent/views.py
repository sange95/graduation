import json
import random
import re
from pprint import pprint

from bson import ObjectId

from info import collection
from info.models import User
from info.untils.common import user_login_data
from info.untils.get_phone import get_phone
from info.untils.json_conversion import JSONEncoder
from ..rent import rent_bul
from flask import render_template, session, current_app, g, request, jsonify, abort


@rent_bul.route("/detail", methods=["get"])
# @user_login_data
def detail():
    """
    详情页
    :return:
    """
    house_id = request.args.get("house_id", None)
    # print(house_id)
    if house_id:
        info = collection.find_one({"_id": ObjectId(house_id)})
        # pprint(info)
        info["phone"] = get_phone()
        info["view_count"] = random.randint(100, 2000)
        # print(info["phone"])
        data = {
            # "user": user,
            "info": info
        }
        return render_template("rent/detail.html", data=data)
    else:
        return render_template('news/404.html')


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
        except Exception as e:
            current_app.logger.error(e)
    user = g.user
    data = collection.find().limit(10)
    data = {
        "user": user,
        "info": data
    }
    # return jsonify(data)
    # print(data)
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
    page = int(request.form.get("curPage", 1))
    skip = int(request.form.get("pageSize", 5))
    # print(page)
    # print(skip)
    # xiaoquname = request.form.get("tiaojian", None)

    # 这下边的都是json
    local = request.form.get("area", None)
    print(dict(request.form))
    chuzufangshi = request.form.get("rentype", None)
    huxing = request.form.get("hometype", None)
    info_list = list()
    print(local)
    # print(type(local))
    if local:
        local = json.loads(local)
    else:
        local = ["金水"]

    print(local)
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
                a_lists = collection.find(
                    {"local": {"$in": local}, "huxing": {"$regex": str}, "chuzufangshi": chuzufangshi}).skip(
                    (page - 1) * skip).limit(skip)
            else:

                str = re.compile((r'.*[5-9]{1}室.*'))
                a_lists = collection.find(
                    {"local": {"$in": local}, "huxing": {"$regex": str}, "chuzufangshi": chuzufangshi}).skip(
                    (page - 1) * skip).limit(skip)
                # a_lists = collection.find({"local":{"$in":local},"huxing": {"$regex":".*?"+huxing+".*?"}, "chuzufangshi": chuzufangshi})

        else:
            a_lists = collection.find({"local": {"$in": local}, "chuzufangshi": chuzufangshi}).skip(
                (page - 1) * skip).limit(skip)

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
                    {"local": {"$in": local}, "huxing": {"$regex": str}}).skip((page - 1) * skip).limit(skip)
            else:
                str = re.compile((r'.*[5-9]{1}室.*'))
                a_lists = collection.find(
                    {"local": {"$in": local}, "huxing": {"$regex": str}}).skip((page - 1) * skip).limit(skip)

        else:
            a_lists = collection.find({"house_area": {"$in": local}}).skip((page - 1) * skip).limit(skip)

        for i in a_lists:
            i["_id"] = JSONEncoder().encode(i["_id"])
            info_list.append(i)
    print(info_list)
    data = {
        # "user": user,
        "info": info_list
    }
    # pprint(data)
    # return jsonify(data)
    return jsonify(data=data)
