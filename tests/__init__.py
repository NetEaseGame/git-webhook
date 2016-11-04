# -*- coding: utf-8 -*-
import os
import json
import logging

os.environ['GIT_WEBHOOK_CONFIG'] = 'config_test.py'
logging.basicConfig(level=logging.DEBUG)

TEST_DIR = os.path.dirname(__file__)
WEBHOOKDATA_DIR = os.path.join(TEST_DIR, 'webhookdata')
WEBHOOKDATA = {}
for filename in os.listdir(WEBHOOKDATA_DIR):
    name = os.path.splitext(filename)[0]
    with open(os.path.join(WEBHOOKDATA_DIR, filename)) as f:
        data = json.load(f)
    WEBHOOKDATA[name] = data
with open(os.path.join(TEST_DIR, '../ssh/id_rsa')) as f:
    RSA_PRIVATE_KEY = f.read()


def success(response):
    if response.status_code == 200:
        print(response.data)
        data = json.loads(response.data)
        return data['success']
    return False


def load_data(response):
    data = json.loads(response.data)
    return data['data']
