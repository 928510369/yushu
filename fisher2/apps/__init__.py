from flask import Flask,current_app
from flask_mail import Mail

from apps.models.base import db


from flask_login import LoginManager
# from apps.models.test import Test

login_manager=LoginManager()
mail=Mail()

def create_app():


    #static_folder="statics"
    app = Flask(__name__,)

    app.config.from_object("apps.secure")
    app.config.from_object("apps.settings")

    register_blueprint(app)
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view="web.login"
    login_manager.login_message="请先登陆或注册"
    with app.app_context():
        db.create_all()
    return app

def register_blueprint(my_app):
    from apps.web import web

    my_app.register_blueprint(web)
