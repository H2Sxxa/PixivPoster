from Library.Quet.lite import LiteLog,LiteConfig,LiteTime
from Library.Quet.markdown import MarkDown,Interpreter
from Library.Pixiv import Direct
from vaule import *
from os import listdir
myLog=LiteLog.LiteLog(name=__name__)
myConfig=LiteConfig.LiteConfig(litelog=True,bindlog=myLog)
myMarkDown=MarkDown.MarkDown()
myMarkDownInter=Interpreter.Interpreter("default.base.md")
myTime=LiteTime.LiteTime()
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
        myLog.infolog("If all failed , you should restart it...")
        MyPixiv.login()
        myConfig.loadCfg()
        loadcfgsign()
def loadcfgsign():
    myConfig.signCfg("pixiv_mode",sign_mode)
def getRank():
    myLog.infolog("Start to get the Pixiv rank")
    return MyPixiv.sortRank(MyPixiv.getRank(myConfig.readCfg("pixiv_mode")))
def genMarkdown():
    myLog.infolog("Start to generate markdown")
    myMarkDownInter.loadall(artistname=artistlist,illust=sortillustlist,illustid=illustidlist,illustname=titlelist)
    mdname=myTime+" "+myConfig.readCfg("pixiv_mode")+".md"
    myMarkDownInter.sampleout(mdname)
    myLog.infolog("Congratulate!All generate finished!")
    return mdname
init()
illustidlist,titlelist,pagecount,tagslist,artistlist=getRank()
urllist=MyPixiv.sort2Rank(pagecount,illustidlist,titlelist)
pureurllist=MyPixiv.extarctlink(urllist)
sortillustlist=MyPixiv.sortillustlink(illustidlist,pureurllist)
mdn=genMarkdown()
mdnc=open(mdn,"r",encoding="utf-8").read()