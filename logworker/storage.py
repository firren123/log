# -*- coding: utf-8 -*-
__author__ = 'fanzhanao'

import json
import pymysql.cursors

class Storage(object):

	def __init__(self,conf={}):
		self.host = conf['host'] if conf['host'] else 'vhost01'
		self.user = conf['user'] if conf['user'] else 'root'
		self.password = conf['password'] if conf['password'] else 'modernmedia'
		self.port = int(conf['port']) if conf['port'] else 3308
		self.dbname = conf['db'] if conf['db'] else 'statistics'
		self.charset = conf['charset'] if conf['charset'] else 'utf8'
		self.db = None
		# 插入SQL
		self.insert_sql = 'INSERT INTO logs (event,parameter,uid,deviceid,devicemodel,appid,appversion,os,osversion,logtime,appname,appbuildversion) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
		#self.insert_sql = 'INSERT INTO logs (event,parameter,uid,deviceid,devicemodel) VALUES (%s,%s,%s,%s,%s)'
		print(self.insert_sql)

	def dbConnect(self):
		if self.db is None:
			self.db = pymysql.connect(host= self.host,
                             user= self.user,
                             passwd= self.password,
                             db= self.dbname,
                             port=self.port,
                             charset= self.charset,
                             cursorclass=pymysql.cursors.DictCursor)

	def dbClose(self):
		if self.db is not None:
			self.db.close()
			self.db = None

	def save(self,data):
		#data = [(u'click', u'{"cat_id": 102, "art_id": 2210}', 1000, u'xxxxxxxxx', u'iPhone 5', 1, u'2.8.2', u'IOS8.3', u'8.4', '1974-04-11 07:33:22', u'\u5546\u4e1a\u5468\u520a', 1873, '7')]
		cursor = self.db.cursor()
		cursor.executemany(self.insert_sql,data)
		cursor.close()
		self.db.commit()


	def save_bak(self,data):
		try:
			data = [(u'click', u'{"cat_id": 102, "art_id": 2210}', '1000', u'xxxxxxxxx', u'iPhone 5', '1', u'2.8.2', u'IOS8.3', u'8.4', '1974-04-11 07:33:22', u'\u5546\u4e1a\u5468\u520a', '1873', '7')]
			cursor = self.db.cursor()
			cursor.executemany(self.insert_sql,data)
			cursor.close()
			self.db.commit()
		except Exception as e:
			print("执行Mysql: %s 时出错：%s data is:%s" % (self.insert_sql, e ,data))
