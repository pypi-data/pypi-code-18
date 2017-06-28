'''
Created on 2017. 6. 28.

@author: chiwon.choi
'''

import os
import socket
import threading
import socketserver


SERVER_HOST = 'localhost'
SERVER_POR = 0 # tells the kernel to pickup a port dynamically
BUF_SIZE = 1024


def client(ip, port, message):
    """ a client to test threading mixin server"""
    
    # connecto to the server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    
    try:
        sock.sendall(message)
        response = sock.recv(BUF_SIZE)
        print("client received: %s" %response)
    finally:
        sock.close()
    
    
class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    """an example of threaded TCP request handler """
    
    def handle(self):
        #socketserver.BaseRequestHandler.handle(self)
        data = self.request.recv(1024)
        cur_thread = threading.current_thread()
        response = "%s: %s" %(cur_thread.name, data)
        
        # python 2.7
        #self.request.sendall(response)
        
        # python 3.5
        msg = bytes(response, 'utf-8')
        self.request.sendall(msg)
        
        
class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """nothing to add here, inherited everything necessary from parents"""
    pass


if __name__ == "__main__":
    # run server
    server = ThreadedTCPServer((SERVER_HOST, SERVER_POR), ThreadedTCPRequestHandler)
    ip, port = server.server_address # retrieve ip address
    
    # start a thread with the server -- one thread per request
    server_thread = threading.Thread(target=server.serve_forever)
    
    # exit the server thread when the main thread exits
    server_thread.daemon = True
    server_thread.start()
    print("server loop running on thread: %s" %server_thread.name)
    
    # run clients
    
    # python 2.7
    #client(ip, port, "hello from client 1")
    #client(ip, port, "hello from client 2")
    #client(ip, port, "hello from client 3")
    
    # python 3.5
    client(ip, port, bytes("hello from client 1", 'utf-8'))
    client(ip, port, bytes("hello from client 2", 'utf-8'))
    client(ip, port, bytes("hello from client 3", 'utf-8'))
    
    # server cleanup
    server.shutdown()
    






