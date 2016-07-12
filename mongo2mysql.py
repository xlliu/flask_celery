# -*- coding: utf-8 -*-
from __future__ import absolute_import
import logging
import logging.config
import time
from celery import Celery, platforms
from flask import Flask, jsonify

from server.request_context import RequestAction

app = Flask(__name__)
# redis://:password@hostname:port/db_number

app.config.update(
        #CELERY_BROKER_URL='amqp://xlliu:zkey@120.131.64.225:5672/xlliuvhost',
        CELERY_BROKER_URL='amqp://42.62.6.220:5672/',
        # CELERY_BROKER_URL='redis://10.0.0.3:6379'
)


celery = Celery("mongo2mysql.ct",
                broker=app.config['CELERY_BROKER_URL'],
                include=['ct.ctask']
                )

celery.config_from_object("ct.celeryconfig")
platforms.C_FORCE_ROOT = True
# celery.conf.update(app.config)

logging.config.fileConfig("logger.conf")  # 采用配置文件
logger = logging.getLogger("log_output")


# app.debug = True
# app.processes = 10
# os.popen("celery -A mongo2mysql.celery worker --loglevel=info")


@app.route('/api/pid/<string:pid>_<int:skip>_<int:limit>')
def pid_action(pid, skip, limit):
    celery.send_task("ct.ctask.pid_action_task", args=[pid, limit, skip], queue="first_ct_queue2")
    return jsonify({"data": 'ok'})
    
@app.route('/api/spss_pid/<string:pid>_<int:skip>_<int:limit>')
def pid_action_spss(pid, skip, limit):
    celery.send_task("ct.ctask.pid_action_spss_task", args=[pid, limit, skip], queue="first_ct_queue2")
    return jsonify({"data": 'ok'})


@app.route('/api/pid/all_pid')
def all_pid_action():
    celery.send_task("ct.ctask.all_pid", args=[], queue="first_ct_queue2")
    return jsonify({"data": 'ok'})

@app.route('/api/aid/<string:aid>')
def aid_action(aid):
    celery.send_task("ct.ctask.aid_action_task", args=[aid], queue="first_ct_queue")
    # aid_action_task.apply_async(args=[aid])
    return jsonify({"data": 'ok'})
    
@app.route('/api/spss_aid/<string:aid>')
def aid_action_spss(aid):
    celery.send_task("ct.ctask.aid_action_spss_task", args=[aid], queue="first_ct_queue")
    # aid_action_task.apply_async(args=[aid])
    return jsonify({"data": 'ok'})


@app.route('/api_1/aid/<string:aid>')
def aid_action_o(aid):
    RequestAction().answers_action(aid)
    return jsonify({"data": 'ok'})


@app.route('/api_1/pid/<string:pid>_<int:limit>_<int:skip>')
def pid_action_o(pid, limit, skip):
    RequestAction().question_action(pid, limit, skip)
    return jsonify({"data": 'ok'})


@app.route('/celery/asyn_sum/<int:a>+<int:b>')
def celery_test(a, b):
    result = celery.send_task("ctask.add_togeth", args=[a, b], queue="first_ct_queue")
    while not result.ready():
        n += 1
        print n
        time.sleep(1)

    return "result: %s" % result.get()

@app.route('/topictest_xlliu')
def server_test():
    return "server ok"


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=4000)
