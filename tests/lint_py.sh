#!/bin/bash

flake8 --format=pylint --max-line-length=120 --ignore=F403,E402,F401,W293 --builtins=_ \
$(find app/ -name '*.py' -print)