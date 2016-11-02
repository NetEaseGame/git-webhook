FROM python:2.7
COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt -i https://pypi.douban.com/simple
WORKDIR /code
CMD mkdir -p /data && \
    celery -A app.celeryInstance worker --loglevel=info --logfile=/data/celery.log --pidfile=/data/celery.pid --detach && \
    gunicorn -b 0.0.0.0:80 -w 5 -k gevent --log-file=/data/gunicorn.log run_webhook:app
