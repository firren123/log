#!/bin/python
# -*- coding: utf-8 -*-

__author__ = 'fanzhanao'
import sys,time

if sys.version_info[0] == 2:
    from daemon import Daemon
else:
    from daemon3 import Daemon
    print ("daemon3")

from consumer import Consumer

class LogWorker(Daemon):
    """
    守护进程处理数据
    """
    def run(self):
        # import pdb; pdb.set_trace()
        consumer = Consumer()
        while True:
            consumer.progress()
            # time.sleep(1)

def test():
    consumer = Consumer()
    while True:
        consumer.progress()
        # time.sleep(1)

if __name__ == "__main__":
    a = test()
    exit(0)
    worker = LogWorker('/data/html/logworker/logworker/test/logworker.pid')
    if len(sys.argv) == 2:
        print ("bbbbb")
        if 'start' == sys.argv[1]:
            print ("start")
            worker.start()
        elif 'stop' == sys.argv[1]:
            worker.stop()
        elif 'restart' == sys.argv[1]:
            worker.restart()
        else:
            print ("unknown command")
            sys.exit(2)

    else:
        print ("usage: %s start|stop|restart" % sys.argv[0])
        sys.exit(2)
