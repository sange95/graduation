from flask import Blueprint, session, request, redirect, url_for

# 创建蓝图
admin_blu = Blueprint("admin", __name__)
from . import views


@admin_blu.before_request
def check_admin():
    is_admin = session.get("is_admin", False)
    if not is_admin and not request.url.endswith(url_for("admin.login")):
        return redirect("/")