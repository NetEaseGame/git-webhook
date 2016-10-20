# -*- coding: utf-8 -*-
'''
Created on 2016-10-20

@author: hustcc
'''
from app import app
from app.utils import ResponseUtil, RequestUtil
from app.tasks import tasks


@app.route('/api/git-webhook/<key>', methods=['POST'])
def api_for_webhook(key):
    '''git hook data
    '''
    try:
        data = RequestUtil.get_parameter(request, 'hook', None)
        if data == None:
            data = request.data

        data = json.loads(data)
        webhook = WebHook.query.filter_by(key=key).first()
        if webhook:
            tasks.do_webhook_shell(webhook.dict(), data)
            return "Work put into Queue."
        else:
            # 
            return "The webhook is expired."
        os.system('ls')
        
        
        
    except:
        return "Request is not valid."
