#!/usr/bin/env python
import platform
print(platform.system())
if platform.system() == "Linux":
    import os
    import sys
    p = os.path.dirname(os.path.dirname((os.path.abspath(__file__))))
    #print(p+"/Library/Quet/lite")
    #sys.path.insert(1,p+"/Library/Quet/lite")
    os.system("export PYTHONPATH="+p+":$PYTHONPATH")
    print("add all support")

from Library.Quet.lite import LiteLog,LiteConfig,LiteTime
from Library.Quet.markdown import MarkDown,Interpreter
from Library.Pixiv import Direct
from Library.Web.wordpress import wp_XMLRPC
from Library.Web.typecho import tc_XMLRPC
myLog=LiteLog.LiteLog(name=__name__)
myConfig=LiteConfig.LiteConfig(litelog=True,bindlog=myLog)
myMarkDown=MarkDown.MarkDown()
myMarkDownInter=Interpreter.Interpreter(".\default.base.md")
myTime=LiteTime()
from vaule import *
from os import listdir, remove, system
from shutil import move
import markdown2
def init():
    global MyPixiv
    if "default.cfg" not in listdir():
        myLog.infolog("Init the config now")
        myConfig.addCfg("web_type","wordpress")
        myConfig.addCfg("web_local_name","blog")
        myConfig.addCfg("web_local_dir","./web/hexo/$web_local_name$/source/_posts")
        myConfig.addCfg("web_local_root","./web/hexo/$web_local_name$")
        myConfig.addCfg("web_local_deploy","_deploy.bat")
        myConfig.addCfg("web_address","https://localhost:6800/xmlrpc.php")
        myConfig.addCfg("web_title","Pixiv $date choiceness")
        myConfig.addCfg("web_account","admin@mail.com")
        myConfig.addCfg("web_password","YourPassword")
        myConfig.addCfg("clean_cache",False)
        myConfig.addCfg("sock_proxy","")
        myConfig.addCfg("sni",True)
        myConfig.addCfg("savelog",False)
        myConfig.addCfg("pixiv_mode","day")
        myConfig.addCfg("refresh_token","")
        myConfig.saveCfg()
        myLog.infolog("Start to login in Pixiv,please login it and input the code")
        if myConfig.readCfg("sock_proxy") != "":
            if myConfig.readCfg("sni"):
                MyPixiv=Direct.Direct(sock=myConfig.readCfg("sock_proxy"),sni=True)
            else:
                MyPixiv=Direct.Direct(sock=myConfig.readCfg("sock_proxy"))
        else:
            if myConfig.readCfg("sni"):
                MyPixiv=Direct.Direct(sni=True)
            else:
                MyPixiv=Direct.Direct()
        auth=MyPixiv.login()
        myConfig.modifyCfg("refresh_token",auth["refresh_token"])
        myConfig.saveCfg()
        loadcfgsign()
    else:
        if myConfig.readCfg("refresh_token") == "":
            auth=MyPixiv.login()
            myConfig.modifyCfg("refresh_token",auth["refresh_token"])
            myConfig.saveCfg()
        else:
            MyPixiv=Direct.Direct(sni=True,refresh_token=myConfig.readCfg("refresh_token"))
            myLog.infolog("Login with the token...")
            myLog.infolog("If all failed , you should restart it...")
            MyPixiv.login()
        loadcfgsign()
def loadcfgsign():
    myConfig.signCfg("pixiv_mode",sign_mode)
def getRank():
    myLog.infolog("Start to get the Pixiv rank")
    return MyPixiv.sortRank(MyPixiv.getRank(myConfig.readCfg("pixiv_mode")))
def genMarkdown():
    myLog.infolog("Start to generate markdown")
    myMarkDownInter.loadall(artistname=artistlist,illust=sortillustlist,illustid=illustidlist,illustname=titlelist,artistid=artistidlist)
    mdname=myTime.getdate()+" "+myConfig.readCfg("pixiv_mode")+".md"
    myMarkDownInter.sampleout(mdname)
    myLog.infolog("Congratulate!All generate finished!")
    return mdname
def postArticle():
    webtype=myConfig.readCfg("web_type")
    if webtype == "wordpress":
        myClient=wp_XMLRPC.wp_XMLRPC(myConfig.readCfg("web_address"),myConfig.readCfg("web_account"),myConfig.readCfg("web_password"))
        myClient.setArticle(myConfig.readCfg("web_title").replace("$date",myTime.getdate()),content=hmdnc)
        articleid=myClient.postArticle()
        myLog.infolog("Post successfully,the article id is "+str(articleid))
    if webtype == "typecho":
        myClient=tc_XMLRPC.tc_XMLRPC(myConfig.readCfg("web_address"),myConfig.readCfg("web_account"),myConfig.readCfg("web_password"))
        myClient.setArticle(myConfig.readCfg("web_title").replace("$date",myTime.getdate()),content=hmdnc)
        articleid=myClient.postArticle()
        myLog.infolog("Post successfully,the article id is "+str(articleid))
    if webtype == "local":
        try:
            move(mdn,myConfig.readCfg("web_local_dir"))
        except Exception as e:
            myLog.errorlog(str(e))
        system("cd \""+myConfig.readCfg("web_local_root")+"\" && "+myConfig.readCfg("web_local_deploy"))
try:
    init()
    illustidlist,titlelist,pagecount,tagslist,artistlist=getRank()
    urllist=MyPixiv.sort2Rank(pagecount,illustidlist,titlelist)
    pureurllist=MyPixiv.extarctSort(urllist,"url")
    sortillustlist=MyPixiv.sortillustlink(illustidlist,pureurllist)
    artistidlist=MyPixiv.extarctSort(artistlist,"id")
    mdn=genMarkdown()
    mdnc=open(mdn,"r",encoding="utf-8").read()
    hmdnc=str(markdown2.markdown_path(mdn))
    with open(mdn.replace(".md",".html"),"w",encoding="utf-8") as f:
        f.write(hmdnc)
    postArticle()
except Exception as e:
    myLog.errorlog(str(e))
finally:
    if myConfig.readCfg("savelog") == True:
        myLog.write_cache_log()
    if myConfig.readCfg("clean_cache") == True:
        try:
            remove(mdn)
        except:
            pass
        try:
            remove(mdn.replace(".md",".html"))
        except:
            pass
    