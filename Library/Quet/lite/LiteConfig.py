from . import LiteEditor,LiteLog
from json import dumps,loads
class LiteConfig():
    def __init__(self,ConfigLocation:str,**kwargs) -> None:
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
        if kwargs.__contains__("bindlog"):
            self.bindlog=kwargs["bindlog"]
        else:
            self.bindlog=None
        self.ConfigCon={}
        self.ConfigSign={}
        self.ConfigLocation=ConfigLocation
        if kwargs.__contains__("ConfigSignLocation"):
            self.ConfigSignLocation=kwargs["ConfigSignLocation"]
        if kwargs.__contains__("litelog"):
            self.litelog=True
        else:
            self.litelog=False
    def saveCfg(self) -> None:
        '''@void'''
        if self.litelog:
            self.selflog.infolog("Save the Config")
            if self.bindlog != None:
                self.bindlog.lastlog=self.selflog.lastlog
                self.bindlog.logcache.append(self.bindlog.lastlog)
        with open(self.ConfigLocation,"w",encoding="utf-8") as f:
            f.write(dumps(self.ConfigCon))
    def loadCfg(self) -> None:
        '''@void\nuse it with the ConfigLocation arg'''
        if self.litelog:
            self.selflog.infolog(f"Load from {self.ConfigLocation}")
            if self.bindlog != None:
                self.bindlog.lastlog=self.selflog.lastlog
                self.bindlog.logcache.append(self.bindlog.lastlog)
        self.ConfigCon=loads(open(self.ConfigLocation,"w",encoding="utf-8").read())
    def loadCfgSign(self) -> None:
        '''@void\nuse it with the ConfigSignLocation arg'''
        if self.litelog:
            self.selflog.infolog(f"Load from {self.ConfigSignLocation}")
            if self.bindlog != None:
                self.bindlog.lastlog=self.selflog.lastlog
                self.bindlog.logcache.append(self.bindlog.lastlog)
        self.ConfigSign=loads(open(self.ConfigSignLocation,"w",encoding="utf-8").read())
    def signCfg(self,key:str,msg:str) -> None:
        '''@void'''
        if self.litelog:
            self.selflog.infolog(f"Sign in {key} -> {msg}")
        self.ConfigSign.update({key:msg})
    def addCfg(self,key:str,defaultvaule:str) -> None:
        '''@void'''
        if self.litelog:
            self.selflog.infolog(f"Add {key} -default> {defaultvaule}")
            if self.bindlog != None:
                self.bindlog.lastlog=self.selflog.lastlog
                self.bindlog.logcache.append(self.bindlog.lastlog)
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
            if self.bindlog != None:
                self.bindlog.lastlog=self.selflog.lastlog
                self.bindlog.logcache.append(self.bindlog.lastlog)
        LiteEditor.run(config=True,configpath=self.ConfigLocation,CfgSign=self.ConfigSign)