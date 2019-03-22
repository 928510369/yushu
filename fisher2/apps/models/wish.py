

from apps import db
from apps.models.base import Base
from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, text, SmallInteger, distinct, func
from sqlalchemy.orm import relationship

from apps.spider.yushu_book import YuShuBook


class Wish(Base):
    id = Column(Integer, primary_key=True)
    user = relationship('User')
    uid=Column(Integer,ForeignKey("user.id"))
    isbn = Column(String(20), nullable=False,)
    # book = relationship('Book')
    # bid = Column(Integer, ForeignKey("book.id"))
    launched =Column(Boolean,default=False)

    @property
    def book(self):
        yushubook = YuShuBook()
        yushubook.search_by_isbn(self.isbn)
        return yushubook.first

    def get_count_list(self,book_list):
        from apps.models.gift import Gift
        isbn_list=[book.isbn for book in book_list]

        # count_list=db.session.query(func.count(distinct(Gift.uid)),Gift.isbn).filter(Gift.launched==False,
        #                                                                   Gift.status == 1,
        #                                                                   Gift.isbn.in_(isbn_list),
        #                                                                   ).group_by(Gift.isbn)\
        #                                                                   .all()
        count_list = db.session.query(func.count(distinct(Wish.uid)), Wish.isbn).filter(Wish.launched == False,
                                                                                        Wish.status == 1,
                                                                                        Wish.isbn.in_(isbn_list),
                                                                                        ).group_by(Wish.isbn) \
            .all()

        count_list=[{"count":w[0],"isbn":w[1]} for w in count_list]

        return count_list

    def delete(self):
        self.status=0