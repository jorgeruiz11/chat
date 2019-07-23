#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
File: client.py
Author: Jorge Ruiz.
'''

import sys
import socket
import pickle
import threading

class Client(object):

    HOST = 'localhost'
    PORT = 1234
    BUFF_SIZE = 2048


    def __init__(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect(("localhost", 1235))
        except:
            print("Connection error")
            sys.exit(-1)

        recv_msg = threading.Thread(target=self.recived_message)
        recv_msg.daemon = True
        recv_msg.start()

        isTrue = True
        while isTrue:
            msg = input("<You> : ")
            if msg != 'DISCONNECT':
                self.send_msg(msg)
            else:
                self.client_socket.close()
                sys.exit(-1)


    def recived_message(self):
        while True:
            try:
                data = self.client_socket.recv(2048)
                if data:
                    print(pickle.loads(data))
            except:
                pass


    def send_msg(self, msg):
        self.client_socket.send(pickle.dumps(msg))



if __name__ == '__main__':
    c = Client()
    #c.connect_to_server()
    #c.handle_client()
    #c.recived_message()
