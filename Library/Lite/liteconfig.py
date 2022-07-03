from . import liteeditor,litelog
from json import dumps,loads
class liteconfig():
    def __init__(self,ConfigLocation:str,**kwargs) -> None:
        '''
        ConfigLocation : The config path\n
        
        litelog(Boolean) : True/False\n
        litelog_style : (D/L)\n
        
        ConfigSignLocation : The config - sign path
        
        '''
        if kwargs.__contains__("litelog_style"):
            self.selflog=litelog.litelog(name=__name__,style=kwargs["litelog_style"])
        else:
            self.selflog=litelog.litelog(name=__name__,style="D")
        
        self.ConfigCon={}
        self.ConfigSign={}
        self.ConfigLocation=ConfigLocation
        if kwargs.__contains__("ConfigSignLocation"):
            self.ConfigSignLocation=kwargs["ConfigSignLocation"]
        if kwargs.__contains__("litelog"):
            self.litelog=True
        else:
            self.litelog=False
    def updateCfg(self):
        if self.litelog:
            self.selflog.infolog("Update the Config")
        self.ConfigCon=loads(open(self.ConfigLocation,"r",encoding="utf-8").read())
    def saveCfg(self) -> None:
        '''@void'''
        if self.litelog:
            self.selflog.infolog("Save the Config")
        with open(self.ConfigLocation,"w",encoding="utf-8") as f:
            f.write(dumps(self.ConfigCon))
    def loadCfg(self) -> None:
        '''@void\nuse it with the ConfigLocation arg'''
        if self.litelog:
            self.selflog.infolog(f"Load from {self.ConfigLocation}")
        self.ConfigCon=loads(open(self.ConfigLocation,"w",encoding="utf-8").read())
    def loadCfgSign(self) -> None:
        '''@void\nuse it with the ConfigSignLocation arg'''
        if self.litelog:
            self.selflog.infolog(f"Load from {self.ConfigSignLocation}")
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
        self.ConfigCon.update({key:defaultvaule})
    def readCfg(self,key:str) -> str:
        self.updateCfg()
        if self.litelog:
            self.selflog.infolog(f"Read {key}")
        return self.ConfigCon[key]
    def editCfg(self) -> None:
        '''@void'''
        if self.litelog:
            self.selflog.infolog("Open a editer")
        liteeditor.run(config=True,configpath=self.ConfigLocation,CfgSign=self.ConfigSign)