from colorama import Fore,init
from . import litetime

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
        return litetime.gettime()

    def getlogname(self) -> str:
        return litetime.getfulltime()+".log"
    
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
        print(self.getFore("info")+f"[INFO | {self.name} | {now}] "+Fore.WHITE+msg)
        cache_log=f"[INFO | {self.name} | {now}] "+msg
        self.lastlog=cache_log
        self.logcache.append(cache_log)

    def warnlog(self,msg:str) -> None:
        '''@void'''
        now=self.gettime()
        print(self.getFore("warn")+f"[WARN | {self.name} | {now}] "+Fore.YELLOW+msg)
        cache_log=f"[WARN | {self.name} | {now}] "+msg
        self.lastlog=cache_log
        self.logcache.append(cache_log)
        
    def errorlog(self,msg:str) -> None:
        '''@void'''
        now=self.gettime()
        print(self.getFore("error")+f"[ERROR | {self.name} | {now}] "+Fore.RED+msg)
        cache_log=f"[ERROR | {self.name} | {now}] "+msg
        self.lastlog=cache_log
        self.logcache.append(cache_log)

    def colorprint(msg,color) -> None:
        '''@void'''
        print(color+msg)
    #input
    def colorinput(msg:str,color:Fore) -> str:
        print(color+msg,end="")
        return input()
    #write log
    def write_cache_log(self,log_path:str,*autologname:bool) -> None:
        '''
        @void\n
        if 'autologname' is True, it will get a name automatically,but you still should point the log_path to a folder(./)
        '''
        if autologname:
            fin_log_path=log_path+self.getlogname()
        else:
            fin_log_path=log_path
        with open(fin_log_path,"w",encoding="utf-8") as f:
            for i in self.logcache:
                f.write(i+"\n")