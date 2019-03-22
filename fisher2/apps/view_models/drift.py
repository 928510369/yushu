from apps.libs.enums import PendingStatus


class DriftCollection():
    def __init__(self,drifts,user_id):
        self.data=[]

        self.__parse(drifts,user_id)

    def __parse(self,drifts,user_id):
        for drift in drifts:
            temp=DriftViewModel(drift,user_id)
            self.data.append(temp.data)




class DriftViewModel():
    def __init__(self,drift,user_id):
        self.data={}

        self.data=self.__parse(drift,user_id)

    def _request_or_gifts(self,drift,user_id):

        if user_id==drift.requester_id:
            you_are="requester"
        else:
            you_are="gifter"

        return you_are

    def __parse(self,drift,user_id):
        you_are=self._request_or_gifts(drift,user_id)
        pending_str_value=PendingStatus.pending_str(drift.pending,you_are)
        r={
            'drift_id': drift.id,
            'you_are': you_are,
            'book_title': drift.book_title,
            'book_author': drift.book_author,
            'book_img': drift.book_img,
            'operator': drift.requester_nickname if you_are != 'requester' \
                else drift.gifter_nickname,
            'date': drift.create_datatime.strftime('%Y-%m-%d'),
            'message': drift.message,
            'address': drift.address,
            'recipient_name': drift.recipient_name,
            'mobile': drift.mobile,
            'status': drift._pending,
            "status_str":pending_str_value
        }

        return r

