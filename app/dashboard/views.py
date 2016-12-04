from flask import Blueprint, render_template, redirect, url_for

dashboard = Blueprint(name="dashboard", url_prefix="dashboard/", import_name=__name__)


@dashboard.route("<string:username>")
def dashboard(username):

    return render_template("dashboard/userdashboard.html")
