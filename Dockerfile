FROM python:2.7
RUN pip install gunicorn -i https://pypi.douban.com/simple
COPY . /code
WORKDIR /code
RUN pip install -r requirements.txt -i https://pypi.douban.com/simple
CMD mkdir -p /data && \
    celery -A app.celeryInstance worker --loglevel=info --detach && \
    gunicorn -c gunicorn.cfg run_webhook:app
