from json import loads
from requests import get
import datetime
def getdate():
	date = datetime.date.today()+datetime.timedelta(-1)
	#datetime.date.today(pytz.timezone('Asia/Tokyo'))
	#pytz.timezone('Asia/Tokyo')
	#pip install pytz
	return date.strftime("%Y-%m-%d")

def getdatelist(beginlist,endlist):
	datelist=[]
	begin = datetime.date(int(beginlist[0]),int(beginlist[1]),int(beginlist[2]))
	end = datetime.date(int(endlist[0]),int(endlist[1]),int(endlist[2]))
	for i in range((end - begin).days+1):
		day = begin + datetime.timedelta(days=i)
		datelist.append(str(day))
	return datelist
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
        raise ValueError("API Requests Error")
    if apitext == "{\"illusts\":[],\"next_url\":null}":
        raise ValueError("A empty date")
    if apitext == "{\"code\":500,\"msg\":\"请求失败\"}" or apitext=="获取失败":
        raise ValueError("The api may get something error")
    try:
        return loads(apitext)
    except:
        raise ValueError("The api may get something error")
