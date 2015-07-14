__author__ = 'fanzhanao'

import io,json,time
import redis
import pymysql.cursors

# from config.config import

class Consumer:
    """
    获取redis的数据，取出后做处理
    """
    def __init__(self):
        config = json.load(open('../config/config.json'))
        redisConf = config['redis']
        # print(redisConf)
        self.redis_server = redisConf['server']
        self.redis_port = int(redisConf['port'])
        self.redis_db = int(redisConf['db'])
        self.queue_key = redisConf['queue_key']
        # 链接redis
        # self.redis = redis.Redis(host=self.redis_server,port=self.redis_port,db=int(self.redis_db))
        self.redis = redis.Redis(host='127.0.0.1',port=6379,db=0)
        self.db = None

    def progress(self):
        start = 0
        start_time = time.time()
        # len = self.redis.llen('events')
        while start < 1:
            _data = self.redis.rpop('events')
            events = self.parseData(_data)
            if events:
                self.saved(events)
            start+=1

        # str = self.redis.rpop('events')
        # pp = pprint.PrettyPrinter(indent=4)
        # pp.pprint(str)
        # return str
        print(time.time()-start_time)


    def parseData(self,data):
        """
        分析数据
        :return:
        """
        data = data.decode()
        returnObjs = []
        if isinstance(data,str):
            data = json.loads(data)
        if isinstance(data,type({})):
            data = [data]
        # print(str(data))
        for dict in data:
            # print(str(dict))
            _row = tuple([dict['event']['name'],json.dumps(dict['event']['param']),dict['uid'],dict['deviceid'],dict['deviceModel'],dict['appid'],201,dict['os'],840])
            returnObjs.append(_row)
        return returnObjs

    def saved(self, data = []):
        """
        :return : bool
        """
        #连接数据库
        self.dbConnect()
        print("data is:%s" % str(data))
        if data is None or data == '':
            return
        if isinstance(data,type({})):
            self.singleSave(data)
        elif isinstance(data,(tuple, list)):
            """
            批量更新数据
            """
            self.mutilSave(data)
        # 关闭数据库
        self.dbClose()

    def singleSave(self,row):
        """
        保存数据到数据库中
        :param data:
        :return:
        """
        if row is None or row =='':
            return
        print (row)

    def mutilSave(self,data):
        """
        批量插入数据
        :param data:
        :return:
        """
        cursor = self.db.cursor()
        try:
            sql = "INSERT INTO logs (event,parameter,uid,deviceid,devicemodel,appid,appversion,os,osversion) VALUES ('%s','%s',%d,'%s','%s','%s',%d,%d,'%s',%d)"
            print('sql is:%s data is:%s' %  (sql,data))
            cursor.executemany(sql,data)
        except Exception as e:
            print("执行Mysql: %s 时出错：%s" % (sql, e))
        finally:
            cursor.close()
            self.db.commit()

    def dbConnect(self):
        """
        数据库连接
        :return:
        """
        if self.db is None:
            self.db = pymysql.connect(host='localhost',
                             user='root',
                             passwd='',
                             db='logs',
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)

    def dbClose(self):
        if self.db is not None:
            self.db.close()


if __name__ == "__main__":
    consumer = Consumer()
    consumer.progress()