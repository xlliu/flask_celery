# -*- coding: utf-8 -*-
# CELERY_BROKER_URL='redis://127.0.0.1:6379'
# CELERY_RESULT_BACKEND='redis://127.0.0.1:6379'
# CELERY_BROKER_URL = 'amqp://xlliu:zkey@120.131.64.225:5672/xlliuvhost'
CELERY_IGNORE_RESULT = True
CELERY_STORE_ERRORS_EVEN_IF_IGNORED = True

CELERYD_POOL_RESTARTS = True
CELERYD_PREFETCH_MULTIPLIER=5

# 每个worker最多执行万100个任务就会被销毁，可防止内存泄露
CELERYD_MAX_TASKS_PER_CHILD=100
CELERY_ACCEPT_CONTENT = ['json']

# 单个任务的运行时间不超过此值，否则会被SIGKILL 信号杀死  
CELERYD_TASK_TIME_LIMIT=3600 * 240

CELERY_TASK_SERIALIZER='json'
CELERY_TIMEZONE='Asia/Shanghai'
# CELERY_ENABLE_UTC=True
# CELERY_IMPORTS=("mongo2mysql")
# 任务发出后，经过一段时间还未收到acknowledge , 就将任务重新交给其他worker执行  
CELERY_DISABLE_RATE_LIMITS = True
# 非常重要,有些情况下可以防止死锁 
# CELERYD_FORCE_EXECV = True 
# 某个程序中出现的队列，在broker中不存在，则立刻创建它  
CELERY_CREATE_MISSING_QUEUES = True
# Enables error emails.
CELERY_SEND_TASK_ERROR_EMAILS = True
SEND_TASK_SENT_EVENT = True

BROKER_POOL_LIMIT = 10
BROKER_CONNECTION_MAX_RETRIES = 20

CELERY_REDIS_MAX_CONNECTIONS = 40


CELERY_QUEUES = {
    "default_dongwm": { # 这是上面指定的默认队列
        "exchange": "default_dongwm",
        "exchange_type": "direct",
        "routing_key": "default_dongwm"
    },
    "first_ct_queue": {
        "exchange": "first_ct_queue",
        "exchange_type": "direct",
        "routing_key": "first_ct_queue"
    },
    "first_ct_queue2": {
        "exchange": "first_ct_queue2",
        "exchange_type": "direct",
        "routing_key": "first_ct_queue2"
    },
    "topicqueue": { # 这是一个topic队列 凡是topictest开头的routing key都会被放到这个队列
        "routing_key": "topictest.#",
        "exchange": "topic_exchange",
        "exchange_type": "topic",
    },
    "test2": { # test和test2是2个fanout队列,注意他们的exchange相同
        "exchange": "broadcast_tasks",
        "exchange_type": "fanout",
        "binding_key": "broadcast_tasks",
    },
    "test": {
        "exchange": "broadcast_tasks",
        "exchange_type": "fanout",
        "binding_key": "broadcast_tasks2",
    },
}

BROKER_TRANSPORT_OPTIONS = {
    'fanout_prefix': True,
    'visibility_timeout': 0
}


ADMINS = (
    ('xlliu', 'liuxl@zkey.cc'),
)

# Email address used as sender (From field).
SERVER_EMAIL = 'liuxl@zkey.cc'
# Mailserver configuration
EMAIL_HOST = 'mail.zkey.cc'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'liuxl@zkey.cc'
EMAIL_HOST_PASSWORD = 'a4133545128'

# RabbitMQ management api
persistent=True
# db="flower_db"
broker="amqp://127.0.0.1:5672"
broker_api="http://127.0.0.1:55672/api/"
logging="info"
