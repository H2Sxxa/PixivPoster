class MarkDown():
    def __init__(self) -> None:
        '''
        Emoji https://gist.github.com/rxaviers/7360908
        '''
        self.br="<br>"
        self.splitline="\n***\n"
        self.sample=""
    def setTitle(self,text:str,level:int) -> str:
        '''
        # Heading level 1	<h1>Heading level 1</h1>	
        ## Heading level 2	<h2>Heading level 2</h2>	
        ### Heading level 3	<h3>Heading level 3</h3>	
        #### Heading level 4	<h4>Heading level 4</h4>	
        ##### Heading level 5	<h5>Heading level 5</h5>	
        ###### Heading level 6	<h6>Heading level 6</h6>	
        '''
        return "#"*int(level)+" %s" % text
    
    def setBr(self,text:str) -> str:
        return text+self.br
    
    def setItalic_Bold(self,text:str) -> str:
        return "***%s***" % text

    def setBold(self,text:str) -> str:
        return "**%s**" % text
    
    def setItalic(self,text:str) -> str:
        return "*%s*" % text
    
    def setQuote(self,text:str) -> str:
        return "> %s" % text
    
    def setOrderList(self,strlist:list) -> list:
        '''
        Must a string list
        '''
        newlist=[]
        for order,item in zip(range(1,len(list)+1),strlist):
            newlist.append("%s. %s" % (order,item))
        return newlist
    def setDisorderList(self,strlist:list) -> list:
        '''
        Must a string list
        '''
        newlist=[]
        for item in strlist:
            newlist.append("- %s" % item)
        return newlist
    
    def setinListitem(self,text:str) -> str:
        return "    %s" % text
    
    def setCode(self,text:str) -> str:
        return "``%s``" % text
    
    def setLink(self,text:str,link:str,**kwargs) -> str:
        '''
        #### kwargs:\n
            isEmail(bool)\n
            linktext(str)
            
        '''

        if kwargs.__contains__("isEmail"):
            isEmail = kwargs["isEmail"]
        else:
            isEmail = False
        if kwargs.__contains__("linktext"):
            linktext = kwargs["linktext"]
            haslinktext = True
        else:
            haslinktext = False
        if isEmail:
            if haslinktext:
                return "[%s]<%s \"%s\">" % (text,link,linktext)
            else:
                return "[%s]<%s>" % (text,link)
        else:
            if haslinktext:
                return "[%s](%s \"%s\")" % (text,link,linktext)
            else:
                return "[%s](%s)" % (text,link)
    def setImg(self,link:str,**kwargs):
        '''
        #### kwargs:\n
            rpimgtext(str)\n
            imgtext(str)
        '''
        if kwargs.__contains__("imgtext"):
            imgtext = kwargs["imgtext"]
            hasimgtext = True
            if imgtext == "":
                hasimgtext=False
        else:
            hasimgtext = False
        if kwargs.__contains__("rpimgtext"):
            rpimgtext = kwargs["rpimgtext"]
            hasrpimgtext = True
            if rpimgtext == "":
                hasrpimgtext=False
        else:
            hasrpimgtext = False
        if hasimgtext and hasrpimgtext:
            return "![%s](%s \"%s\")" % (rpimgtext,link,imgtext)
        elif hasimgtext and not hasrpimgtext:
            return "![](%s \"%s\")" % (link,imgtext)
        elif not hasimgtext and hasrpimgtext:
            return "![%s](%s)" % (rpimgtext,link)
        else:
            return "![](%s)" % link
    def setImgSlide(self,markdownImgList:list):
        for img in markdownImgList:
            if img != markdownImgList[-1]:
                slide=slide+img+","
            else:
                slide=slide+img
        return "<%s>" % slide
    def setSample(self,Sample:str,ReplaceDict:str) -> Exception or None:
        for key,vaule in ReplaceDict.items():
            if key in Sample:
                Sample.replace(key,vaule)
        self.sample=Sample


from json import loads

class Interpreter():
    def __init__(self,basemdlocation:str="./default.base.md") -> None:
        self.markdown=MarkDown()
        self.sample=open(basemdlocation,"r",encoding="utf-8").read()
        self.sample=self.setVar(self.sample)
        self.samplelist=self.sample.splitlines()
        self.mystyle={"illust":{"rpimgtext":"","imgtext":""}}
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
            if ":style>" in obj:
                self.sample=self.sample.replace(obj+"\n","")
                obj = obj.replace(":style>","")
                styledict:dict = loads(obj)
                if "function" not in styledict.keys():
                    print("A illegal style")
                    continue
                if styledict["function"] == "illust":
                    if "rpimgtext" in styledict.keys():
                        rpimgtext = styledict["rpimgtext"]
                    else:
                        rpimgtext = ""
                    if "imgtext" in styledict.keys():
                        imgtext = styledict["imgtext"]
                    else:
                        imgtext = ""
                    self.mystyle["illust"]={"rpimgtext":rpimgtext,"imgtext":imgtext}
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
                    if self.illustid.index(illustid)+1 > self.maxillust:
                        break
                    oneindex=self.illustid.index(illustid)
                    oneobj=self.illustsample.replace(":illustid",str(illustid)).replace(":illustname",illustname).replace(":artistname",artistname["name"]).replace(":artistid",str(artistid))
                    finimg=""
                    for img in self.illust[oneindex]:
                        img=self.markdown.setImg(img,imgtext=self.mystyle["illust"]["imgtext"].replace(":illustid",str(illustid)).replace(":illustname",illustname).replace(":artistname",artistname["name"]).replace(":artistid",str(artistid)),rpimgtext=self.mystyle["illust"]["rpimgtext"].replace(":illustid",str(illustid)).replace(":illustname",illustname).replace(":artistname",artistname["name"]).replace(":artistid",str(artistid)))
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
        from time import strftime,localtime
        if "$date" in obj:
            obj=obj.replace("$date",strftime("%Y-%m-%d", localtime()))
        if "$time" in obj:
            obj=obj.replace("$time",strftime(("%H-%M-%S"),localtime()))
        if "$br" in obj:
            obj=obj.replace("$br",self.markdown.br)
        return obj
    def sampleout(self,location):
        with open(location,"w",encoding="utf-8") as f:
            f.write(self.sample.replace("$n","\n"))


from os import listdir,mkdir
from os.path import isdir
from urllib import parse
class MDBook():
    def __init__(self) -> None:
        '''
        MDBgen=MDBook.MDBook()\n
        MDBgen.scanFolder("sourcelib")#a folder with your picture folder\n
        MDBgen.genBook(address=".",urlsafe=True)
        '''
        self.selfMD=MarkDown()
        self.folderlist=[]
        self.imglist=[]
        self.sourcedir=[]
        self.location=""

    def scanFolder(self,folder:str) -> None:
        self.folderlist=listdir(folder)
        self.location=folder
        self.scanFolderIMG()
    def scanFolderIMG(self) -> None:
        for onefolder in self.folderlist:
            self.imglist.append(listdir(self.location+"/"+onefolder))
        #print(self.imglist)
    def genBook(self,address:str=".",outdir:str="./out",urlsafe:bool=False) -> None:
        address=address+"/"+self.location
        if not isdir(outdir):
            mkdir(outdir)
        for imgfolder in self.folderlist:
            sourcedir=[]
            for img in self.imglist[self.folderlist.index(imgfolder)]:
                sourcedir.append(address+"/"+imgfolder+"/"+img)
            self.sourcedir.append(sourcedir)
        for sourceimglist,foldername in zip(self.sourcedir,self.folderlist):
            fin=""
            for sourceimg in sourceimglist:
                if urlsafe:
                    sourceimg=parse.quote(sourceimg)
                if fin == "":
                    fin=self.selfMD.setImg(sourceimg,rpimgtext=sourceimg)
                else:
                    fin=fin+"\n"+self.selfMD.setImg(sourceimg,rpimgtext=sourceimg)
            fin="# "+foldername+"\n"+fin
            #print(len(self.folderlist),self.folderlist.index(foldername),self.folderlist.index(foldername))
            if self.folderlist.index(foldername)!=0:
                lastfoldername=self.folderlist[self.folderlist.index(foldername)-1]
                if urlsafe:
                    lastfoldername=parse.quote(lastfoldername)
                fin=fin+"\n### "+self.selfMD.setLink(self.selfMD.setBold("上一话 %s" % self.folderlist[self.folderlist.index(foldername)-1]),"./"+lastfoldername+".md")
            if self.folderlist.index(foldername)!=len(self.folderlist)-1:
                prefoldername=self.folderlist[self.folderlist.index(foldername)+1]
                if urlsafe:
                    prefoldername=parse.quote(prefoldername)
                fin=fin+"\n### "+self.selfMD.setLink(self.selfMD.setBold("下一话 %s" % self.folderlist[self.folderlist.index(foldername)+1]),"./"+prefoldername+".md")
            with open(outdir+"/"+foldername+".md","w",encoding="utf-8") as f:
                f.write(fin)
            
