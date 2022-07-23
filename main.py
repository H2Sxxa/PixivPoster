#!/usr/bin/env python
import platform
if platform.system() == "Linux":
    import os
    import sys
    p = os.path.dirname((os.path.abspath(__file__)))
    sys.path.insert(1,p)
    print("add "+p+" support")
from Library.Quet import TaskManager
from Library.Quet import LiteManager
from Library.Quet import MarkDownManager
from Library.Pixiv import Direct
from Library.Web.wordpress import wp_XMLRPC
from Library.Web.typecho import tc_XMLRPC
from Library.Web.flaurm.api import Flarum
from vaule import *
from os import listdir, remove, system,getcwd
from shutil import move
import markdown2
myLog=LiteManager.LiteLog(name=__name__)
myTime=LiteManager.LiteTime()
myMarkDown=MarkDownManager.MarkDown()
def initTasks(taskfile):
    global myTask
    myTask=TaskManager.Task(taskfile)
    myTask.setArgsTasks("use_config",initVar)
    myTask.setTask("run",run)
def initVar(Location):
    global myConfig,myMarkDownInter
    myConfig = LiteManager.LiteConfig(Location+"/config.cfg",litelog=True,bindlog=myLog)
    myMarkDownInter=MarkDownManager.Interpreter(Location+"/base.md")
    init(Location=Location)
def init(Location):
    global MyPixiv
    if "config.cfg" not in listdir(Location):
        myLog.infolog("Init the config now")
        myConfig.addCfg("web_type","local")
        myConfig.addCfg("web_local_name","blog")
        myConfig.addCfg("web_local_dir","./web/hexo/$web_local_name$/source/_posts")
        myConfig.addCfg("web_local_root","./web/hexo/$web_local_name$")
        myConfig.addCfg("web_local_deploy","_deploy.bat")
        myConfig.addCfg("web_address","https://localhost:6800/xmlrpc.php")
        myConfig.addCfg("web_title","Pixiv $date choiceness")
        myConfig.addCfg("web_flarum_tagid","1")
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
    myMarkDownInter.loadall(artistname=artistlist,illust=sortillustlist,illustid=illustidlist,illustname=titlelist,artistid=artistidlist,illusttag=puretagslist)
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
        myClient.setArticle(myConfig.readCfg("web_title").replace("$date",myTime.getdate()),content=mdnc)
        articleid=myClient.postArticle()
        myLog.infolog("Post successfully,the article id is "+str(articleid))
    if webtype == "local":
        try:
            move(mdn,myConfig.readCfg("web_local_dir"))
        except Exception as e:
            myLog.errorlog(str(e))
        system("cd \""+myConfig.readCfg("web_local_root")+"\" && "+myConfig.readCfg("web_local_deploy"))
    if webtype == "flarum":
        myClient=Flarum(myConfig.readCfg("web_account"),myConfig.readCfg("web_password"),myConfig.readCfg("web_address"))
        myClient.postArticle(myConfig.readCfg("web_title").replace("$date",myTime.getdate()),mdnc,myConfig.readCfg("web_flarum_tagid"))
def run():
    global mdnc,mdn,illustidlist,titlelist,pagecount,tagslist,artistlist,hmdnc,puretagslist,sortillustlist,artistidlist
    try:
        illustidlist,titlelist,pagecount,tagslist,artistlist=getRank()
        illusttags=[]
        tr_illusttags=[]
        for s1tagslist in tagslist:
            illusttags.append(MyPixiv.extarctSort(s1tagslist,"name"))
            tr_illusttags.append(MyPixiv.extarctSort(s1tagslist,"translated_name"))
        puretagslist=[illusttags,tr_illusttags]
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
initTasks(getcwd()+"/task.txt")
myTask.runTask()
for k,v in myTask.getTasks().items():
    myLog.infolog("[%s]%s" % (k,v))
try:
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
except:
    pass