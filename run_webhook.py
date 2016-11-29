# -*- coding: utf-8 -*-
'''
Created on 2016年10月20日

@author: hustcc
'''


from app import app, socketio

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=18340)
