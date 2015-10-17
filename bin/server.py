import socket
import threading
import time

class myThread (threading.Thread):
    def __init__(self, socket, address):
        """
        Initialise the variables needed to communicate
        """
        self.socket = socket
        self.address = address[0]
        self.port = address[1]
        print("connection accepted with " + self.address)

    def run(self):
        self.communicate()
    
    def receive(self):
        """
        Try to receive a connection. 
        Return False if there is the connection has to be closed (if it receives no data)
        """
        data = self.socket.recv(1024)
        if not data:
            return False
        else:
            print("received data : " + data.decode())
            return data
    
    def send(self, data):
        """
        Sends a data string
        If the connection is closed, close the connection
        """
        self.socket.sendall(data.encode())
        print("sent " + str(data))
        time.sleep(0.1)
        


    def communicate(self):
        """
        Sends the reply
        Waits for other connections and sends the reply
        If the connection is closed, stops the loop
        """
        tok = 1
        self.socket.sendall(str(tok).encode())
        while True:
            tok += 1
            data = self.receive() 
            if data == False: break
            print("received data " + data.decode())
            self.send(str(tok))
            


class server:
    def __init__(self, host, port):
        # create an INET, STREAMing socket
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # bind the socket to a public host, and a well-known port
        self.serversocket.bind((host, port))
        # become a server socket
        self.serversocket.listen(5)
    
    def accept(self):
        """
        Waits for a connection on the socket
        When a connection has been made, starts a new thread
        """
        while True:
            # accept connections from outside
            (clientsocket, address) = self.serversocket.accept()
            # now do something with the clientsocket
            # in this case, we'll pretend this is a threaded server
            
            try:
                ct = myThread(clientsocket, address)
                ct.run()
            except socket.error as e:
                print("socket broken. Closing the connection")
                ct.close()


if __name__ == "__main__":
    HOST = ""
    PORT = 80
    serv = server(HOST, PORT)
    serv.accept()









"""
import socketserver, subprocess, sys
from threading import Thread
import time


def handle(self):
    # self.request is the client connection
    data = self.request.recv(1024)  # clip input at 1Kb
    self.request.send(reply)
    self.request.close()


class SingleTCPHandler(socketserver.BaseRequestHandler):
    "One instance per connection.  Override handle(self) to customize action."
    def handle(self):
        while True:
            # self.request is the client connection
            data = self.request.recv(1024)  # clip input at 1Kb
            print("received " + data.decode())
            self.request.send("coucou".encode())
            self.request.close()
            time.sleep(0.1)

class SimpleServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    # Ctrl-C will cleanly kill all spawned threads
    daemon_threads = True
    # much faster rebinding
    allow_reuse_address = True

    def __init__(self, server_address, RequestHandlerClass):
        socketserver.TCPServer.__init__(self, server_address, RequestHandlerClass)




if __name__ == "__main__":
    HOST = ""
    PORT = 80
    server = SimpleServer((HOST, PORT), SingleTCPHandler)
    # terminate with Ctrl-C
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        sys.exit(0)    # Create the server, binding to localhost on port 9999
    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
"""
