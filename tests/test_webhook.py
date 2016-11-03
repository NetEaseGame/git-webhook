# -*- coding: utf-8 -*-
import os
import json
from app.utils.HookDataParse import (
    get_repo_name,
    get_repo_branch,
    get_push_name,
    get_push_email
)

WEBHOOKDATA_DIR = os.path.join(os.path.dirname(__file__), 'webhookdata')
WEBHOOKDATA = {}
for filename in os.listdir(WEBHOOKDATA_DIR):
    name = os.path.splitext(filename)[0]
    with open(os.path.join(WEBHOOKDATA_DIR, filename)) as f:
        data = json.load(f)
    WEBHOOKDATA[name] = data


def test():
    for name, data in WEBHOOKDATA.items():
        print('\n' + name.center(60, '-'))
        print(get_repo_name(data))
        print(get_repo_branch(data))
        print(get_push_name(data))
        print(get_push_email(data))
