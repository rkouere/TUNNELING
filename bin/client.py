#! /usr/bin/env python3

#Socket client example in python
 
import socket   #for sockets
import sys  #for exit
from tools import httpPacket



class server:
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
        except socket.gaierror:
            #could not resolve
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
        try :
            #Set the whole string
            print(packet.encode())
            self.s.sendall(packet.encode())
        except socket.error:
            #Send failed
            print('Send failed')
            sys.exit()

    def receivePacket(self):
        """
        Receive a packet
        """
        return self.s.recv(4096)


def main(host, port): 
    #create an INET, STREAMing socket
    con = server(host, port, True)
    con.initConnection()
    #Send some data to remote server
    message = httpPacket()
    con.sendPacket(message.getGETPacket())
    print('Message send successfully')
     
    #Now receive data
    print(con.receivePacket())
     
# This is a Python's special:
# The only way to tell wether we are running the program as a binary,
# or if it was imported as a module is to check the content of
# __name__.
# If it is `__main__`, then we are running the program
# standalone, and we run the main() function.
if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]))
