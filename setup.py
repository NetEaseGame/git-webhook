# -*- coding: utf-8 -*-
'''
Created on 2016-11-30

@author: hustcc
'''
from distutils.core import setup
from setuptools import find_packages
from app import __version__


LONGDOC = """
git-webhook is a web app base on
    Python Flask + SQLAchemy + Celery + Redis + React.

Aims to deploy a git webhook platform easily,
    now supports  Github / GitLab / Gogs / GitOsc

How to deploy & run ?

pip install git-webhook

1. gitwebhook config : will init config into HOME dir

2. gitwebhook runserver : run web server, with default port 18340

2. gitwebhook celery

then visit ip:18340
"""


setup(name='git-webhook',
      version=__version__,
      description=(u'使用 Python Flask + SQLAchemy + Celery + Redis + React '
                   u'开发的用于迅速搭建并使用 WebHook '
                   u'进行自动化部署和运维，'
                   u'支持 Github / GitLab / Gogs / GitOsc。'),
      long_description=LONGDOC,
      author='hustcc',
      author_email='vip@hust.edu.cn',
      url='https://github.com/hustcc',
      license='MIT',
      install_requires=[
        'flask==0.11.1',
        'flask-sqlalchemy==2.1',
        'pymysql==0.7.9',
        'jinja2==2.8',
        'github-flask==3.1.3',
        'eventlet==0.19.0',
        'paramiko==2.0.2',
        'celery==3.1.24',
        'redis==2.10.5',
        'schema==0.6.5',
        'validators==0.11.0',
        'flask-socketio==2.7.2',
        'Flask-Script==2.0.5',
      ],
      classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Natural Language :: Chinese (Simplified)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development'
        'Topic :: Utilities'
      ],
      keywords='git, webhook, ci, GitHub, GitLab, Gogs, GitOsc',
      packages=find_packages('app'),
      package_dir={'': 'app'},
      entry_points={
        'console_scripts': ['gitwebhook=manage:run']
      })
