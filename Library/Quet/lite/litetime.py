import time
class LiteTime():
	def getdate(self):
		return time.strftime("%Y-%m-%d", time.localtime())
	def gettime(self):
		return time.strftime("%H:%M:%S", time.localtime())
	def getfulltime(self):
		return time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())