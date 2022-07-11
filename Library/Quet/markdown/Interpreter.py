from . import MarkDown

class Interpreter():
    def __init__(self,basemdlocation:str="./default.base.md") -> None:
        self.markdown=MarkDown.MarkDown()
        self.sample=open(basemdlocation,"r",encoding="utf-8").read()
        self.sample=self.setVar(self.sample)
        self.samplelist=self.sample.splitlines()
        self.outlist=[]
    def loadall(self,**infodict):
        '''
        image(dict):
            artistname:strlist
            aritstid:strlist
            illust:strlist(the link of the illust)[(p1,p2,...),(p1,p2,...),...]
            illustname:strlist
            illustid:strlist
            #TODO illusttag:[strlist,int or None(all tag)]
        '''  
        self.artistname=infodict["artistname"]
        self.artistid=infodict["artistid"]
        self.illust=infodict["illust"]
        self.illustname=infodict["illustname"]
        self.illustid=infodict["illustid"]
        #self.illusttag=infodict["illusttag"]
        self.mainthread()
    def mainthread(self):
        for obj in self.samplelist:
            if "?>img," in obj:
                objself=obj.split(">img,")[1].split("<?")[0]
                objself="?>img,"+objself+"<?"
                objlist=obj.split(">img,")[1].split("<?")[0].split(",")
                self.maxillust=objlist[0]
                self.illustsample=objlist[1]
                if self.maxillust == "None":
                    self.maxillust=len(self.illustid)
                else:
                    self.maxillust=int(self.maxillust)
                
                for illustid,illustname,artistname,artistid in zip(self.illustid,self.illustname,self.artistname,self.artistid):
                    oneindex=self.illustid.index(illustid)
                    oneobj=self.illustsample.replace(":illustid",str(illustid)).replace(":illustname",illustname).replace(":artistname",artistname["name"]).replace(":artistid",str(artistid))
                    finimg=""
                    for img in self.illust[oneindex]:
                        img=self.markdown.setImg(img,imgtext=illustname)
                        if finimg == "":
                            finimg=img
                        else:
                            finimg=finimg+"\n"+img
                    oneobj=oneobj.replace(":illust",finimg)
                    self.outlist.append(oneobj)
                fin=""
                for i in self.outlist:
                    if i == self.outlist[0]:
                        fin=i
                    else:
                        fin=fin+i
                self.sample=self.sample.replace(objself,fin)
    def setVar(self,obj):
        if "$date" in obj:
            from time import strftime,localtime
            obj=obj.replace("$date",strftime("%Y-%m-%d", localtime()))
        if "$br" in obj:
            obj=obj.replace("$br",self.markdown.br)
        return obj
    def sampleout(self,location):
        with open(location,"w",encoding="utf-8") as f:
            f.write(self.sample.replace("$n","\n"))
        