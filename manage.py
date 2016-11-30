# -*- coding: utf-8 -*-
'''
Created on 2016-11-23

@author: hustcc
'''

import subprocess
import sys
from flask_script import Manager, Command, Server as _Server, Option
from app import SQLAlchemyDB as db, socketio, app, __version__
import os
import shutil


manager = Manager(app)


class Server(_Server):
    help = description = 'Runs the Git-WebHook web server'

    def get_options(self):
        options = (
            Option('-h', '--host',
                   dest='host',
                   default='0.0.0.0'),
            Option('-p', '--port',
                   dest='port',
                   type=int,
                   default=18340),
            Option('-d', '--debug',
                   action='store_true',
                   dest='use_debugger',
                   help=('enable the Werkzeug debugger (DO NOT use in '
                         'production code)'),
                   default=self.use_debugger),
            Option('-D', '--no-debug',
                   action='store_false',
                   dest='use_debugger',
                   help='disable the Werkzeug debugger',
                   default=self.use_debugger),
            Option('-r', '--reload',
                   action='store_true',
                   dest='use_reloader',
                   help=('monitor Python files for changes (not 100%% safe '
                         'for production use)'),
                   default=self.use_reloader),
            Option('-R', '--no-reload',
                   action='store_false',
                   dest='use_reloader',
                   help='do not monitor Python files for changes',
                   default=self.use_reloader),
        )
        return options

    def __call__(self, app, host, port, use_debugger, use_reloader):
        # override the default runserver command to start a Socket.IO server
        if use_debugger is None:
            use_debugger = app.debug
            if use_debugger is None:
                use_debugger = True
        if use_reloader is None:
            use_reloader = app.debug
        import eventlet
        # monkey_patch
        eventlet.monkey_patch()

        socketio.run(app,
                     host=host,
                     port=port,
                     debug=use_debugger,
                     use_reloader=use_reloader,
                     **self.server_options)


manager.add_command("runserver", Server())


class CeleryWorker(Command):
    """Starts the celery worker."""
    name = 'celery'
    capture_all_args = True

    def run(self, argv):
        cmd = ['celery', '-A', 'app.celeryInstance', 'worker'] + argv
        ret = subprocess.call(cmd)
        sys.exit(ret)


manager.add_command("celery", CeleryWorker())


class Config(Command):
    """Generates new configuration file into user Home dir."""
    name = 'config'
    capture_all_args = True

    def run(self, argv):
        dir = os.path.join(os.path.expanduser('~'), '.git-webhook')
        if not os.path.exists(dir):
            os.makedirs(dir)
        # default dir is user HOME
#         if argv and len(argv) > 0:
#             dir = argv[0]
        # copy app/git_webhook_config.py into dir
        if os.path.isdir(dir):
            path = os.path.join(dir, 'git_webhook_config.py')
            if os.path.exists(path):
                print('Fail: the configuration file exist in `%s`.' % path)
            else:
                shutil.copy('app/config_example.py', path)
                print('OK: init configuration file into `%s`.' % path)
        else:
            print('Fail: %s should be directory.' % dir)


manager.add_command("config", Config())


@manager.command
def createdb(drop_first=False):
    """Creates the database."""
    if drop_first:
        db.drop_all()
    db.create_all()
    print('OK: database is initialed.')


@manager.command
def lint():
    """Runs code linter."""
    lint = subprocess.call(['flake8']) == 0
    if lint:
        print('OK')
    sys.exit(lint)


@manager.command
def version():
    "Shows the version"
    print __version__


# script entry
def run():
    manager.run()


if __name__ == '__main__':
    manager.run()
