# -*- coding: utf-8 -*-
'''
Created on 2016-10-20

@author: hustcc
'''
from app.wraps.login_wrap import login_required
from app import app
from app.utils import ResponseUtil, RequestUtil
from app.database.model import History

# get history list
@app.route('/api/history/list', methods=['GET'])
@login_required()
def api_history_list():
    # login user
    user_id = RequestUtil.get_login_user().get('id', '')
    
    webhook_id = RequestUtil.get_parameter('webhook_id', '')
    page = RequestUtil.get_parameter('page', '1')
    try:
        page = int(page)
        if page < 1:
            page = 1
    except:
        page = 1

    page_size = 25
    paginations = History.query.order_by(History.id.desc()).paginate(page, page_size, error_out=False)
    
    histories = paginations.items
    histories = [history.dict() for history in histories]
    
    
    data = {
        'histories': histories,
        'has_prev': paginations.has_prev,
        'has_next': paginations.has_next,
        'page': paginations.page
    }
    
    return ResponseUtil.standard_response(1, histories)