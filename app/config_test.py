# -*- coding: utf-8 -*-
DEBUG = True
TESTING = True
SECRET_KEY = 'SECRET_KEY'
DATABASE_URI = 'mysql+pymysql://root:root@127.0.0.1/git_webhook'

CELERY_BROKER_URL = 'redis://:@127.0.0.1:6379/0'
CELERY_RESULT_BACKEND = 'redis://:@127.0.0.1:6379/0'

SOCKET_MESSAGE_QUEUE = 'redis://:@127.0.0.1:6379/0'

GITHUB_CLIENT_ID = '123'
GITHUB_CLIENT_SECRET = 'SECRET'
