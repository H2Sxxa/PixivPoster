from . import Api
from . import tool
from pixivpy_async.sync import *

class Direct():
    def __init__(self,**kwargs) -> None:
        '''
        sock(str):support sock5/4 and http\n
        sni(bool):Pass the SNI\n
        refresh_token(str):
        '''
        if kwargs.__contains__("refresh_token"):
            self.token=kwargs["refresh_token"]
            self.hastoken=True
        else:
            self.hastoken=False
        if kwargs.__contains__("sock"):
            self.sock=kwargs["sock"]
            self.hassock=True
        else:
            self.hassock=False
        
        if kwargs.__contains__("sni"):
            if kwargs["sni"] == True:
                self.sni=True
            else:
                self.sni=False
        else:
            self.sni=False
        self.initAppPixivAPI()
    def initAppPixivAPI(self):
        if self.hassock and self.sni:
            aapi = AppPixivAPI(proxy=self.sock,bypass=True)
        elif self.hassock and not self.sni:
            aapi = AppPixivAPI(proxy=self.sock)
        elif not self.hassock and self.sni:
            aapi = AppPixivAPI(bypass=True)
        else:
            aapi = AppPixivAPI()
        self.aapi=aapi
    def login(self):
        '''
        set refresh_token(auth['refresh_token']) in init,or you must manual login
        '''
        if self.hastoken:
            try:
                auth=self.aapi.login(refresh_token=self.token)
            except Exception as e:
                print(str(e))
                print("If all failed , you should reload it")
        else:
            auth=self.aapi.login_web()
            return auth
    def getRank(self,mode:str='day'):
        try:
            rank=self.aapi.illust_ranking(mode)
            return rank
        except Exception as e:
            print(str(e))
            print("failed,may be the refresh_token has expired,it has turned to api")
            return Api.pixiv()
    def sortRank(self,jsondict):
        illustidlist,titlelist,pagecount,tagslist,userlist=[],[],[],[],[]
        for i in jsondict["illusts"]:
            illustidlist.append(i["id"])
            titlelist.append(i["title"])
            pagecount.append(i["page_count"])
            tagslist.append(i["tags"])
            userlist.append(i["user"])
        return illustidlist,titlelist,pagecount,tagslist,userlist
    def sort2Rank(self,pagecount,illustidlist,titlelist,address:str="pixiv.re"):
        return tool.mk_list(pagecount,illustidlist,titlelist,address)
    def sortillustlink(self,illustidlist,illusturllist):
        alllist=[]
        onelist=[]
        for iid in illustidlist:
            iid=str(iid)
            for illusturl in illusturllist:
                if iid in illusturl:
                    onelist.append(illusturl)
            alllist.append(onelist)
            onelist=[]
        return alllist
    def extarctSort(self,adict:dict,key:str) -> list:
        finlist=[]
        for i in adict:
            finlist.append(i[key])
        return finlist