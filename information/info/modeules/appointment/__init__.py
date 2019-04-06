from flask import Blueprint
appointment_bul = Blueprint("appointment", __name__, url_prefix="/appointment")
from . import views
