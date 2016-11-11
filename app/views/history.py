# -*- coding: utf-8 -*-
'''
Created on 2016-10-20

@author: hustcc
'''
from app.wraps.login_wrap import login_required
from app import app
from app.utils import ResponseUtil, RequestUtil, AuthUtil
from app.database.model import History, WebHook


# get history list
@app.route('/api/history/list', methods=['GET'])
@login_required()
def api_history_list():
    # login user
    user_id = RequestUtil.get_login_user().get('id', '')

    webhook_id = RequestUtil.get_parameter('webhook_id', '')

    if not AuthUtil.has_readonly_auth(user_id, webhook_id):
        return ResponseUtil.standard_response(0, 'Permission deny!')

    page = RequestUtil.get_parameter('page', '1')
    try:
        page = int(page)
        if page < 1:
            page = 1
    except:
        page = 1

    page_size = 25
    paginations = History.query\
        .filter_by(webhook_id=webhook_id)\
        .order_by(History.id.desc())\
        .paginate(page, page_size, error_out=False)

    histories = [history.dict() for history in paginations.items]

    data = {
        'histories': histories,
        'has_prev': paginations.has_prev,
        'has_next': paginations.has_next,
        'page': paginations.page
    }

    return ResponseUtil.standard_response(1, data)
