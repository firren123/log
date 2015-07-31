# -*- coding: utf-8 -*-
__author__ = 'fanzhanao'

import os,zipfile,glob,json

class ReadFile(object):
	"""
	读取指定目录的文件
	"""
	def __init__(self,path):
		# zip 文件 path
		self.workpath = path
		# exract 目录
		self.extractpath = path + r'/extracts'
		print(self.extractpath)
		self.zipfiles = []
		self.files = []
		self.initSelf()

	def initSelf(self):
		self.getFileList()
		if not os.path.exists(self.extractpath):
			os.mkdir(self.extractpath)

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

	def parseFile(self):
		if len(self.files) > 0 :
			for f in self.files:
				print(f)
				with open(f) as ff:
					lines = ff.readlines()


#
# if __name__ == "__main__":
# 	f = ReadFile(r'/Users/fanzhanao/Work/python/data')
# 	f.unzipFile()
# 	f.parseFile()