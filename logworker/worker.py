# -*- coding: utf-8 -*-
__author__ = 'fanzhanao'

import sys,time,os

from daemon import Daemon
from consumer import Consumer

class LogWorker(Daemon):
    """
    守护进程处理数据
    """
    def run(self):
        consumer = Consumer()
        while True:
            consumer.progress()
            # time.sleep(1)

if __name__ == "__main__":
    worker = LogWorker('/tmp/logworker.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
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