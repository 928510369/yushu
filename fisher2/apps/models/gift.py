from flask import current_app

from apps import db
from apps.models.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey, desc, func, text, SmallInteger, distinct, Boolean
from sqlalchemy.orm import relationship


from apps.spider.yushu_book import YuShuBook


class Gift(Base):
    id = Column(Integer, primary_key=True)
    user = relationship('User')
    uid=Column(Integer,ForeignKey("user.id"))
    isbn = Column(String(20), nullable=False,)
    # book = relationship('Book')
    # bid = Column(Integer, ForeignKey("book.id"))
    launched =Column(Boolean,default=False)


    @classmethod
    def recent(cls):#order_by(cls.create_datatime).\.group_by(Gift.isbn)
        recent_gifts=cls.query.filter_by(launched=False).group_by(Gift.isbn).\
            order_by(desc(cls.create_time)).limit(current_app.config["RECENT_BOOK_COUNT"]).distinct()\
            .all()

        return recent_gifts


    @property
    def book(self):
        yushubook=YuShuBook()
        yushubook.search_by_isbn(self.isbn)
        return yushubook.first


    def get_count_list(self,book_list):
        from apps.models.wish import Wish
        isbn_list=[book.isbn for book in book_list]

        # count_list=db.session.query(func.count(distinct(Wish.uid)),Wish.isbn).filter(Wish.launched==False,
        #                                                                   Wish.status == 1,
        #                                                                   Wish.isbn.in_(isbn_list),
        #                                                                   ).group_by(Wish.isbn)\
        #                                                                   .all()
        count_list = db.session.query(func.count(distinct(Gift.uid)), Gift.isbn).filter(Gift.launched == False,
                                                                                        Gift.status == 1,
                                                                                        Gift.isbn.in_(isbn_list),
                                                                                        ).group_by(Gift.isbn) \
            .all()

        count_list=[{"count":w[0],"isbn":w[1]} for w in count_list]

        return count_list


    def is_yourself_gift(self,id):

        return True if self.uid==id else False

    def delete(self):
        self.status=0