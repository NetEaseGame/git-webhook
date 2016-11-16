# -*- coding: utf-8 -*-
'''
Created on 2016年10月20日

@author: hustcc
'''


from app import app, socket

if __name__ == '__main__':
    socket.run(app, host='0.0.0.0', port=18340, debug=True)
