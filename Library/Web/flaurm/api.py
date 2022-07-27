from requests import post,get,patch,packages
from json import dumps, loads
class Flarum():
    def __init__(self,account:str=None,password:str=None,url:str=None) -> None:
        '''
        Example\n
        account: flarum\n
        password: 123456789\n
        url: https://127.0.0.1
        '''
        packages.urllib3.disable_warnings()
        self.Verify=True
        if url == None:
            raise ValueError("A none url")
        if account == None and password == None:
            self._header=None
        else:
            _identify={
                "identification":account,
                "password":password
            }
            self.url=url
            identify=loads(post(url+"/api/token",data=_identify,verify=self.Verify).text)
            self._header={
                "Authorization":"Token %s;userId=%s" % (identify["token"],identify["userId"])
                }
    def getHeader(self):
        return self._header
    #tag
    def get2Tags(self) -> dict:
        '''
        return a dict like {tagid:name,tagid2:name2...}
        '''
        resp=get(self.url+"/api/tags",headers=self._header,verify=self.Verify)
        raw=loads(resp.text)
        result={}
        for tag in raw["data"]:
            result.update({tag["id"]:tag['attributes']["name"]})
        return result
    
    def getTags(self) -> dict:
        '''
        return all tag infomation
        '''
        resp=get(self.url+"/api/tags",headers=self._header,verify=self.Verify)
        return loads(resp.text)
    
    
    #article(discussions)
    def postArticle(self,title:str,content:str,tag_id:str) -> dict:
        '''
        return all infomation of the new article
        '''
        _json={"data":{"type": "discussions","attributes": {"title": title,"content": content},"relationships":{"tags": {"data": [{"type": "tags","id": tag_id}]}}}}
        resp=post(self.url+"/api/discussions",headers=self._header,json=_json,verify=self.Verify)
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
    #posts
    def editPosts(self,post_id:str,content:str) -> dict:
        '''
        return all information of the new posts
        '''
        _json={"data": {"type": "posts","attributes": {"content": content},"id": post_id}}
        resp=post("%s/api/posts/%s"%(self.url,post_id),headers=self._header,json=_json,verify=self.Verify)
        return loads(resp.text)
    
    def postPosts(self,article_id:str="",content:str="") -> dict:
        _json={"data":{"type":"posts","attributes":{"content":content},"relationships":{"discussion":{"data":{"type":"discussions","id":article_id}}}}}
        resp=post(self.url+"/api/posts",headers=self._header,json=_json,verify=self.Verify)
        return loads(resp.text)
    def getPosts(self,post_id:str):
        resp=get("%s/api/posts/%s" % (self.url,post_id),headers=self._header,verify=self.Verify)
        return loads(resp.text)
    #users
    def createUser(self,username:str,email:str,password:str) -> dict:
        '''
        return all infomation of the new user
        '''
        _json={"data":{"attributes":{"username":username,"email":email,"password":password}}}
        resp=post(self.url+"/api/users",headers=self._header,json=_json,verify=self.Verify)
        return loads(resp.text)
    
    def getUser(self,user_id:str="") -> dict:
        '''
        return all infomation of the user
        '''
        if user_id == "":
            resp=get("%s/api/users" % (self.url),headers=self.header,verify=self.Verify)
        else:
            resp=get("%s/api/users/%s" % (self.url,user_id),headers=self.header,verify=self.Verify)
        return loads(resp.text)