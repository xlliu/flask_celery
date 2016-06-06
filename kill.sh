kill -9 `ps -ef | grep 'celery -A mongo2mysql.celery worker'| grep -v grep | awk '{print $2}'` `ps -ef | grep 'python tornado_ct_server'| grep -v grep | awk '{print $2}'`
