# -*- coding: utf-8 -*-
__author__ = 'fanzhanao'

import json
import redis
import pymysql.cursors
# from config.config import

class Consumer:
    """
    获取redis的数据，取出后做处理
    """
    def __init__(self):
        config = json.load(open(u'../config/config.json'))
        self.redisConf = config['redis']
        self.dbConf = config['db']
        self.queue_key = self.redisConf['queue_key']
        self.insert_sql = 'INSERT INTO logs (event,parameter,uid,deviceid,devicemodel,appid,appversion,os,osversion) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        # 链接redis
        # self.redis = redis.Redis(host=str(self.redisConf['server']),port=int(self.redisConf['port']),db=int(self.redisConf['db']))
        self.redis = redis.Redis(host='127.0.0.1',port=6379,db=0)
        self.db = None
        self.num = 50
        self.data = []

    def progress(self):
        start = 0
        len_events = self.redis.llen('events')
        if int(len_events) > 0:
            self.data = []
            while start < min(len,self.num):
                _data = self.redis.rpop('events')
                self.parseData(_data)
                start+=1

            if len(self.data) > 0 :
                self.dbConnect()
                self.saved()
                self.dbClose()
        else:
            return


    def parseData(self,data):
        """
        分析数据
        :return:
        """
        if data is None:
            return None
        try:
            data = json.loads(data.decode())
            if not isinstance(data,list):
                data = [data]
            for dict in data:
                param = json.dumps(dict['event']['param'])
                _row = (dict['event']['name'],param,str(dict['uid']),dict['deviceid'],dict['deviceModel'],str(dict['appid']),'201',dict['os'],'840')
                self.data.append(_row)
        except Exception as e:
            print("error is %s" % e)
            return None
        # finally:



    def saved(self):
        """
        :return : bool
        """
        #连接数据库

        if self.data is None or len(self.data) == 0:
            return False
        if isinstance(self.data,type({})):
            self.singleSave()
        elif isinstance(self.data,(tuple, list)):
            """
            批量更新数据
            """
            self.mutilSave()

    def singleSave(self,row):
        """
        保存数据到数据库中
        :param data:
        :return:
        """
        if row is None or row =='':
            return
        print (row)

    def mutilSave(self):
        """
        批量插入数据
        :param data:
        :return:
        """
        # cursor = self.db.cursor()
        try:
            cursor = self.db.cursor()
            cursor.executemany(self.insert_sql,self.data)
            cursor.close()
            self.db.commit()
        except Exception as e:
            print("执行Mysql: %s 时出错：%s data is:%s" % (self.insert_sql, e ,self.data))


    def dbConnect(self):
        """
        数据库连接
        :return:
        """
        if self.db is None:
            self.db = pymysql.connect(host= self.dbConf['server'],
                             user= self.dbConf['user'],
                             passwd= self.dbConf['password'],
                             db= self.dbConf['db'],
                             charset= self.dbConf['charset'],
                             cursorclass=pymysql.cursors.DictCursor)
            # self.db = pymysql.connect(host= 'localhost',
            #                  user='root',
            #                  passwd='',
            #                  db='logs',
            #                  charset='utf8',
            #                  cursorclass=pymysql.cursors.DictCursor)

    def dbClose(self):
        if self.db is not None:
            self.db.close()
            self.db = None


# if __name__ == "__main__":
#     consumer = Consumer()
#     consumer.progress()