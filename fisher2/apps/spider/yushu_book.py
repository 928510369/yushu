from flask import current_app
from apps.libs.httpreq import Http
from apps.models.base import db
from apps.models.book import Book
class YuShuBook(object):

    # api http://t.yushu.im/v2/book/search?q={}&start={}&count={}
    # api http://t.yushu.im/v2/book/isbn/{isbn}
    isbn_url='http://t.yushu.im/v2/book/isbn/{isbn}'
    key_url="http://t.yushu.im/v2/book/search?q={}&count={}&start={}"

    def __init__(self):
        self.total=0
        self.books=[]

    def __fill_single(self,data):
        self.total=1
        self.books.append(data)

    def __fill_collection(self,data):
        self.total=data["total"]
        self.books=data["books"]


    def search_by_key(self,keywords,page):
        url = self.key_url.format(keywords,current_app.config["PER_PAGE"],self.get_pagecount(page))
        result = Http.get(url)

        self.__fill_collection(result)


    def search_by_isbn(self,isbn):

        url=self.isbn_url.format(isbn=isbn)

        if Book.query.filter_by(isbn=isbn).first():
            print("mysql exist")

        result=Http.get(url)

        self.__fill_single(result)



    def get_pagecount(self,page):
        count=(page-1)*current_app.config["PER_PAGE"]
        return count

    @property
    def first(self):
        return self.books[0] if self.total>0 else None