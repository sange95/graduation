from ..rent import rent_bul
from flask import render_template


@rent_bul.route("/index", methods=["get"])
def index():
    print("ccccccccccccc")
    data = "ccc"
    return render_template("rent/index.html", data=data)


@rent_bul.route("/detail", methods=["get"])
def detail():
    print("这是租房的详情页")
    data = "ccc"
    return render_template("rent/detail.html", data=data)
