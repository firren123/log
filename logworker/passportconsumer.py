# -*- coding: utf-8 -*-
__author__ = 'lichenjun'
import json,time, multiprocessing,logging
import redis
import pymysql.cursors
# from config.config import

class Consumer:
    """
    获取redis的数据，取出后做处理
    """
    def __init__(self):
        self.config = json.load(open(u'../config/config.json'))
        self.redisConf = self.config['redis']
        # self.queue_key = self.redisConf['queue_key']
        self.queue_key = self.config['passport_queue_key']
        # 链接redis
        # self.redis = redis.Redis(host=str(self.redisConf['server']),port=int(self.redisConf['port']),db=int(self.redisConf['db']))
        self.redis = redis.Redis(self.redisConf.host,self.redisConf.port,self.redisConf.db)
        logging.basicConfig(filename = self.config['error_log'], level = logging.DEBUG)
        self.db = None
        self.storage = self.config['passportdb']
        self.num = 50
        self.data = []

    def progress(self):
        #import pdb; pdb.set_trace()
        start = 0
        len_events = self.redis.llen(self.queue_key)
        if int(len_events) > 0:
            self.data = []
            while start < min(len_events,self.num):
                _data = self.redis.rpop(self.queue_key)
                self.parseData(_data)
                start+=1

            if len(self.data) > 0 :
                self.dbConnect()
                self.createPassportSql()
                self.saved()
                self.dbClose()
        else:
            return

    def dbConnect(self):
        if self.db is None:
            self.db = pymysql.connect(host=self.storage['host'],
                                      user=self.storage['user'],
                                      passwd=self.storage['password'],
                                      db=self.storage['dbname'],
                                      port=self.storage['port'],
                                      charset=self.storage['charset'],
                                      cursorclass=pymysql.cursors.DictCursor)
        else:
            a =self.db
            d = a
    def dbClose(self):
        if self.db is not None:
            self.db.close()
            self.db = None

    def createPassportSql(self):
        # _row = (dict['others'],str(data['passportid']),data['active_id'],data['active_name'],str(data['uid']),data['ip'],data['even'],data['info'],time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(int(dict['addtime'])))
        self.insert_sql = 'INSERT INTO passport_log (others,passportid,active_id,active_name,uid,ip,even,info) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'
    def parseData(self,dataStr):
        """
        分析数据
        :return:
        """

        from urllib import unquote
        test = unquote(dataStr)
        dataStr = test
        if dataStr is None:
            return None
        try:
            data = json.loads(dataStr.decode('utf-8'),encoding="utf-8")
            events = data['even']
            if not isinstance(events,list):
                events = [events]
            for dict in events:
                param = json.dumps(dict['param'],encoding="utf-8", ensure_ascii=False)
                #_row = (dict['event'],param,str(data['uid']),data['deviceid'],data['devicemodel'],str(data['appid']),data['appversion'],data['os'],data['osversion'],time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(int(dict['timestamp']))),data['appname'],data['appbuildversion'])
                others = json.dumps(data['others'])
                info = json.dumps(data['info'])


                _row = (others,data['passportid'],data['active_id'],data['active_name'],str(data['uid']),data['ip'],dict['event'],info)
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
            try:
                self.singleSave()
            except Exception as e:
                print("执行Mysql: 时出错：%s data is:%s" % ( e ,self.data))
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

    def save(self, data):
        # data = [(u'click', u'{"cat_id": 102, "art_id": 2210}', 1000, u'xxxxxxxxx', u'iPhone 5', 1, u'2.8.2', u'IOS8.3', u'8.4', '1974-04-11 07:33:22', u'\u5546\u4e1a\u5468\u520a', 1873, '7')]
        cursor = self.db.cursor()
        cursor.executemany(self.insert_sql, data)
        cursor.close()
        self.db.commit()
    def mutilSave(self):
        """
        批量插入数据
        :param data:
        :return:
        """
        # cursor = self.db.cursor()
        try:
            self.save(self.data)
        except Exception as e:
            print("执行Mysql: 时出错：%s data is:%s" % ( e ,self.data))




if __name__ == "__main__":
    consumer = Consumer()
    while True:
        consumer.progress()
