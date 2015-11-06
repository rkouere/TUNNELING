#! /usr/bin/env python3
import socket   # for sockets
import sys
from Crypto.Cipher import XOR
import base64
import struct
import random
import time
import hashlib

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
    def __init__(self):
        self.key = "maggle"

    def encrypt(self, plaintext):
        cipher = XOR.new(self.key)
        return base64.b64encode(base64.b64encode(cipher.encrypt(plaintext)))

    def decrypt(self, ciphertext):
        cipher = XOR.new(self.key)
        return cipher.decrypt(base64.b64decode(base64.b64decode(ciphertext)))


def encode_data(data):
    #return base64.b64encode(data)
    
    
    print("[send time ]="+str(encode_data.num))
    
    len_data=len(data)
    len_nn=random.randint(1,8192-len_data)

    header=struct.pack("<III",encode_data.num,len_data,len_nn)
    
    encode_data.num+=1

    noisynoise=random.getrandbits(len_nn*8)

    
    all_data=header+data+(noisynoise.to_bytes(len_nn,'big'))
   
    print("len(all_data)="+str(len(all_data)))
    signature=hashlib.sha256(all_data).hexdigest()
    print("SIGNATURE="+signature)
    all_data=all_data+signature.encode('ascii')
    return crypto().encrypt(all_data)
encode_data.num=1

def decode_data(data):
    #return base64.b64decode(data)
    if len(data)>0:
        clear_data=crypto().decrypt(data)

        time_now,len_data,len_nn=struct.unpack("<III",clear_data[:12])
    
        print("[receive time ]="+str(time_now))
    
        ssh_data=clear_data[12:12+len_data]
        
        signature=(clear_data[12+len_data+len_nn:]).decode()
    
        print("len(clear_data)="+str(len(clear_data[:-64])))
         
        verif_sign=hashlib.sha256(clear_data[:-64]).hexdigest()

        if signature == verif_sign:
            return time_now,ssh_data
    return 0,''

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
