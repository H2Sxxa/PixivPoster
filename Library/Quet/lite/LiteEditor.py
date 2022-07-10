from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from json import loads,dumps
from . import LiteTime
class LiteEditor():
    def run(self,**kwargs) -> None:
        '''
        config@Noneable(bool)\n
        configpath@Noneable(str)
        '''
        self.filename=""
        self.CfgSign={}
        self.Itime=LiteTime.LiteTime()
        self.root=Tk()
        self.root.title("LiteEditor")
        self.text=Text(self.root,selectforeground="black",undo=True,font=50)
        self.text.pack(fill=BOTH,expand=YES)
        self.text.tag_config('bold', font='Courier 12 bold',background="yellow")
        self.text.tag_config('hide', elide=1)
        self.lastplace=self.text.index('1.0')
        if kwargs.__contains__("CfgSign"):
            self.CfgSign=kwargs["CfgSign"]
        try:
            if kwargs.__contains__("config"):
                self.runcfg=1
                self.text.bind('<Control-s>', self.fastsavecfg)
            else:
                self.runcfg=0
                self.text.bind('<Control-s>', self.fastsave)
            if kwargs.__contains__("configpath"):
                self.filename=kwargs["configpath"]
                self.loadcfg()
                self.boldtag()
        except Exception as e:
            print(str(e))
            self.runcfg=0
        topmenu=Menu(self.root)
        filemenu=Menu(topmenu,tearoff=False)
        if self.runcfg != 1:
            filemenu.add("command",label="打开",command=self.openfile)
        filemenu.add_command(label="打开父文件夹",command=self.open_father)
        if self.runcfg != 1:
            filemenu.add_command(label="保存",command=self.savefile)
        else:
            filemenu.add_command(label="保存",command=self.savecfg)
        if self.runcfg != 1:
            filemenu.add_command(label="另存为",command=self.savefileas)
        filemenu.add_separator()
        filemenu.add_command(label="退出",command=quit)
        topmenu.add_cascade(label="文件", menu=filemenu)
        editmenu=Menu(topmenu,tearoff=False)
        editmenu.add_command(label="撤销",command=self.callback)
        editmenu.add("command",label="剪切",command=self.cut)
        editmenu.add_command(label="复制",command=self.copy)
        editmenu.add_command(label="粘贴",command=self.paste)
        editmenu.add_separator()
        editmenu.add_command(label="时间/日期",command=self.get_time)
        topmenu.add_cascade(label="编辑",menu=editmenu)

        helpmenu=Menu(topmenu,tearoff=False)
        helpmenu.add_command(label="关于",command=self.about)
        topmenu.add_cascade(label="帮助",menu=helpmenu)

        self.popupmenu=Menu(self.root,tearoff=False)
        if self.runcfg != 1:
            self.popupmenu.add_command(label="保存",command=self.savefile)
        else:
            self.popupmenu.add_command(label="保存",command=self.savecfg)
        if self.runcfg != 1:
            self.popupmenu.add_command(label="另存为",command=self.savefileas)
        self.popupmenu.add_separator()
        self.popupmenu.add_command(label="撤回",command=self.callback)
        self.popupmenu.add_separator()
        self.popupmenu.add("command",label="剪切",command=self.cut)
        self.popupmenu.add_command(label="复制",command=self.copy)
        self.popupmenu.add_command(label="粘贴",command=self.paste)
        self.popupmenu.add("command",label="删除",command=self.textdelete)
        self.text.bind("<Button-3>",self.popup)
        self.root.config(menu=topmenu)
        mainloop()
    def boldtag(self):
        nextplace = self.text.search('[B]', self.lastplace, 'end')
        if nextplace:
            boldon = nextplace + ' +3c'
            self.text.tag_add('hide', nextplace, boldon)
            boldoff = self.text.search('[/B]', boldon, 'end')
            if boldoff:
                self.text.tag_add('bold', boldon, boldoff) 
                codoff = boldoff + ' +4c'
                self.text.tag_add('hide', boldoff, codoff)
            self.lastplace = codoff
            self.boldtag()
        else:
            return
    def openfile(self):
        filename=filedialog.askopenfilename()
        if filename == "":
            return
        self.filename=filename
        try:
            f=open(filename,'r',encoding="utf-8")
            f2=f.read()
            f.close()
            self.root.title("LiteEditor - "+filename)
        except Exception as e:
            messagebox.showerror("ERROR",str(e))
            return
        self.text.insert(INSERT,f2)

    def savefileas(self):
        filename=filedialog.asksaveasfilename(filetypes=[("*",".*")])
        if filename == "":
            return
        self.root.title("LiteEditor - "+filename)
        with open(filename,'a',encoding="utf-8") as f:
            f.write(self.text.get("1.0",'end-1c'))

    def savefile(self):
        if self.filename == "":
            self.savefileas()
        else:
            with open(self.filename,'w',encoding="utf-8") as f:
                f.write(self.text.get("1.0",'end-1c'))
    def open_father(self):
        from os import startfile
        from os.path import dirname
        try:
            startfile(dirname(self.filename))
        except Exception as e:
            messagebox.showerror("ERROR",str(e))
            return
    def quit(self):
        self.root.destroy()

    def about(self):
        messagebox.showinfo("关于","开发者：H2Sxxa")

    def callback(self):
        try:
            self.text.edit_undo()
        except:
            return
    def fastsave(self,event):
        if self.filename !="":
            self.savefile()
            self.root.title("LiteEditor - "+self.filename+" saved "+self.Itime.getfulltime())
        else:
            self.savefileas()
    def fastsavecfg(self,event):
        self.savecfg()
        self.root.title("LiteEditor - "+"1"+" saved "+self.Itime.getfulltime())
    def popup(self,event):
        self.popupmenu.post(event.x_root,event.y_root)

    def copy(self):
        content=self.text.get(SEL_FIRST,SEL_LAST)
        self.text.clipboard_clear()
        self.text.clipboard_append(content)

    def cut(self):
        content=self.text.get(SEL_FIRST,SEL_LAST)
        self.text.delete(SEL_FIRST,SEL_LAST)
        self.text.clipboard_clear()
        self.text.clipboard_append(content)

    def paste(self):
        self.text.insert(INSERT,self.text.clipboard_get())
        
    def textdelete(self):
        self.text.delete(SEL_FIRST,SEL_LAST)

    def get_time(self):
        msg=self.Itime.getfulltime()
        self.text.insert(INSERT,msg)
    ###
    def loadcfg(self):
        f=open(self.filename,'r',encoding="utf-8")
        self.root.title("LiteEditor - "+self.filename)
        f2=f.read()
        configjson=loads(f2)
        f2=""
        for key,vaule in configjson.items():
            key=str(key)
            if type(vaule) == str:
                f2=f2+self.addsign(key)+key+" -> "+vaule+"\n"
            elif type(vaule) == bool:
                if vaule == False:
                    f2=f2+self.addsign(key)+key+" -> "+"False(bool)"+"\n"
                else:
                    f2=f2+self.addsign(key)+key+" -> "+"True(bool)"+"\n"
            elif type(vaule) == dict:
                f2=f2+self.addsign(key)+key+" -> "+str(vaule)+"\n"
            elif type(vaule) == int:
                f2=f2+self.addsign(key)+key+" -> "+str(vaule)+"(int)\n"
            else:
                print("unsupport",type(vaule))
        f.close()
        self.text.insert(INSERT,f2)
    def addsign(self,key):
        if self.CfgSign.__contains__(key):
            if "\n" in self.CfgSign[key]:
                self.CfgSign[key]=self.CfgSign[key].replace("\n","[/B]\n[B]#")
            return "[B]#"+self.CfgSign[key]+"[/B]\n"
        else:
            return ""
    def savecfg(self):
        findict={}
        raw=self.text.get("1.0",'end-1c')
        rawlist=raw.splitlines()
        mirrorlist=[]
        for i in rawlist:
            if "#" not in i:
                mirrorlist.append(i)
        rawlist=mirrorlist
        for i in rawlist:
            asplit=i.split(" -> ")
            if len(asplit) == 1:
                v=""
            else:
                if asplit[1] == "False(bool)":
                    asplit[1] = False
                elif asplit[1] == "True(bool)":
                    asplit[1] = True
                elif "(int)" in asplit[1]:
                    asplit[1]=int(asplit[1].replace("(int)",""))
                k,v=asplit[0],asplit[1]
            findict.update({k:v})
        with open(self.filename,"w",encoding="utf-8") as f:
            f.write(dumps(findict,indent=4))
    ####
LiteEditor()