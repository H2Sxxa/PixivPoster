from . import LiteEditor,LiteLog
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
            self.selflog=LiteLog.LiteLog(name=__name__,style=kwargs["litelog_style"])
        else:
            self.selflog=LiteLog.LiteLog(name=__name__,style="D")
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
        return self.ConfigCon[key]
    def editCfg(self) -> None:
        '''@void'''
        if self.litelog:
            self.selflog.infolog("Open a editer")
            self.addbindlog()
        LiteEditor.LiteEditor().run(config=True,configpath=self.ConfigLocation,CfgSign=self.ConfigSign)
        if self.litelog:
            self.selflog.infolog("Close the editer")
            self.addbindlog()
            self.loadCfg()
            self.selflog.infolog("Last config -> "+str(self.ConfigCon))
            self.addbindlog()
    def addbindlog(self) -> None:
        if self.bindlog != None:
            self.bindlog.lastlog=self.selflog.lastlog
            self.bindlog.logcache.append(self.bindlog.lastlog)