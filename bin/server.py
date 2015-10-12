#! /usr/bin/env python3

import socket
import sys
from threading import Thread
from binascii import hexlify
#from thread import start_new_thread

class DisplaySocket(Thread):

    def __init__(self,param_conn):
        Thread.__init__(self)
        self.sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sparam=param_conn
    def run(self):
        self.sock.connect(self.sparam)
        while True:
            try:
                print(str(self.sock.recv(8192)))
            except socket.error as e:
                print(e)

class ClientThread(Thread):
 
    def __init__(self,conn,ssh_socket):
        Thread.__init__(self)
        self.conn = conn
        self.ssh=ssh_socket
        
        self.sock=SSHOutputRedirectThread(conn,ssh_socket).start()
    
    def run(self):
        #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Sending message to connected client
        # send only takes string
        # self.conn.send(bytes('Welcome to the server. Type something and hit enter\n','utf-8'))
        

        
        # infinite loop so that function do not terminate and thread do not end.
        while True:
            # Receiving from client
            data = self.conn.recv(8192)
            
            """idx=data.find(b'\r\n\r\n')
            print("idx ="+str(idx))
            if idx == -1:
                headers = ""
                content = data
            else:
                headers=data[:idx]
                content=date[idx+4:]
            """       
            
            print("data="+str(data))
            
            self.ssh.sendall(data)
            #reply = s.recv(8192)        
            #reply = bytes('OK...','ascii') + data
            
            if not data:
                break
            #self.conn.sendall(reply)
        # came out of loop
        self.conn.close()


#redirect ssh output to a sock
class SSHOutputRedirectThread(Thread):
    def __init__(self, sock ,ssh_socket):
        Thread.__init__(self)
        self.sock=sock
        self.ssh=ssh_socket

    def run(self):

        while True:
            try:
                data=self.ssh.recv(8192)
                print("data="+str(data))
                self.sock.sendall(data)
            except error as e :
                print(str(e))





class SSHInputRedirectThread(Thread):

    def __init__(self,param_conn):
        Thread.__init__(self)
        self.sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sparam=param_conn
        self.ssh=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ssh.connect(('localhost',22))

    def run(self):
        self.sock.connect(self.sparam)

        while True:
            try:
                data=self.sock.recv(8192)
                self.ssh.sendall(data)
            except error as e :
                self.ssh.close()
                print(str(e))


def wait_conn(sock,ssh_socket):
    # Start listening on socket
    sock.listen(10)

    print('Socket now listening')
    # Function for handling connections. This will be used to create threads
    # now keep talking with the client
    while 1:
        # wait to accept a connection - blocking call
        conn, addr = sock.accept()
        

        print('Connected with ' + addr[0] + ':' + str(addr[1]))
        # start new thread takes 1st argument as a function name to be run,
        # second is the tuple of arguments to the function.
        ClientThread(conn,ssh_socket).start()
        #start_new_thread(clientthread, (conn,))
    s.close()


def main2():
    port=8888
    
    ssh_sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssh_sock.connect(("localhost",22))
    

    HOST = ''    # Symbolic name meaning all available interfaces
    PORT = port  # Arbitrary non-privileged port
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Socket created')
    # Bind socket to local host and port
    try:
        sock.bind((HOST, PORT))
    except socket.error as msg:
        print('Bind failed. Error Code : ' +
              str(msg[0]) + ' Message ' + str(msg[1]))
        sys.exit()
    print('Socket bind complete')
    
    

    wait_conn(sock,ssh_sock)
    #SSHInputRedirectThread(param_conn).start()

# This is a Python's special:
# The only way to tell wether we are running the program as a binary,
# or if it was imported as a module is to check the content of
# __name__.
# If it is `__main__`, then we are running the program
# standalone, and we run the main() function.
if __name__ == "__main__":
    main2()
