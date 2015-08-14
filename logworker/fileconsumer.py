# -*- coding: utf-8 -*-
__author__ = 'fanzhanao'

import os,zipfile,glob,json,redis,time
from storage import Storage

class FileConsumer(object):
	"""
	读取指定目录的文件
	"""
	def __init__(self):
		# zip 文件 path
		config = json.load(open(u'../config/config.json'))
		self.redisConf = config['redis']
		self.data = []
		self.lines = []
		self.redis = redis.Redis(host='10.10.107.35',port=6379,db=0)
		self.storage = Storage(config['db'])
		# self.initSelf()

	def progress(self):
		f = self.redis.rpop('zipfiles')
		if zipfile.is_zipfile(f):
			self.read_zip_file(f)
			if len(self.lines) > 0:
				try:
					# 分析每行数据
					pubData = json.loads(self.lines.pop(0).decode('utf-8'),encoding="utf-8")
					for evt  in self.lines:
						evt = json.loads(evt.decode('utf-8'),encoding='utf-8')
						param = json.dumps(evt['param'],encoding="utf-8", ensure_ascii=False)
						_row = (evt['event'],param,str(pubData['uid']),pubData['deviceid'],pubData['devicemodel'],str(pubData['appid']),pubData['appversion'],pubData['os'],pubData['osversion'],time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(int(evt['timestamp']))),pubData['appname'],pubData['appbuildversion'])
						self.data.append(_row)

					if len(self.data) > 0 :
						self.storage.dbConnect()
						self.saved()
						self.storage.dbClose()
					os.remove(f)
				except OSError:
					pass

	def saved(self):
		if self.data is None or len(self.data) == 0:
			return False
		try:
			self.storage.save(self.data)
		except Exception as e:
			print("执行Mysql: 时出错：%s data is:%s" % ( e ,self.data))


	def read_zip_file(self,filepath):
		zfile = zipfile.ZipFile(filepath)
		for finfo in zfile.infolist():
			ifile = zfile.open(finfo)
			self.lines = ifile.readlines()

# if __name__ == "__main__":
# 	f = FileConsumer()
# 	f.progress()