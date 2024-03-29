#! /usr/bin/env python3
import socket   # for sockets
import sys
from Crypto.Cipher import XOR
import base64

hardReturn = "\r\n"


class crypto():
    """
    Thanks poida
    http://stackoverflow.com/questions/2490334/simple-way-to-encode-a-string-according-to-a-passwordself
    Usage :
    >>> encrypt('notsosecretkey', 'Attack at dawn!')
    'LxsAEgwYRQIGRRAKEhdP'

    >>> decrypt('notsosecretkey', encrypt('notsosecretkey', 'Attack at dawn!'))
    'Attack at dawn!'
    """
    secret_key = "maggle"

    def encrypt(self, key, plaintext):
        cipher = XOR.new(key)
        return base64.b64encode(cipher.encrypt(plaintext))

    def decrypt(self, key, ciphertext):
        cipher = XOR.new(key)
        return cipher.decrypt(base64.b64decode(ciphertext))


def encode_data(data):
    return base64.b64encode(data)


def decode_data(data):
    return base64.b64decode(data)


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
