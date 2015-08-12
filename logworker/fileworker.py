# -*- coding: utf-8 -*-
__author__ = 'fanzhanao'

import os,zipfile,glob,json,redis

class ReadFile(object):
	"""
	读取指定目录的文件
	"""
	def __init__(self):
		# zip 文件 path
		# exract 目录
		self.extractpath = r''
		self.zipfiles = []
		self.files = []
		self.redis = None
		self.initSelf()

	def initSelf(self):
		self.getFileList()
		if self.redis is None:
			self.redis = redis.Redis(host='127.0.0.1',port=6379,db=0)
		if not os.path.exists(self.extractpath):
			os.mkdir(self.extractpath)

	def progress(self):
		file_len = self.redis.llen('zipfiles')
		while file_len > 0:
			f = self.redis.rpop('zipfiles')
			if zipfile.is_zipfile(f):
				nlist = []
				with zipfile.ZipFile(f) as zf:
					nlist = zf.extractall('.')
				if nlist:
					try:
						os.remove(f)
					except OSError:
						pass

					#pars file
					for ff in nlist:
						self.parseFile(ff)

			file_len = file_len-1


	def getFileList(self):
		if os.path.exists(self.workpath):
			for f in glob.glob(self.workpath+"/*.zip"):
				self.zipfiles.append(f)

	def unzipFile(self):
		"""
		:desc 解压缩文件
		:param zipfile:
		:return: file
		"""
		if len(self.zipfiles) > 0:
			for f in self.zipfiles:
				if zipfile.is_zipfile(f):
					try:
						zfile = zipfile.ZipFile(f)
						zfile.extractall(self.extractpath)
						(filePath,ext) = os.path.splitext(self.extractpath +"/" + os.path.basename(f))
						self.files.append(filePath)
					except:
						print('error')
						continue

	def parseFile(self,f):
		print(f)
		try:
			with open(f) as ff:
				lines = ff.readlines()
		except OSError:
			pass

#
# if __name__ == "__main__":
# 	f = ReadFile(r'/Users/fanzhanao/Work/python/data')
# 	f.unzipFile()
# 	f.parseFile()