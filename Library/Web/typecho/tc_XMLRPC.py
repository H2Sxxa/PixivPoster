from pytypecho import Typecho,Post
class tc_XMLRPC():
    def __init__(self,site:str,account:str,password:str) -> None:
        self.tc=Typecho(site,account,password)
    def setArticle(self,title:str="",tag:list=[],content:str="",cate:list=[],publish:bool=False) -> None:
        self.pubilsh=publish
        self.post=Post(title,content,categories=cate)
    def postArticle(self):
        postid=self.tc.new_post(self.post,self.pubilsh)
        return postid