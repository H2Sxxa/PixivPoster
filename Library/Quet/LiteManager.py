from colorama import Fore,init
class LiteLog():
    #init
    def __init__(self,**kwargs):
        '''
        name __name__ -> name=__name__\n
        style the color print style (D/L) -> style = 'L'
        '''
        init(autoreset=True)
        self.IFore=Fore
        self.logcache=[]
        self.lastlog=""
        try:
            self.style=kwargs["style"]
            if self.style not in ["D","L"]:
                self.style="D"
        except:
            self.style="D"
        try:
            self.name=kwargs["name"]
        except:
            self.name="LiteLogger"
            self.warnlog("The *name is null,it has been set to \"LiteLogger\"")
    #tool
    def gettime(self) -> str:
        return LiteTime().gettime()

    def getlogname(self) -> str:
        return LiteTime().getfulltime()+".log"
    
    def getFore(self,level:str) -> Fore:
        if self.style == "D":
            if level=="info":
                return Fore.GREEN
            if level=="warn":
                return Fore.YELLOW
            if level=="error":
                return Fore.RED
        else:
            if level=="info":
                return Fore.LIGHTGREEN_EX
            if level=="warn":
                return Fore.LIGHTYELLOW_EX
            if level=="error":
                return Fore.LIGHTRED_EX

    #print log
    def infolog(self,msg:str) -> None:
        '''@void'''
        now=self.gettime()
        print(self.getFore("info")+f"[INFO | {self.name} | {now}] "+Fore.WHITE+str(msg))
        cache_log=f"[INFO | {self.name} | {now}] "+str(msg)
        self.lastlog=cache_log
        self.logcache.append(cache_log)

    def warnlog(self,msg:str) -> None:
        '''@void'''
        now=self.gettime()
        print(self.getFore("warn")+f"[WARN | {self.name} | {now}] "+Fore.YELLOW+str(msg))
        cache_log=f"[WARN | {self.name} | {now}] "+str(msg)
        self.lastlog=cache_log
        self.logcache.append(cache_log)
        
    def errorlog(self,msg:str) -> None:
        '''@void'''
        now=self.gettime()
        print(self.getFore("error")+f"[ERROR | {self.name} | {now}] "+Fore.RED+str(msg))
        cache_log=f"[ERROR | {self.name} | {now}] "+str(msg)
        self.lastlog=cache_log
        self.logcache.append(cache_log)

    def colorprint(msg,color) -> None:
        '''@void'''
        print(color+str(msg))
    #input
    def colorinput(msg:str,color:Fore) -> str:
        print(color+str(msg),end="")
        return input()
    #write log
    def write_cache_log(self,log_path:str=None,*autologname:bool) -> None:
        '''
        @void\n
        if 'autologname' is True or 'log_path' is None, it will get a name automatically,but you still should point the log_path to a folder(./)
        '''
        if log_path == None:
            autologname=True
            log_path=""
        if autologname:
            fin_log_path=log_path+self.getlogname()
        else:
            fin_log_path=log_path
        with open(fin_log_path,"w",encoding="utf-8") as f:
            for i in self.logcache:
                f.write(i+"\n")

from json import dumps,loads
class LiteConfig():
    def __init__(self,ConfigLocation:str="./default.cfg",ConfigSignLocation:str="./default.scfg",**kwargs) -> None:
        '''
        ConfigLocation : The config path\n
        ConfigSignLocation : The config - sign path
        
        litelog(Boolean) : True/False\n
        bindlog : Add the selflog to main log system (as bindlog=LiteLog.LiteLog(name=__name__))\n
        litelog_style : (D/L)\n
        
        '''
        if kwargs.__contains__("litelog_style"):
            self.selflog=LiteLog(name=__name__,style=kwargs["litelog_style"])
        else:
            self.selflog=LiteLog(name=__name__,style="D")
        if kwargs.__contains__("litelog"):
            self.litelog=True
        else:
            self.litelog=False
        if kwargs.__contains__("bindlog"):
            self.bindlog=kwargs["bindlog"]
        else:
            self.bindlog=None
        self.ConfigCon={}
        self.ConfigSign={}
        self.ConfigLocation=ConfigLocation
        self.ConfigSignLocation=ConfigSignLocation
    def modifyCfg(self,key:str,vaule:any) -> None:
        "@void\nuse it to modify the configuration"
        if self.ConfigCon.__contains__(key):
            if self.litelog:
                self.selflog.infolog("Set "+key+":"+self.ConfigCon[key]+" to "+vaule)
            self.ConfigCon[key]=vaule
        else:
            if self.litelog:
                self.selflog.errorlog("There is not a key named"+key)
        if self.litelog:
            self.addbindlog()
    def saveCfg(self) -> None:
        '''@void'''
        if self.litelog:
            self.selflog.infolog("Save the Config")
            self.addbindlog()
        with open(self.ConfigLocation,"w",encoding="utf-8") as f:
            f.write(dumps(self.ConfigCon,indent=4))
    def saveCfgSign(self) -> None:
        '''@void'''
        if self.litelog:
            self.selflog.infolog("Save the ConfigSign")
            self.addbindlog()
        with open(self.ConfigSignLocation,"w",encoding="utf-8") as f:
            f.write(dumps(self.ConfigSign,indent=4))
    def loadCfg(self) -> None:
        '''@void\nuse it with the ConfigLocation arg'''
        if self.litelog:
            self.selflog.infolog(f"Load from {self.ConfigLocation}")
            self.addbindlog()
        self.ConfigCon=loads(open(self.ConfigLocation,"r",encoding="utf-8").read())
    def loadCfgSign(self) -> None:
        '''@void\nuse it with the ConfigSignLocation arg'''
        if self.litelog:
            self.selflog.infolog(f"Load from {self.ConfigSignLocation}")
            self.addbindlog()
        self.ConfigSign=loads(open(self.ConfigSignLocation,"r",encoding="utf-8").read())
    def signCfg(self,key:str,msg:str) -> None:
        '''@void'''
        if self.litelog:
            self.selflog.infolog(f"Sign in {key} -> {msg}")
        self.ConfigSign.update({key:msg})
    def addCfg(self,key:str,defaultvaule:any) -> None:
        '''@void'''
        if self.litelog:
            self.selflog.infolog(f"Add {key} -default> {defaultvaule}")
            self.addbindlog()
        self.ConfigCon.update({key:defaultvaule})
    def readCfg(self,key:str) -> str:
        self.loadCfg()
        if self.litelog:
            self.selflog.infolog(f"Read {key}")
        res=self.ConfigCon[key]
        for key2,vaule in self.ConfigCon.items():
            if type(key2) == str and type(self.ConfigCon[key]) == str:
                if "$"+key2+"$" in self.ConfigCon[key]:
                    res=self.ConfigCon[key].replace("$"+key2+"$",vaule)
        return res
    def addbindlog(self) -> None:
        if self.bindlog != None:
            self.bindlog.lastlog=self.selflog.lastlog
            self.bindlog.logcache.append(self.bindlog.lastlog)

import time
class LiteTime():
	def getdate(self):
		return time.strftime("%Y-%m-%d", time.localtime())
	def gettime(self):
		return time.strftime("%H:%M:%S", time.localtime())
	def getfulltime(self):
		return time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())