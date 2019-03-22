
class BookViewModel:

    def __init__(self,data):
        self.title=data["title"]
        self.publisher=data["publisher"]
        self.pages=data["pages"] or ""
        self.author=",".join(data["author"])
        self.price=data["price"]
        self.summary=data["summary"] or ""
        self.image=data["image"]
        self.isbn = data["isbn"]
        self.pubdate=data["pubdate"]
        # print(data)
        self.binding=data["binding"]

    @property
    def intro(self):
        intros=filter(lambda x: True if x  else False,[self.author,self.publisher,self.price])

        return "/".join(intros)



class BookCollectModel:
    def __init__(self):
        self.total=""
        self.keywords=None
        self.books=[]
    def fill(self,data,q):
        # print("data",data)
        self.total = data.total
        self.keywords = q
        self.books = [BookViewModel(book) for book in data.books]







class _BookViewModel:
    @classmethod
    def package_single(cls,data,keywords):
        result={
            "books":[],
            'total':0,
            "keywords":keywords,
        }
        if data:
            result["total"]=1
            result["books"]=[cls._cut_book_data(data),]

        return result

    @classmethod
    def package_collection(cls,data,keywords):
        result={
            "books":[],
            'total':0,
            "keywords":keywords,
        }
        if data:
            result["total"]=data["total"]
            result["books"]=[cls._cut_book_data(book) for book in data["books"]  ]
        return result

    @classmethod
    def _cut_book_data(cls,data):
        book={
            "title":data["title"],
            "publisher":data["publisher"],
            "pages":data["pages"] or "",
            "author":",".join(data["author"]),
            "price":data["price"],
            "summary":data["summary"] or "",
            "image":data["image"]


        }

        return book