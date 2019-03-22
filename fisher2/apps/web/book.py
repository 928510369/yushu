import json

from flask_login import current_user

from apps.models.gift import Gift
from apps.models.wish import Wish
from apps.spider.yushu_book import YuShuBook
from apps.libs.utils import isbn_or_key
from flask import jsonify,request,render_template,flash
from apps.forms import book
from apps.view_models.trade import TradeInfo
from . import web
from apps.view_models.book import BookCollectModel,BookViewModel


@web.route('/test')
def test():
    r1={
        "name":"",
        "age":21,

    }
    flash("aniu")
    return render_template('test.html',data=r1)


@web.app_template_filter("add1")
def add1(li):
    li=li+1
    return li


@web.route("/book/search")
def search():
    #api http://t.yushu.im/v2/book/search?q={}&count={}&start={}
    #api http://t.yushu.im/v2/book/isbn/{isbn}

    form_obj=book.SearchForm(request.args)
    books=BookCollectModel()

    if form_obj.validate():
        q=form_obj.q.data.strip()
        page=form_obj.page.data
        is_isbn_or_key=isbn_or_key(q)
        yushu_book=YuShuBook()


        if is_isbn_or_key=="key":
            yushu_book.search_by_key(q,page)
        else:

            yushu_book.search_by_isbn(q)


        books.fill(yushu_book,q)

        #return json.dumps(books,default=lambda o: o.__dict__)

        # return jsonify(books.__dict__)
    else:
        flash("输入关键字搜索信息失败")

    return render_template("search_result.html",books=books)

@web.route("/book/<isbn>/detail")
def book_detail(isbn):
    has_in_gifts=False
    has_in_wishs=False

    yushubook=YuShuBook()
    yushubook.search_by_isbn(isbn)

    book= BookViewModel(yushubook.first)
    if current_user:
        if Gift.query.filter_by(uid=current_user.id,isbn=isbn).first():
            has_in_gifts=True
        if Wish.query.filter_by(uid=current_user.id,isbn=isbn).first():
            has_in_wishs=True

    trade_gifts=Gift.query.filter_by(isbn=isbn,launched=False).all()
    trade_wishs=Wish.query.filter_by(isbn=isbn,launched=False).all()

    trade_gifts_model=TradeInfo(trade_gifts)
    trade_wishs_model = TradeInfo(trade_wishs)

    return render_template("book_detail.html",book=book,wishes=trade_wishs_model,gifts=trade_gifts_model,\
                           has_in_gifts=has_in_gifts,has_in_wishs=has_in_wishs)