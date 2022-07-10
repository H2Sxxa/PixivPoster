from Library.Quet.lite import LiteLog,LiteConfig
from Library.Quet.markdown import MarkDown
from Library.Pixiv import Direct
from vaule import *
from os import listdir
myLog=LiteLog.LiteLog(name=__name__)
myConfig=LiteConfig.LiteConfig(litelog=True,bindlog=myLog)
def init():
    if "default.cfg" not in listdir():
        myLog.infolog("Init the config now")
        myConfig.addCfg("web-",123)
        myConfig.addCfg("pixiv-mode","day")
        myConfig.saveCfg()
        loadcfgsign()
    else:
        myConfig.loadCfg()
        loadcfgsign()
def loadcfgsign():
    myConfig.signCfg("pixiv-mode",sign_mode)

init()
myConfig.editCfg()
#myLog.write_cache_log()
'''
try:
    MP=Direct.Direct(sni=True,refresh_token='1236kTgCA7VbDcxrhAeMliKxDVvsu9Jb4tW2qmb3tVM3FU')
    response=MP.login()
    refresh_token=response["refresh_token"]
    rk=MP.getRank(mode="day_r18")
    illustidlist,titlelist,pagecount,tagslist,userlist=MP.sortRank(rk)
    urllist=MP.sort2Rank(pagecount,illustidlist,titlelist)
    for i in urllist:
        print(i)
except Exception as e:
    myLog.errorlog(e)
myLog.write_cache_log()
'''