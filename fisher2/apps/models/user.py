from math import floor

from flask import current_app

from apps.libs.utils import isbn_or_key
from apps.models.base import Base
from sqlalchemy import Column,Integer,String,Boolean,Float
from werkzeug.security import generate_password_hash,check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as TimeSer
from flask_login import UserMixin
from apps import login_manager, db
from apps.models.drift import Drift
from apps.models.gift import Gift
from apps.models.wish import Wish
from apps.spider.yushu_book import YuShuBook
from apps.libs.enums import PendingStatus

class User(UserMixin,Base):
    id = Column(Integer, primary_key=True)
    nickname = Column(String(24), nullable=False)
    phone_number = Column(String(18), unique=True)
    _password=Column("password",String(128),nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    confirmed = Column(Boolean, default=False)
    beans = Column(Float, default=0)
    send_counter = Column(Integer, default=0)
    receive_counter = Column(Integer, default=0)
    wx_open_id=Column(String(50))
    wx_name=Column(String(32))



    @property
    def summary(self):
        return dict(
            nickname=self.nickname,
            beans=self.beans,
            email=self.email,
            send_receive=str(self.send_counter) + '/' + str(self.receive_counter)
        )

    def can_send_drift(self):
        if self.beans<1:
            return False
        success_gift_count=Gift.query.filter_by(launched=True,uid=self.id).count()

        success_receive_count=Drift.query.filter_by(requester_id=self.id,_pending=PendingStatus.success.value).count()

        return True if floor(success_receive_count /2 ) < success_gift_count else False

    @property
    def password(self):
        return self._password


    @password.setter
    def password(self,raw):

        self._password=generate_password_hash(raw)


    def check_password(self,raw):
        return check_password_hash(self._password,raw)

    def can_save_to_list(self, isbn):
        if isbn_or_key(isbn)!= 'isbn':
            return False
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(isbn)
        if not yushu_book.first:
            return False
        gifting = Gift.query.filter_by(uid=self.id, isbn=isbn,
                                       launched=False).first()
        wishing = Wish.query.filter_by(uid=self.id, isbn=isbn,
                                       launched=False).first()
        if not gifting and not wishing:
            return True
        else:
            return False


    def get_tokon(self,expirtion=600):
        serobj=TimeSer(current_app.config["SECRET_KEY"],expirtion)
        temp=serobj.dumps({"id":self.id}).decode("utf-8")
        return temp

    @staticmethod
    def reset_password(token,pwd):
        s=TimeSer(current_app.config["SECRET_KEY"])
        try:
            data=s.loads(token.encode("utf-8"))
        except Exception:
            return False
        uid=data.get("id")
        with db.auto_commit():
            user=User.query.get(uid)
            if user:
                user.password=pwd
                return True
            else:
                return False

@login_manager.user_loader
def get_user(uid):
    return User.query.get(int(uid))