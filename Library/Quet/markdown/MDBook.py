from os import listdir,mkdir
from os.path import isdir
from urllib import parse
from . import MarkDown
class MDBook():
    def __init__(self) -> None:
        '''
        MDBgen=MDBook.MDBook()\n
        MDBgen.scanFolder("sourcelib")#a folder with your picture folder\n
        MDBgen.genBook(address=".",urlsafe=True)
        '''
        self.selfMD=MarkDown.MarkDown()
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
            
