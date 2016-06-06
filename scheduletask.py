# -*- coding: utf-8 -*-


"""
@version: ??
@author: xlliu
@contact: liu.xuelong@163.com
@site: https://github.com/xlliu
@software: PyCharm
@file: scheduletask.py
@time: 2016/4/26 9:39
"""
import os
import subprocess
import threading

# import sys
#
# reload(sys)
# sys.setdefaultencoding('utf-8')


class myThread(threading.Thread):

    HOTPLAY_CATCHUP_DIR = os.path.dirname(__file__)

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        self.do_init_catchup()

    def do_init_catchup(self, log_name="celery_info"):
        print 'start to init catch output info log name is %s' % (log_name)
        job_args = 'source %s/init_catch_up.sh >> logs/%s.log' % (self.HOTPLAY_CATCHUP_DIR, log_name)
        # job_args = 'celery -A mongo2mysql.celery worker --loglevel=info > logs/%s.log' % (log_name)
        # job_args = 'celery -A mongo2mysql.celery worker --loglevel=info'
        print 'job_args:', job_args
        P = subprocess.Popen(job_args, shell=True)
        rt_code = P.wait()
        if rt_code == 0:
            print 'job success...'
        else:
            print 'job error:%d' % (rt_code)
