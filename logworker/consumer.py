# -*- coding: utf-8 -*-
__author__ = 'fanzhanao'

import json,time, multiprocessing,logging
import redis
import pymysql.cursors
from storage import Storage
# from config.config import

class Consumer:
    """
    获取redis的数据，取出后做处理
    """
    def __init__(self):
        self.config = json.load(open(u'../config/config.json'))
        self.redisConf = self.config['redis']
        self.queue_key = self.redisConf['queue_key']
        # 链接redis
        # self.redis = redis.Redis(host=str(self.redisConf['server']),port=int(self.redisConf['port']),db=int(self.redisConf['db']))
        self.redis = redis.Redis(host='10.10.107.35',port=6379,db=0)
        logging.basicConfig(filename = self.config['error_log'], level = logging.DEBUG)
        # self.db = None
        self.storage = Storage(self.config['db'])
        self.num = 50
        self.data = []

    def progress(self):
        start = 0
        len_events = self.redis.llen('events')
        if int(len_events) > 0:
            self.data = []
            while start < min(len_events,self.num):
                _data = self.redis.rpop('events')
                self.parseData(_data)
                start+=1

            if len(self.data) > 0 :
                self.storage.dbConnect()
                self.saved()
                self.storage.dbClose()
        else:
            return


    def parseData(self,dataStr):
        """
        分析数据
        :return:
        """
        if dataStr is None:
            return None
        try:
            data = json.loads(dataStr.decode('utf-8'),encoding="utf-8")
            events = data['events']
            if not isinstance(events,list):
                events = [events]
            for dict in events:
                param = json.dumps(dict['param'],encoding="utf-8", ensure_ascii=False)
                _row = (dict['event'],param,str(data['uid']),data['deviceid'],data['devicemodel'],str(data['appid']),data['appversion'],data['os'],data['osversion'],time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(int(dict['timestamp']))),data['appname'],data['appbuildversion'])
                self.data.append(_row)
        except Exception as e:
            logging.error("convert data to json object error! --data is :" + dataStr + "; \nerror is " + str(e)  + ";\n===============================================================\n")
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
            self.storage.save(self.data)
        except Exception as e:
            print("执行Mysql: 时出错：%s data is:%s" % ( e ,self.data))



# if __name__ == "__main__":
#     consumer = Consumer()
#     consumer.progress()