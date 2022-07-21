from json import loads
from requests import get
import platform
if platform.system() == "Linux":
    import os
    import sys
    p = os.path.dirname(os.path.dirname((os.path.abspath(__file__))))
    sys.path.insert(1,p)
    print("add "+p+"support")
from . import ITime
def pixiv(date=None):
    if date == None:
        adate="date="+ITime.getdate()
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
        raise ValueError("API Requests Error")
    if apitext == "{\"illusts\":[],\"next_url\":null}":
        raise ValueError("A empty date")
    if apitext == "{\"code\":500,\"msg\":\"请求失败\"}" or apitext=="获取失败":
        raise ValueError("The api may get something error")
    try:
        return loads(apitext)
    except:
        raise ValueError("The api may get something error")
