# -*- coding: utf-8 -*-
'''
Created on 2016年10月20日

@author: hustcc
'''


from app import app

if __name__ == '__main__':
    app.run('0.0.0.0', 18340, debug=True,  threaded=True)