from Library.Quet.lite import LiteLog
from Library.Quet.markdown import MarkDown
from Library.Pixiv import Direct
MP=Direct.Direct(sni=True,refresh_token='6kTgCA7VbDcxrhAeMliKxDVvsu9Jb4tW2qmb3tVM3FU')
response=MP.login()
refresh_token=response["refresh_token"]
rk=MP.getRank(mode="day_r18")
illustidlist,titlelist,pagecount,tagslist,userlist=MP.sortRank(rk)
urllist=MP.sort2Rank(pagecount,illustidlist,titlelist)
for i in urllist:
    print(i)