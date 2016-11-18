# -*- coding: utf-8 -*-
'''
Created on 2016-10-20

index, login, logout
@author: hustcc
'''

from app import app, github, __version__
from app.utils import ResponseUtil, RequestUtil, DateUtil
from werkzeug.utils import redirect
from flask.helpers import url_for, flash
from flask.globals import session
from app.database.model import User


@app.route('/', methods=['GET'])
def index():
    return ResponseUtil.render_template('index.html', __version__=__version__)


@app.route('/login', methods=['GET'])
def login():
    return github.authorize()


@github.access_token_getter
def token_getter():
    return session.get('oauth_token', None)


@app.route('/github/callback')
@github.authorized_handler
def github_authorized(oauth_token):
    if oauth_token is None:
        flash("Authorization failed.")
        return redirect(url_for('index'))

    session['oauth_token'] = oauth_token

    me = github.get('user')
    user_id = me['login']

    # is user exist
    user = User.query.get(user_id)

    if user is None:
        # not exist, add
        user = User(id=user_id)

    # update github user information
    user.last_login = DateUtil.now_datetime()
    user.name = me.get('name', user_id)
    user.location = me.get('location', '')
    user.avatar = me.get('avatar_url', '')

    user.save()

    RequestUtil.login_user(user.dict())

    return redirect(url_for('index'))


@app.route('/logout', methods=['GET'])
def logout():
    RequestUtil.logout()
    return redirect(url_for('index'))
