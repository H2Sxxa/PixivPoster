from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods import posts
class wp_XMLRPC():
    def __init__(self,site:str,account:str,password:str) -> None:
        self.wp = Client(site,account,password)
        self.post = WordPressPost()
    def setArticle(self,title:str="",tag:list=[],content:str="",cate:list=[],state:str="draft") -> None:
        self.post.title=title
        self.post.content = content
        self.post.state = state
        self.post.terms_names = {
            'category': cate,
            'post_tag': tag,
        }
    def postArticle(self):
        self.post.id = self.wp.call(posts.NewPost(self.post))
        return self.post.id