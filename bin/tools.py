#! /usr/bin/env python3
import socket   # for sockets
import sys
hardReturn = "\r\n"


def packetHttpToSSH(packet):
    """
    Strips the http packet of the header and sends it to ssh
    """
    return createSSHPacketFromHml(packet)


def packetSSHToHttp(packet, host):
    """
    Encapsulates a ssh packet with a http header
    """
    return createGetPacketFromSSH(packet)


def processHttpRequests(packet, http_con, ssh_con):
    """
    Takes a http packet
    Strips the packet of its header
    Sends the packet to ssh
    TO DO: sends a reply to ssh
    """
    # data = packetHttpToSSH(packet)
    data = packet
    print(data)
    ssh_con.sendall(data)


def proceesSSHRequests(packet, http_con):
    """
    Takes a ssh packet
    Encapsulates the packet in a GET http packet
    Sends the new packet to http
    """
    # data = packetSSHToHttp(packet)
    data = packet
    http_con.sendall(data)

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


def createGetPacketFromSSH(packet):
    """
    Encapsulate data (byte array) in a GET packet
    Return a bite array of the packer
    """
    GETHeader = (
        "GET /"
        + " HTTP/1.1" + hardReturn
        + "Connection: keep-alive" + hardReturn
        + "Cache-Control: no-cache" + hardReturn + hardReturn).encode()
    return GETHeader + packet


def createSSHPacketFromHml(packet):
    data_string = packet.decode()
    data_index = data_string.find(hardReturn + hardReturn)
    return packet[data_index + 4:]


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
        print(self.data)
        # self.setContentLength()

    def setContentLength(self):
        print(self.data)
        self.contentLength = "Content-length: " + str(
            len(self.data.encode())) + hardReturn

    def getData(self, httpPacket):
        """
        Returns the data of a http packet
        """
        data_string = httpPacket.decode()
        data_index = data_string.find(hardReturn + hardReturn)
        return httpPacket[data_index + 4:]

    def getGETHeader(self):
        return (self.GETHeader + self.host + hardReturn).encode()

    def getGETPacket(self, data):
        """
        Constructs the http packet to send
        """
        print(data)
        header = (self.GETHeader + self.host + hardReturn).encode()
        packet = header + data
        return packet

    def getOkPacket(self):
        packet = self.OK200Header + hardReturn
        return packet


def test():
    print("test")


def main():
    http = packetSSHToHttp(b'deadbeef', "")
    print(http)
    ssh = packetHttpToSSH(http)
    print(ssh)

# This is a Python's special:
# The only way to tell wether we are running the program as a binary,
# or if it was imported as a module is to check the content of
# __name__.
# If it is `__main__`, then we are running the program
# standalone, and we run the main() function.
if __name__ == "__main__":
    main()
