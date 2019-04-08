from flask import Blueprint
rent_bul = Blueprint("rent", __name__, url_prefix="/rent")
from . import views


