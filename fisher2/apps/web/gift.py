from flask import current_app, flash, redirect, url_for, render_template
from flask_login import login_required, current_user
from sqlalchemy import desc

from apps import db
from apps.libs.enums import PendingStatus
from apps.models.drift import Drift
from apps.models.gift import Gift
# from apps.view_models.gift import Mygifts
from apps.models.wish import Wish
from apps.view_models.trade import Mytrades
from . import web


__author__ = '七月'


@web.route('/my/gifts')
@login_required
def my_gifts():
    uid=current_user.id
    book_lists=Gift.query.filter_by(uid=uid,launched=False).order_by(desc(Gift.create_time)).all()
    wishs_count=Wish().get_count_list(book_lists)
    gifts_view_model=Mytrades(book_lists,wishs_count)
    return render_template("my_gifts.html",gifts=gifts_view_model.trades)

@web.route('/gifts/book/<isbn>')
@login_required
def save_to_gifts(isbn):
   if current_user.can_save_to_list(isbn):

       # try:
       #     gift=Gift()
       #     gift.uid=current_user.id
       #     gift.isbn=isbn
       #     current_user.beans+=current_app.config["BEANS_UPLOAD_TO_BOOK"]
       #     db.session.add(gift)
       #     db.session.commit()
       #
       # except Exception as e:
       #     db.session.rollback()
       #     raise e
        with db.auto_commit():
            gift = Gift()
            gift.uid = current_user.id
            gift.isbn = isbn
            current_user.beans += current_app.config["BEANS_UPLOAD_TO_BOOK"]
            db.session.add(gift)
   else:
        flash("这本书已经添加到你的赠送清单或已存在与你的心愿清单，请不要重复添加")

   return redirect( url_for("web.book_detail",isbn=isbn))


@web.route('/gifts/<gid>/redraw')
def redraw_from_gifts(gid):
    gift=Gift.query.filter_by(id=gid,launched=False).first_or_404()
    drift=Drift.query.filter_by(gift_id=gid,pending=PendingStatus.waiting).first_or_404()
    if drift:
        flash("交易正在进行中，请先前往处理")
    else:
        with db.auto_commit():
            gift.delete()

    return redirect(url_for("web.my_gifts"))

