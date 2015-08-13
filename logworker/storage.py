# -*- coding: utf-8 -*-
__author__ = 'fanzhanao'

import json
import pymysql.cursors

class Storage(object):

	def __init__(self,conf={}):
		self.host = conf['host'] if conf['host'] else '127.0.0.1'
		self.user = conf['user'] if conf['user'] else 'root'
		self.password = conf['password'] if conf['password'] else ''
		self.port = int(conf['port']) if conf['port'] else 3306
		self.dbname = conf['db'] if conf['db'] else 'statistics'
		self.charset = conf['charset'] if conf['charset'] else 'utf8'
		self.db = None
		# 插入SQL
		self.insert_sql = 'INSERT INTO logs (event,parameter,uid,deviceid,devicemodel,appid,appversion,os,osversion,logtime,appname,appbuildversion) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'

	def dbConnect(self):
		if self.db is None:
			self.db = pymysql.connect(host= self.host,
                             user= self.user,
                             passwd= self.password,
                             db= self.dbname,
                             charset= self.charset,
                             cursorclass=pymysql.cursors.DictCursor)

	def dbClose(self):
		if self.db is not None:
			self.db.close()
			self.db = None

	def save(self,data):
		try:
			cursor = self.db.cursor()
			cursor.executemany(self.insert_sql,data)
			cursor.close()
			self.db.commit()
		except Exception as e:
			print("执行Mysql: %s 时出错：%s data is:%s" % (self.insert_sql, e ,data))
