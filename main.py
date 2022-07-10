from Library.Quet.lite import LiteLog,LiteConfig
from Library.Quet.markdown import MarkDown
from Library.Pixiv import Direct
from vaule import *
from os import listdir
myLog=LiteLog.LiteLog(name=__name__)
myConfig=LiteConfig.LiteConfig(litelog=True,bindlog=myLog)
def init():
    global MyPixiv
    if "default.cfg" not in listdir():
        MyPixiv=Direct.Direct(sni=True)
        myLog.infolog("Init the config now")
        myConfig.addCfg("web_type","wordpress")
        myConfig.addCfg("pixiv_mode","day")
        myLog.infolog("Start to login in Pixiv,please login it and input the code")
        auth=MyPixiv.login()
        myConfig.addCfg("refresh_token",auth["refresh_token"])
        myConfig.saveCfg()
        loadcfgsign()
    else:
        MyPixiv=Direct.Direct(sni=True,refresh_token=myConfig.readCfg("refresh_token"))
        myLog.infolog("Login with the token...")
        MyPixiv.login()
        myConfig.loadCfg()
        loadcfgsign()
def loadcfgsign():
    myConfig.signCfg("pixiv_mode",sign_mode)
def getRank():
    myLog.infolog("Strart to get the Pixiv rank")
    return MyPixiv.sortRank(MyPixiv.getRank(myConfig.readCfg("pixiv_mode")))
    
init()
#myConfig.editCfg()
illustidlist,titlelist,pagecount,tagslist,userlist=getRank()
urllist=MyPixiv.sort2Rank(pagecount,illustidlist,titlelist)
for i in urllist:
    myLog.infolog(i)