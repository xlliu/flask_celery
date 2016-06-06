# encoding: utf-8


"""
@version: ??
@author: xlliu
@contact: liu.xuelong@163.com
@site: https://github.com/xlliu
@software: PyCharm
@file: ctask.py
@time: 2016/5/3 13:59
"""
from __future__ import absolute_import
from mongo2mysql import celery
from server.request_context import RequestAction


@celery.task()
def add_togeth(a, b):
    return a + b


@celery.task()
def pid_action_task(pid, limit, skip):
    RequestAction().question_action(pid, limit, skip)
    return 'ok'


@celery.task()
def aid_action_task(aid):
    RequestAction().answers_action(aid)
    return 'ok'

@celery.task()
def all_pid():
    RequestAction().all_action()
    return "ok"
