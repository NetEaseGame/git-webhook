# -*- coding: utf-8 -*-
import os
import json
import logging

os.environ['GIT_WEBHOOK_CONFIG'] = 'config_test.py'
logging.basicConfig(level=logging.DEBUG)

WEBHOOKDATA_DIR = os.path.join(os.path.dirname(__file__), 'webhookdata')
WEBHOOKDATA = {}
for filename in os.listdir(WEBHOOKDATA_DIR):
    name = os.path.splitext(filename)[0]
    with open(os.path.join(WEBHOOKDATA_DIR, filename)) as f:
        data = json.load(f)
    WEBHOOKDATA[name] = data


def success(response):
    if response.status_code == 200:
        print(response.data)
        data = json.loads(response.data)
        return data['success']
    return False


def load_data(response):
    data = json.loads(response.data)
    return data['data']
