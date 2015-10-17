import socket
import threading

class myThread (threading.Thread):
    def __init__(self, socket, address):
        self.socket = socket
        self.address = address[0]
        self.port = address[1]
        print("connection accepted with " + self.address)
    def run(self):
        self.socket.sendall("coucou".encode())



class server:
    def __init__(self, host, port):
        # create an INET, STREAMing socket
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # bind the socket to a public host, and a well-known port
        self.serversocket.bind((host, port))
        # become a server socket
        self.serversocket.listen(5)
    
    def accept(self):
        while True:
            # accept connections from outside
            (clientsocket, address) = self.serversocket.accept()
            # now do something with the clientsocket
            # in this case, we'll pretend this is a threaded server
            ct = myThread(clientsocket, address)
            ct.run()


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
