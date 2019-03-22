from apps.view_models.book import BookViewModel


class Mygifts():
    def __init__(self,ming_of_gifts,gifts_wishs):
        self.gifts=[]
        self.mine_of_gifts=ming_of_gifts
        self.gifts_wishs=gifts_wishs
        self.gifts=self.__parse()

    def __parse(self):
        temp_gifts=[]
        for gift in self.mine_of_gifts:
            res=self.__matching(gift)
            temp_gifts.append(res)

        return temp_gifts

    def __matching(self,gift):
        count=0
        for gift_wishs in self.gifts_wishs:
            if gift.isbn!=gift_wishs['isbn']:
                pass
            else:
                count=gift_wishs["count"]
                break

        r={
            "wishes_count":count,
            "book":BookViewModel(gift.book),
            "id":gift.id

        }

        return r

