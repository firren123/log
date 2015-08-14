# -*- coding: utf-8 -*-
__author__ = 'fanzhanao'

import sys

if sys.version_info[0] == 2:
    from daemon import Daemon
else:
    from daemon3 import Daemon

from fileconsumer import FileConsumer

class FileLogWorker(Daemon):
    """
    守护进程处理数据
    """
    def run(self):
        consumer = FileConsumer()
        while True:
            consumer.progress()
            # time.sleep(1)

if __name__ == "__main__":
    worker = FileLogWorker('/tmp/filelogworker.pid')
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