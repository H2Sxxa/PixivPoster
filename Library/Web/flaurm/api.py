from requests import post,get,patch
from json import loads
class Flarum():
    def __init__(self,account:str=None,password:str=None,url:str=None) -> None:
        '''
        Example\n
        account: flarum\n
        password: 123456789\n
        url: https://127.0.0.1
        '''
        if url == None:
            raise ValueError("A none url")
        if account == None and password == None:
            self.header=None
        else:
            _identify={
                "identification":account,
                "password":password
            }
            self.url=url
            identify=loads(post(url+"/api/token",data=_identify).text)
            self._header={
                "Authorization":"Token %s;userId=%s" % (identify["token"],identify["userId"])
                }
    #tag
    def get2Tags(self) -> dict:
        '''
        return a dict like {tagid:name,tagid2:name2...}
        '''
        resp=get(self.url+"/api/tags",headers=self._header)
        raw=loads(resp.text)
        result={}
        for tag in raw["data"]:
            result.update({tag["id"]:tag['attributes']["name"]})
        return result
    def getTags(self) -> dict:
        '''
        return all tag infomation
        '''
        resp=get(self.url+"/api/tags",headers=self._header)
        return loads(resp.text)
    #article(discussions)
    def postArticle(self,title:str,content:str,tagid:str) -> dict:
        '''
        return all infomation of the new article
        '''
        _json={"data":{"type": "discussions","attributes": {"title": title,"content": content},"relationships":{"tags": {"data": [{"type": "tags","id": tagid}]}}}}
        resp=post(self.url+"/api/discussions",headers=self._header,json=_json)
        return loads(resp.text)
    
    def getArticle(self,article_id:str="") -> dict:
        '''
        return all infomation of the article
        '''
        if article_id == "":
            resp=get("%s/api/discussions" % (self.url),headers=self.header)
        else:
            resp=get("%s/api/discussions/%s" % (self.url,article_id),headers=self.header)
        return loads(resp.text)
    
    def patchArticle(self,article_id:str="") -> dict:
        pass
    #users
    def createUser(self,username:str,email:str,password:str) -> dict:
        '''
        return all infomation of the new user
        '''
        _json={"data":{"attributes":{"username":username,"email":email,"password":password}}}
        resp=post(self.url+"/api/users",headers=self._header,json=_json)
        return loads(resp.text)
    
    def getUser(self,user_id:str="") -> dict:
        '''
        return all infomation of the user
        '''
        if user_id == "":
            resp=get("%s/api/users" % (self.url),headers=self.header)
        else:
            resp=get("%s/api/users/%s" % (self.url,user_id),headers=self.header)
        return loads(resp.text)