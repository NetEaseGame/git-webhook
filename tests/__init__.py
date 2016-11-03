# -*- coding: utf-8 -*-
import os
import logging

os.environ['GIT_WEBHOOK_CONFIG'] = 'config_test.py'
logging.basicConfig(level=logging.DEBUG)
