FROM python:2.7

COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt -i https://pypi.douban.com/simple && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
WORKDIR /code
CMD mkdir -p /data && \
    python manage.py celery --loglevel=info --logfile=/data/celery.log --pidfile=/run/celery.pid --detach && \
    gunicorn -P -b 0.0.0.0:80 -k eventlet -w 1 --log-file=/data/gunicorn.log manage:app
