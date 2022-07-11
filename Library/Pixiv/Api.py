import json
from requests import get
from .time import getdate
def pixiv(date=None):
    if date == None:
        adate="date="+getdate()
    else:
        adate="date="+date
    api=r"https://api.acgmx.com/public/ranking?ranking_type=illust&mode=daily&per_page=50&page=1&"+adate
    #print(api)
    #illustidlist,titlelist,pagecount,tagslist,userlist=getinfo(api)
    return getinfo(api)
def getinfo(api):
    try:
        apitext=get(api).text
    except:
        return [],[],[],[],[]
    if apitext == "{\"illusts\":[],\"next_url\":null}":
        return [],[],[],[],[]
    if apitext == "{\"code\":500,\"msg\":\"请求失败\"}" or apitext=="获取失败":
        return [],[],[],[],[]
    try:
        return json.loads(apitext)
    except:
        return None

