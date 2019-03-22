from flask_login import login_required, current_user
from flask import redirect, url_for, flash, render_template, request
from sqlalchemy import or_, desc

from apps import db
from apps.forms.book import DriftForm
from apps.libs.email import send_mail
from apps.libs.enums import PendingStatus
from apps.models.drift import Drift
from apps.models.gift import Gift
from apps.models.user import User
from apps.models.wish import Wish
from apps.view_models.book import BookViewModel
from apps.view_models.drift import DriftCollection, DriftViewModel
from . import web


__author__ = '七月'


@web.route('/drift/<int:gid>', methods=['GET', 'POST'])
@login_required
def send_drift(gid):

    current_gift=Gift.query.get_or_404(gid)
    res=current_gift.is_yourself_gift(current_user.id)
    if res:
        flash("这是你自己的礼物，不可向自己索要书籍")
        return redirect(url_for("web.book_detail",isbn=current_gift.isbn))

    can=current_user.can_send_drift()
    if not can:
        return render_template("not_enough_beans.html",beans=current_user.beans)
    form_obj = DriftForm(request.form)
    if request.method=="POST" and form_obj.validate():

        save_drift(form_obj,current_gift)
        send_mail(current_gift.user.email, '有人想要一本书', 'email/get_gift',
                   wisher=current_user,
                   gift=current_gift)

        return redirect(url_for("web.pending"))
    gither=current_gift.user.summary
    return render_template("drift.html",gifter=gither,user_beans=current_user.beans,form=form_obj)
@web.route('/pending')
@login_required
def pending():
    drifts=Drift.query.filter(or_(Drift.requester_id==current_user.id,Drift.gifter_id==current_user.id))\
        .order_by(desc(Drift.create_time)).all()
    drift_list=DriftCollection(drifts,current_user.id)
    return render_template("pending.html",drifts=drift_list.data)



@web.route('/drift/<int:did>/reject')
@login_required
def reject_drift(did):
    with db.auto_commit():
        drift = Drift.query.filter(Gift.uid == current_user.id,
                                   Drift.id == did).first_or_404()
        drift.pending = PendingStatus.reject
        requester=User.query.get_or_404(drift.requester_id)
        requester.beans+=1
    return redirect(url_for('web.pending'))


@web.route('/drift/<int:did>/redraw')
@login_required
def redraw_drift(did):
    with db.auto_commit():
        try:
            drift=Drift.query.filter_by(requester_id=current_user.id,id=did).first_or_404()
            drift.pending=PendingStatus.redraw
            current_user.beans+=1
        except Exception as e:
            flash("你已经超权")

    # view_model = DriftViewModel(drifts)
    # return render_template('pending.html', drifts=view_model)
    return redirect(url_for("web.pending"))


@web.route("/drift/<int:did>/mailed")
def mailed_drift(did):
    with db.auto_commit():
        drift=Drift.query.filter_by(gifter_id=current_user.id,id=did).first_or_404()
        drift.pending=PendingStatus.success
        current_user.beans+=1
        gift=Gift.query.filter_by(id=drift.gift_id).first_or_404()
        gift.launched=True

        wish=Wish.query.filter_by(isbn=drift.isbn,uid=drift.requester_id,launched=False)
        wish.launched=True
    return redirect(url_for("web.pending"))
def save_drift(dirft_form,current_gift):
    with db.auto_commit():
        drift=Drift()
        dirft_form.populate_obj(drift)

        drift.gift_id = current_gift.id
        drift.requester_id = current_user.id
        drift.requester_nickname = current_user.nickname
        drift.gifter_nickname = current_gift.user.nickname
        drift.gifter_id = current_gift.user.id
        book=BookViewModel(current_gift.book)
        drift.book_title = book.title
        drift.book_author = book.author
        drift.book_img = book.image
        drift.isbn=book.isbn
        try:
            current_user.beans-=1
        except Exception as e:
            print("鱼豆小于1")
            pass

        db.session.add(drift)
