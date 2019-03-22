from apps.view_models.book import BookViewModel


class TradeInfo:

    def __init__(self,goods):
        self.total=0
        self.trades=[]
        self._parse(goods)

    def _parse(self,goods):
        self.total=len(goods)
        self.trades=[self.map_to_trade(single)  for single in goods ]


    def map_to_trade(self,single):

        if single.create_datatime:
            time = single.create_datatime.strftime('%Y-%m-%d')
        else:
            time="未知"
        return dict(
            user_name=single.user.nickname,
            time=time,
            id=single.id

        )

class Mytrades():
    def __init__(self,trades_of_mine,trades_count_list):
        self.trades=[]
        self.__trades_of_mine=trades_of_mine
        self.__trades_count_list=trades_count_list
        self.trades=self.__parse()

    def __parse(self):
        temp_trades=[]
        for trade_of_mine in self.__trades_of_mine:
            res=self.__matching(trade_of_mine)
            temp_trades.append(res)

        return temp_trades

    def __matching(self,trade):
        count=0
        for trade_count_list in self.__trades_count_list:
            if trade.isbn!=trade_count_list['isbn']:
                pass
            else:
                count=trade_count_list["count"]
                break

        r={
            "trade_count":count,
            "book":BookViewModel(trade.book),
            "id":trade.id

        }

        return r


