from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from . import litetime
from json import loads,dumps
####
def loadcfg(location):
    global globalCfg
    globalCfg=location
    f=open(location,'r',encoding="utf-8")
    root.title("LiteEditor - "+location)
    f2=f.read()
    configjson=loads(f2)
    f2=""
    for key,vaule in configjson.items():
        f2=f2+addsign(key)+key+" -> "+vaule+"\n"
    f.close()
    text.insert(INSERT,f2)
def addsign(key):
    if CfgSign == {}:
        pass
    else:
        for sk,sv in CfgSign.items():
            if sk == key:
                return "#"+sv+"\n"
def savecfg():
    findict={}
    raw=text.get("1.0",'end-1c')
    rawlist=raw.splitlines()
    for i in rawlist:
        if "#" in i:
            rawlist.remove(i)
    for i in rawlist:
        asplit=i.split(" -> ")
        if len(asplit) == 1:
            v=""
        else:
            k,v=asplit[0],asplit[1]
        findict.update({k:v})
    with open(globalCfg,"w",encoding="utf-8") as f:
        f.write(dumps(findict))
####
def openfile():
    filename=filedialog.askopenfilename()
    if filename == "":
        return
    global globalfilename
    globalfilename=filename
    try:
        f=open(filename,'r',encoding="utf-8")
        f2=f.read()
        f.close()
        root.title("LiteEditor - "+filename)
    except Exception as e:
        messagebox.showerror("ERROR",str(e))
        return
    text.insert(INSERT,f2)

def savefileas():
    filename=filedialog.asksaveasfilename(filetypes=[("*",".*")])
    if filename == "":
        return
    root.title("LiteEditor - "+filename)
    global globalfilename
    globalfilename=filename
    with open(filename,'a',encoding="utf-8") as f:
        f.write(text.get("1.0",'end-1c'))

def savefile():
    try:
        str(globalfilename)
    except Exception as e:
        messagebox.showerror("ERROR",str(e))
        savefileas()
    try:
        with open(globalfilename,'w',encoding="utf-8") as f:
            f.write(text.get("1.0",'end-1c'))
    except:
        savefileas()
def open_father():
    from os import startfile
    from os.path import dirname
    try:
        startfile(dirname(globalfilename))
    except Exception as e:
        messagebox.showerror("ERROR",str(e))
        return
def quit():
    root.destroy()

def about():
    messagebox.showinfo("关于","开发者：Change\n封装&二次开发者：H2Sxxa")

def callback():
    try:
        text.edit_undo()
    except:
        return
def fastsave(event):
    savefile()
    root.title("LiteEditor - "+globalfilename+" saved "+litetime.getfulltime())
def fastsavecfg(event):
    savecfg()
    root.title("LiteEditor - "+globalCfg+" saved "+litetime.getfulltime())
def popup(event):
    popupmenu.post(event.x_root,event.y_root)

def copy():
    global content
    content=text.get(SEL_FIRST,SEL_LAST)
    text.clipboard_clear()
    text.clipboard_append(content)

def cut():
    global content
    content=text.get(SEL_FIRST,SEL_LAST)
    text.delete(SEL_FIRST,SEL_LAST)
    text.clipboard_clear()
    text.clipboard_append(content)

def paste():
    text.insert(INSERT,text.clipboard_get())
    
def textdelete():
    text.delete(SEL_FIRST,SEL_LAST)

def get_time():
    msg=litetime.getfulltime()
    text.insert(INSERT,msg)

def run(**kwargs):
    '''
    config@Nullable(bool)\n
    configpath@Nullable(str)
    '''
    global root
    root=Tk()
    root.title("LiteEditor")
    global text
    text=Text(root,selectforeground="black",undo=True,font=50)
    text.pack(fill=BOTH,expand=YES)
    if kwargs.__contains__("CfgSign"):
        global CfgSign
        CfgSign=kwargs["CfgSign"]
    try:
        if kwargs.__contains__("config"):
            runcfg=1
            text.bind('<Control-s>', fastsavecfg)
        else:
            runcfg=0
            text.bind('<Control-s>', fastsave)
        if kwargs.__contains__("configpath"):
            loadcfg(kwargs["configpath"])
    except Exception as e:
        print(str(e))
        runcfg=0
    
    topmenu=Menu(root)
    filemenu=Menu(topmenu,tearoff=False)
    if runcfg != 1:
        filemenu.add("command",label="打开",command=openfile)
    filemenu.add_command(label="打开父文件夹",command=open_father)
    if runcfg != 1:
        filemenu.add_command(label="保存",command=savefile)
    else:
        filemenu.add_command(label="保存",command=savecfg)
    if runcfg != 1:
        filemenu.add_command(label="另存为",command=savefileas)
    filemenu.add_separator()
    filemenu.add_command(label="退出",command=quit)
    topmenu.add_cascade(label="文件", menu=filemenu)
    editmenu=Menu(topmenu,tearoff=False)
    editmenu.add_command(label="撤销",command=callback)
    editmenu.add("command",label="剪切",command=cut)
    editmenu.add_command(label="复制",command=copy)
    editmenu.add_command(label="粘贴",command=paste)
    editmenu.add_separator()
    editmenu.add_command(label="时间/日期",command=get_time)

    topmenu.add_cascade(label="编辑",menu=editmenu)

    helpmenu=Menu(topmenu,tearoff=False)
    helpmenu.add_command(label="关于",command=about)
    topmenu.add_cascade(label="帮助",menu=helpmenu)

    global popupmenu
    popupmenu=Menu(root,tearoff=False)
    if runcfg != 1:
        popupmenu.add_command(label="保存",command=savefile)
    else:
        popupmenu.add_command(label="保存",command=savecfg)
    if runcfg != 1:
        popupmenu.add_command(label="另存为",command=savefileas)
    popupmenu.add_separator()
    popupmenu.add_command(label="撤回",command=callback)
    popupmenu.add_separator()
    popupmenu.add("command",label="剪切",command=cut)
    popupmenu.add_command(label="复制",command=copy)
    popupmenu.add_command(label="粘贴",command=paste)
    popupmenu.add("command",label="删除",command=textdelete)
    text.bind("<Button-3>",popup)

    root.config(menu=topmenu)
    mainloop()