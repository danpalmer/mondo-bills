web: gunicorn bills.wsgi --log-file -
worker: celery --without-gossip --without-mingle --without-heartbeat --app=bills worker -l info
