#! /usr/bin/env python3
import socket   # for sockets
import sys
import threading
import time
hardReturn = "\r\n"


"""
SERVER
"""


class myThread (threading.Thread):
    def __init__(self, socket, address):
        """
        Initialise the variables needed to communicate
        """
        self.socket = socket
        self.address = address[0]
        self.port = address[1]
        print("connection accepted with " + self.address)

    def log(self, message):
        print("[server] " + message)

    def run(self):
        self.communicate()

    def receive(self):
        """
        Try to receive a connection.
        Return False if there is the connection has to be closed
        (if it receives no data)
        """
        data = self.socket.recv(1024)
        if not data:
            return False
        else:
            self.log("received data : " + data.decode())
            return data

    def send(self, data):
        """
        Sends a data string
        If the connection is closed, close the connection
        """
        self.socket.sendall(data.encode())
        self.log("sent " + str(data))
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
            if data is False:
                break
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
            except KeyboardInterrupt:
                print("socket broken. Closing the connection")
                clientsocket.close()


"""
CLIENT
"""


class client:
    def __init__(self, host, port, debug=False):
        self.host = host
        self.port = port
        self.debug = debug

    def initConnection(self):
        self.initSocket()
        self.getHostName()
        self.connectToHost()

    def initSocket(self):
        """
        Initialise une socket
        """
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error:
            print('Failed to create socket')
            sys.exit()
        print('Socket Created')

    def getHostName(self):
        """
        Get the ip address of the host.
        """
        try:
            self.remote_ip = socket.gethostbyname(self.host)
            print("Host " + self.host + " is on ip " + self.remote_ip)
        except socket.gaierror:
            # could not resolve
            print('Hostname could not be resolved. Exiting')
            sys.exit()

    def connectToHost(self):
        """
        Connect to the remote host
        """
        self.s.connect((self.remote_ip, self.port))
        print('Socket Connected to ' + self.host + ' on ip ' + self.remote_ip)

    def sendPacket(self, packet):
        """
        Takes a packet as a string
        Sends a packet
        Return : error if the packet could not be sent
        """
        try:
            # Set the whole string
            print(packet.encode())
            self.s.sendall(packet.encode())
        except socket.error:
            # Send failed
            print('Send failed')
            sys.exit()

    def receivePacket(self):
        """
        Receive a packet
        """
        return self.s.recv(4096)

    def close(self):
        """
        Close the socket
        """
        self.s.close()


class httpPacket:
    def __init__(self, host):
        """
        Set the typical header
        """
        self.header = (
            "Content-type: application/octet-stream" + hardReturn
            + "Transfer-Encoding: chunked" + hardReturn
            + "Proxy-Connection: ")
        self.GETHeader = (
            "GET /cgi-bin/test.py"
            + " HTTP/1.1" + hardReturn
            + "Connection: keep-alive" + hardReturn
            + "Cache-Control: no-cache" + hardReturn)
        self.OK200Header = (
            "HTTP/1.1 200 OK" + hardReturn)
        self.data = ""
        self.contentLength = ""
        self.host = "Host: " + host + hardReturn

    def setCookie(self, token):
        """
        Sets a cookie. Has to be a digit
        """
        self.header += "Set-Cookie: tok=" + str(token) + hardReturn

    def setData(self, data):
        """
        Sets the data to send
        Sets the length of the data
        """
        self.data = data
        self.setContentLength()

    def setContentLength(self):
        self.contentLength = "Content-length: " + str(
            len(self.data)) + hardReturn

    def getGETPacket(self):
        """
        Constructs the http packet to send
        """
        packet = self.GETHeader + self.host + hardReturn
        return packet

    def getOkPacket(self):
        packet = self.OK200Header + hardReturn
        return packet


def test():
    print("test")


def main():
    packet = httpPacket()
    packet.setCookie(1234)
    packet.setData("salut tout le monde")
    print(packet.getGETPacket())

# This is a Python's special:
# The only way to tell wether we are running the program as a binary,
# or if it was imported as a module is to check the content of
# __name__.
# If it is `__main__`, then we are running the program
# standalone, and we run the main() function.
if __name__ == "__main__":
    main()
