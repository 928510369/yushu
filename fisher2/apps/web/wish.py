from flask import current_app, flash, redirect, url_for, render_template
from flask_login import current_user
from sqlalchemy import desc

from apps import db
from apps.libs.email import send_mail
from apps.libs.enums import PendingStatus
from apps.models.drift import Drift
from apps.models.gift import Gift
from apps.models.wish import Wish
from apps.view_models.trade import Mytrades
# from apps.view_models.wish import Mywishs
from . import web

__author__ = '七月'


def limit_key_prefix():
    pass


@web.route('/my/wish')
def my_wish():
    uid = current_user.id
    book_lists = Wish.query.filter_by(uid=uid,launched=False).order_by(desc(Wish.create_time)).all()
    gifts_count = Gift().get_count_list(book_lists)
    wishs_view_model = Mytrades(book_lists, gifts_count)
    return render_template("my_wish.html", wishes=wishs_view_model.trades)



@web.route('/wish/book/<isbn>')
def save_to_wish(isbn):
    if current_user.can_save_to_list(isbn):


        with db.auto_commit():
            wish = Wish()
            wish.uid = current_user.id
            wish.isbn = isbn
            db.session.add(wish)
    else:
        flash("这本书已经添加到你的赠送清单或已存在与你的心愿清单，请不要重复添加")

    return redirect(url_for("web.book_detail", isbn=isbn))


@web.route('/satisfy/wish/<int:wid>')
def satisfy_wish(wid):
    wish = Wish.query.get_or_404(wid)
    gift = Gift.query.filter_by(uid=current_user.id, isbn=wish.isbn).first()
    if not gift:
        flash('你还没有上传此书，请点击“加入到赠送清单”添加此书。添加前，请确保自己可以赠送此书')
    else:
        send_mail(wish.user.email, '有人想送你一本书', 'email/satisify_wish', wish=wish,
                   gift=gift)
        flash('已向他/她发送了一封邮件，如果他/她愿意接受你的赠送，你将收到一个鱼漂')
    return redirect(url_for('web.book_detail', isbn=wish.isbn))



@web.route('/wish/book/<isbn>/redraw')
def redraw_from_wish(isbn):
    wish=Wish.query.filter_by(isbn=isbn,launched=False).first_or_404()
    drift = Drift.query.filter_by(requester=current_user.id,isbn=isbn,pending=PendingStatus.waiting).first_or_404()
    if drift:
        flash("请先去书记交易页面去撤销书籍")
    else:
        with db.auto_commit():
            wish.delete()

    return redirect(url_for("web.my_wish"))

