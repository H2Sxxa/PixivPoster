def mk_list(pagecount:list,illustid:list,titlelist:list,address="pixiv.re"):
    urllist=[]
    for page,pid,title in zip(pagecount,illustid,titlelist):
        if "　" in title:
            title=title.replace("　"," ")
        if int(page) == 1:
            urllist.append({"url":f"https://{address}/"+str(pid)+".jpg","out":title+".jpg"})
        else:
            for pagenum in range(1,int(page)+1):
                urllist.append({"url":f"https://{address}/"+str(pid)+"-"+str(pagenum)+".jpg","out":title+" "+str(pagenum)+".jpg"})
    return urllist