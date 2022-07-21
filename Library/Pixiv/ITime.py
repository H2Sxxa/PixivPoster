import datetime
def getdate():
	date = datetime.date.today()+datetime.timedelta(-1)
	#datetime.date.today(pytz.timezone('Asia/Tokyo'))
	#pytz.timezone('Asia/Tokyo')
	#pip install pytz
	return date.strftime("%Y-%m-%d")

def getdatelist(beginlist,endlist):
	datelist=[]
	begin = datetime.date(int(beginlist[0]),int(beginlist[1]),int(beginlist[2]))
	end = datetime.date(int(endlist[0]),int(endlist[1]),int(endlist[2]))
	for i in range((end - begin).days+1):
		day = begin + datetime.timedelta(days=i)
		datelist.append(str(day))
	return datelist