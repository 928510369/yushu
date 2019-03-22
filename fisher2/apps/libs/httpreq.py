import requests,json
from flask import jsonify
class Http:
    @staticmethod
    def get(url,return_json=True):
        response=requests.get(url=url)


        # print(response.content.decode("utf-8"))
        if response.status_code!=200:
            return "" if return_json else {}
        return json.loads(response.text) if return_json else response

