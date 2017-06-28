'''
Created on 2017. 6. 28.

@author: chiwon.choi


@ error : 소켓 에러

server listening to port: 8800
[WinError 10038] 소켓 이외의 개체에 작업을 시도했습니다

=> 윈도우 환경에서만 오류가 납니다. 
   connection_list = [sys.stdin, clientSocket] 코드는 window o/s 에서 sys.stdin 을 socket 으로 오픈할수 없어서 오류가 발생합니다. 
      임시적으로 connection_list = [clientSocket] 로 접속하면 되지만 키보드 입력은 안됩니다. 
   sys.stdin은 분리해서 처리 해야할 것 같네요

'''

#coding=utf-8

import select
import socket
import sys
import signal

# python 2.7
#import cPickle

# python 3.5
import _pickle as cPickle

import struct
import argparse

from sys import stdin



SERVER_HOST = 'localhost'
CHAT_SERVER_NAME = 'server'

# some utilities
def send(channel, *args):
    buffer = cPickle.dumps(args)
    value = socket.htonl(len(buffer))
    size = struct.pack("L", value)
    channel.send(size)
    channel.send(buffer)
    
def receive(channel):
    size = struct.calcsize("L")
    size = channel.recv(size)
    
    try:
        size = socket.htonl(struct.unpack("L", size)[0])
    except struct.error as e:
        return ''
    
    buf = ""
    while len(buf) < size:
        buf = channel.recv(size - len(buf))
        
    return cPickle.loads(buf)[0]
    
    
class ChatServer(object):
    """ an example chat server using select """
    
    def __init__(self, port, backlog=5):
        self.clients = 0
        self.clientmap = {}
        self.outputs = [] # list output sockets
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((SERVER_HOST, port))
        
        print("server listening to port: %s" %port)
        self.server.listen(backlog)
        
        # catch keyboard interrupts
        signal.signal(signal.SIGINT, self.sighandler)
        
    def sighandler(self, signum, frame):
        """ clean up client outputs"""
        
        # close the server
        print("shutting down server...")
        
        # close existing client sockets
        for output in self.outputs:
            output.close()
            
        self.server.close()
        
    def get_client_name(self, client):
        """ return the name of the client """
        
        info = self.clientmap[client]
        host, name = info[0][0], info[1]
        return '@'.join((name, host))
    
    def run(self):
        inputs = [self.server, sys.stdin]
        self.outputs = []
        running = True
        
        while running:
            try:
                readable, writeable, exceptional = select.select(inputs, self.outputs, [])
            except select.error as e:
                print(e)
                break
            
            for sock in readable:
                if sock == self.server:
                    # handle the server socket
                    client, address = self.server.accept()
                    print("chat server: got connection %d from %s" %(client.fileno(), address))
                    
                    #read the login name
                    cname = receive(client).split('NAME: ')[1]
                    
                    # compute client name and send back
                    self.clients += 1
                    send(client, 'Client : ' + str(address[0]))
                    inputs.append(client)
                    self.clientmap[client] = (address, cname)
                    
                    # send joining information to other clients
                    msg = "\n(Connected: New client (%d) from %s)" %(self.clients, self.get_client_name(client))
                    
                    for output in self.outputs:
                        send(output, msg)
                        
                    self.outputs.append(client)
                    
                elif sock == sys.stdin:
                    # handle standard input
                    junk = sys.stdin.readline()
                    running = False
                    
                else:
                    # handle all other sockets
                    try:
                        data = receive(sock)
                        if data:
                            # send as new clients's message...
                            msg = '\n#[' + self.get_client_name(sock) + ']>>' + data
                            
                            # send data to all except ourself
                            for output in self.outputs:
                                if output != sock:
                                    send(output, msg)
                                    
                        else:
                            print("chat server: %d hung up" %sock.fileno())
                            self.clients -= 1
                            sock.close()
                            inputs.remove(sock)
                            self.outputs.remove(sock)
                            
                            # sending client leaving information to others
                            msg = "\n(Now hung up: Client from %s)" % self.get_client_name(sock)
                            for output in self.outputs:
                                send(output, msg)
                                
                    except socket.error as e:
                        print("except! %s" %e)
                        # remove
                        inputs.remove(sock)
                        self.outputs.remove(sock)
                        
        self.server.close()                
                    
   
class ChatClient(object):
    """ a command line chat client using select """
    
    def __init__(self, name, port, host=SERVER_HOST):
        self.name = name
        self.connected = False
        self.host = host
        self.port = port
        
        # initial prompt
        self.prompt='[' + '@'.join((name, socket.gethostname().split('.')[0])) + ']> '
        
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((host, self.port))
            
            print("Now connected to chat server@ port %d" %self.port)
            self.connected = True
            
            # send my name...
            send(self.sock,'NAME: ' + self.name) 
            data = receive(self.sock)
            
            # contains client address, set it
            #addr = data.split('CLIENT: ')[1]
            addr = data.split('CLIENT: ')[0]
            
            
            self.prompt = '[' + '@'.join((self.name, addr)) + ']> '
            
        except socket.error as e:
            print("Failed to connect to chat server @ port %d" %self.port)
            sys.exit(1)

    def run(self):
        """ Chat client main loop """
        
        while self.connected:
            try:
                sys.stdout.write(self.prompt)
                sys.stdout.flush()
                
                # Wait for input from stdin and socket
                #readable, writeable,exceptional = select.select([0, self.sock], [],[])
                readable, writeable,exceptional = select.select([self.sock], [],[])
                
                
                for sock in readable:
                    if sock == 0:
                        data = sys.stdin.readline().strip()
                        #data = "hello client!"
                        if data: send(self.sock, data)
                    elif sock == self.sock:
                        data = receive(self.sock)
                        if not data:
                            print('Client shutting down.')
                            self.connected = False 
                            break
                        else:
                            sys.stdout.write(data + '\n')
                            sys.stdout.flush()
                            
            except KeyboardInterrupt:
                print (" Client interrupted. ")
                self.sock.close()
                break


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Socket Server Example with Select')
    parser.add_argument('--name', action="store", dest="name", required=True)
    parser.add_argument('--port', action="store", dest="port", type=int, required=True)
    given_args = parser.parse_args() 
    port = given_args.port
    name = given_args.name


    client = ChatClient(name=name, port=port)
    client.run()        

    '''
    if name == CHAT_SERVER_NAME:
        server = ChatServer(port)
        server.run()
    else:
        client = ChatClient(name=name, port=port)
        client.run()        
    '''




