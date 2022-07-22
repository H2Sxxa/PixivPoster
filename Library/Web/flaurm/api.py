from requests import post
from json import loads,dumps
class Flaurm():
    def __init__(self,account:str,password:str,url:str) -> None:
        _identify={
            "identification":account,
            "password":password
        }
        identify=loads(post(url+"/api/token",data=_identify).text)
        self.token=identify["token"]
        self.id=identify["userId"]
        self.url=url
        self._header={
            "Authorization":"Token " + self.token+"; userId=%s" % self.id
        }
    def postArticle(self) -> None:
        _data={"data":{"type": "discussions","attributes": {"title": "API test","content": "Hello World"},"relationships":{"tags": {"data": [{"type": "tags","id": "1"}]}}}}
        resp=post(self.url+"/api/discussions",headers=self._header,data=_data)
        print(loads(resp.text))