#! /usr/bin/env python3
import socket   # for sockets
import sys
import threading
import time
hardReturn = "\r\n"


class tunnel:
    """
    Maison : "vps205524.ovh.net 8001 80"
    Entreprise : "localhost 80 22"
    """
    def __init__(self, host, portIn, portOut):
        self.host = host
        self.portIn = portIn
        self.portOut = portOut

    def init(self):
        incoming_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        incoming_connection.bind(("", self.portIn))
        # become a server socket
        incoming_connection.listen(5)
        # accept connections from outside
        (incoming_socket, address) = incoming_connection.accept()
        print("connection ssh created")
        data = incoming_socket.recv(1024)
        print("ssh data = " + data.decode())
        outgoing_connection = client(self.host, self.portOut)
        outgoing_connection.initConnection()
        sshToHttp(
            incoming_socket, outgoing_connection.getSocket(), data).start()

        data = incoming_socket.recv(1024)
        if data:
            sshToHttp(
                outgoing_connection.getSocket(), incoming_socket, data).start()


class sshToHttp(threading.Thread):
    """
    Redirects the connections from ssh client to outgoing_connection
    """
    def __init__(self, outgoing_connection, incoming_connection, first_data):
        threading.Thread.__init__(self)
        self.incoming_connection = incoming_connection
        self.outgoing_connection = outgoing_connection
        print("[SSHRedirectToHTTP] send first message = " + str(first_data))
        self.incoming_connection.sendall(first_data)

    def run(self):
        """
        Récupère le flux ssh et le renvoit au serveur
        """
        while True:
            # Receiving from ssh
            print("[SSHRedirectToHTTP] waiting for data to receive")
            data = self.incoming_connection.recv(1024)
            if data:
                print("[SSHRedirectToHTTP] recv")
                print("[SSHRedirectToHTTP] dataSSH = " + str(data))
                try:
                    print("[SSHRedirectToHTTP] sendall")
                    time.sleep(0.01)
                    self.outgoing_connection.sendall(data)
                except socket.error as e:
                    print(e)
                    break
            else:
                break
        self.incoming_connection.close()

"""
CLIENT
"""


class client:
    def __init__(self, host, port, debug=False):
        self.host = host
        self.port = port
        self.debug = debug

    def log(self, message):
        print("[client] " + message)

    def initConnection(self):
        self.initSocket()
        self.getHostName()
        self.connectToHost()

    def getSocket(self):
        """
        Return the socket
        """
        return self.s

    def initSocket(self):
        """
        Initialise une socket
        """
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error:
            self.log('Failed to create socket')
            sys.exit()
        self.log('Socket Created')

    def getHostName(self):
        """
        Get the ip address of the host.
        """
        try:
            self.remote_ip = socket.gethostbyname(self.host)
            self.log("Host " + self.host + " is on ip " + self.remote_ip)
        except socket.gaierror:
            # could not resolve
            self.log('Hostname could not be resolved. Exiting')
            sys.exit()

    def connectToHost(self):
        """
        Connect to the remote host
        """
        self.s.connect((self.remote_ip, self.port))
        self.log(
            'Socket Connected to ' + self.host + ' on ip ' + self.remote_ip)

    def send(self, packet):
        """
        Takes a packet as a string
        Sends a packet
        Return : error if the packet could not be sent
        """
        try:
            # Set the whole string
            self.log("Sending : " + str(packet))
            self.s.sendall(packet)
        except socket.error:
            # Send failed
            self.log('Send failed')
            sys.exit()

    def receive(self):
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
            "GET /"
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

    def getData(self, httpPacket):
        """
        Returns the data of a http packet
        """
        data_string = str(httpPacket)
        data_index = data_string.find(hardReturn + hardReturn)
        return data_string[data_index + 4:]

    def getGETPacket(self):
        """
        Constructs the http packet to send
        """
        packet = self.GETHeader + self.host + hardReturn + self.data
        return packet

    def getOkPacket(self):
        packet = self.OK200Header + hardReturn
        return packet


def test():
    print("test")


def main():
    packet = httpPacket("localhost")
    packet.setCookie(1234)
    packet.setData("salut tout le monde")
    print(packet.getData(packet.getGETPacket()))

# This is a Python's special:
# The only way to tell wether we are running the program as a binary,
# or if it was imported as a module is to check the content of
# __name__.
# If it is `__main__`, then we are running the program
# standalone, and we run the main() function.
if __name__ == "__main__":
    main()
