from requests import post,get
from json import loads
class Flarum():
    def __init__(self,account:str,password:str,url:str) -> None:
        _identify={
            "identification":account,
            "password":password
        }
        self.url=url
        identify=loads(post(url+"/api/token",data=_identify).text)
        self.token=identify["token"]
        self.id=identify["userId"]
        self._header={
            "Authorization":"Token %s;userId=%s" % (self.token,self.id)
            }
    def getTags(self) -> dict:
        resp=get(self.url+"/api/tags",headers=self._header)
        raw=loads(resp.text)
        result={}
        for tag in raw["data"]:
            result.update({tag["id"]:tag['attributes']["name"]})
        return result
    
    def postArticle(self,title:str,content:str,tagid:str) -> None:
        _json={"data":{"type": "discussions","attributes": {"title": title,"content": content},"relationships":{"tags": {"data": [{"type": "tags","id": tagid}]}}}}
        resp=post(self.url+"/api/discussions",headers=self._header,json=_json)
        return loads(resp.text)