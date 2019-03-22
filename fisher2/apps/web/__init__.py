from flask import Blueprint, render_template

web=Blueprint("web",__name__)


@web.app_errorhandler(404)
def not_found(e):
    return render_template("404.html"),404

from apps.web import book
from apps.web import auth
from apps.web import drift
from apps.web import gift
from apps.web import main
from apps.web import wish

