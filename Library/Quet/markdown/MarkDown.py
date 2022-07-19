
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
        else:
            hasimgtext = False
            
        if kwargs.__contains__("rpimgtext"):
            rpimgtext = kwargs["rpimgtext"]
            hasrpimgtext = True
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
    