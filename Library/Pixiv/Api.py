import json
from requests import get
from .time import getdate
def pixiv(date):
    if date == None:
        adate="date="+getdate()
    else:
        adate="date="+date
    api=r"https://api.acgmx.com/public/ranking?ranking_type=illust&mode=daily&per_page=50&page=1&"+adate
    #print(api)
    illustidlist,titlelist,pagecount,tagslist,userlist=getinfo(api)
    return illustidlist,titlelist,pagecount,tagslist,userlist
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
        rawjson=json.loads(apitext)
    except:
        return [],[],[],[],[]
    illustidlist,titlelist,pagecount,tagslist,userlist=[],[],[],[],[]
    for i in rawjson["illusts"]:
        illustidlist.append(i["id"])
        titlelist.append(i["title"])
        pagecount.append(i["page_count"])
        tagslist.append(i["tags"])
        userlist.append(i["user"])
    return illustidlist,titlelist,pagecount,tagslist,userlist

