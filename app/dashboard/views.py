from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user

dashboard = Blueprint(name="dashboard", url_prefix="/dashboard", import_name=__name__)


@dashboard.route("/<string:username>")
def user_dashboard(username):
    user = current_user
    return render_template("dashboard/userdashboard.html", user=user)
