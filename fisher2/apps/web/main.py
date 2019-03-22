from flask import render_template

from apps import db
from apps.models.gift import Gift
from apps.models.wish import Wish
from apps.view_models.book import BookViewModel
from . import web


__author__ = '七月'


# def __current_user_status_change():
#     r = request


@web.route('/')
def index():

    recent_gifts=Gift.recent()
    books=[BookViewModel(gift.book) for gift in recent_gifts]

    return render_template("index.html",recent=books)



@web.route('/personal')
def personal_center():
    pass



# @web.route('/testsql')
# def testsql():
#     with db.auto_commit():
#
#         wish=Wish()
#         wish.uid=2
#         wish.launched=True
#         wish.isbn="9787535438171"
#         db.session.add(wish)
#
#     return "ok"


