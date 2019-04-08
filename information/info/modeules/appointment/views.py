from ..appointment import appointment_bul
from flask import render_template


@appointment_bul.route("/index", methods=["get"])
def index():
    data = "ccc"
    return render_template("appointment/index.html", data=data)


@appointment_bul.route("/detail", methods=["get"])
def detail():
    print("这是预约的详情页")
    data = "ccc"
    return render_template("appointment/detail.html", data=data)
