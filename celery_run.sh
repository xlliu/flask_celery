# nohup celery -A mongo2mysql.celery worker -c 2  --loglevel=info --logfile logs/celery_info.log
nohup celery -A mongo2mysql.celery worker -P eventlet -c 5 --loglevel=info --logfile logs/celery_info.log --pidfile celery_pid &
# nohup celery -A mongo2mysql.celery worker -n hotplay_default_worker -c 3 -Q hotplay_sh_default_queue -l info &
