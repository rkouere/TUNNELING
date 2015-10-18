#! /usr/bin/env python3
import socket   # for sockets
import sys
hardReturn = "\r\n"


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
    data_string = packet.decode("ISO-8859-1")
    data_index = data_string.find(hardReturn + hardReturn)
    return packet[data_index + 4:]


def packetHttpToSSH(packet):
    """
    Strips the http packet of the header and sends it to ssh
    """
    return packet
    # return createSSHPacketFromHml(packet)


def packetSSHToHttp(packet, host):
    """
    Encapsulates a ssh packet with a http header
    """
    return packet
    # return createGetPacketFromSSH(packet)


def processHttpRequests(packet, http_con, ssh_con):
    """
    Takes a http packet
    Strips the packet of its header
    Sends the packet to ssh
    TO DO: sends a reply to ssh
    """
    data = packetHttpToSSH(packet)
    print("[processHttpRequests] sending to ssh " + str(data))
    ssh_con.sendall(data)


def proceesSSHRequests(packet, http_con):
    """
    Takes a ssh packet
    Encapsulates the packet in a GET http packet
    Sends the new packet to http
    """
    data = packetSSHToHttp(packet, "")
    print("[proceesSSHRequests] sending to http " + str(data))
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


def main():
    ssh_packet = b'\x00\x00\x00 \t{\xf14F]\x1by<a\xc6\x9a"\xb8\x9c\xab\xc8\xf5\x94\x96\xb6\xdbzF\xa6K\xd6\xdd\xc6=\xb4\x90\x95\xd7\xf1\xc4\x8a\x1b\xc9n\x00\x00\x00 \xbc~\x977\xb5\xd8\xf0vY\xbbq\xea*\x06\xe9\xab9\x9e\x0f\xc8\x07\xb9\\\x03@\xb6x\xd3\x81\\\x14j\xb3\xf6\x82R\xb3*\xac\xc1\x00\x00\x00\x10\xfeA\xae\x92z])\xeaH\xed\x1d\x1f\'\x1c\x94=\x95+\x81\x1c\xf6\x89/\xb8'
    print(ssh_packet)
    get_packet = createGetPacketFromSSH(ssh_packet)
    print(get_packet)
    ssh_new_pack = createSSHPacketFromHml(get_packet)
    print(ssh_new_pack)
    print(ssh_packet == ssh_new_pack)
# This is a Python's special:
# The only way to tell wether we are running the program as a binary,
# or if it was imported as a module is to check the content of
# __name__.
# If it is `__main__`, then we are running the program
# standalone, and we run the main() function.
if __name__ == "__main__":
    main()
