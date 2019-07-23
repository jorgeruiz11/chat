#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
File: server.py
Author: Jorge Ruiz.
'''

import sys
import socket
import pickle
import traceback
import threading

class Server(object):


    def __init__(self):
        self.total_connections = []

        HOST = 'localhost'
        PORT = 1235
        BUFF_SIZE = 2048

        print('Initializating server... \n')
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((HOST, PORT))
        print("Listenning on port: " + str(PORT))
        self.server_socket.listen(10)
        # La siguiente línea es necesaria para mandar una excepción si ya no se recive nada.
        self.server_socket.setblocking(False)

        accept_conn = threading.Thread(target=self.accept_connections)
        handle_conn = threading.Thread(target=self.handle_connections)

        accept_conn.daemon = True
        accept_conn.start()

        handle_conn.daemon = True
        handle_conn.start()


        check = True
        while check:
            msg = input("<Server> : ")
            if msg == 'DISCONNECT':
                self.server_socket.close()
                sys.exit(-1)
            else:
                pass


    def send_to_all(self, message, client):
        for c in self.total_connections:
            try:
                if c != client:
                    c.send(message)
            except:
                self.total_connections.remove(c)


    def accept_connections(self):
        print("accept_connections initialized")
        while True:
            try:
                conn, addr = self.server_socket.accept()
                conn.setblocking(False)
                self.total_connections.append(conn)
            except:
                pass


    def handle_connections(self):
        print("handle_connections initialized")
        while True:
            if len(self.total_connections) > 0:
                for c in self.total_connections:
                    try:
                        data = c.recv(2048)
                        if data:
                            self.send_to_all(data, c)
                    except:
                        pass



if __name__ == '__main__':
    s = Server()
#    s.create_server()
