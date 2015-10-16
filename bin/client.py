#! /usr/bin/env python3

#Socket client example in python
 
import socket   #for sockets
import sys  #for exit

def main(host, port): 
    #create an INET, STREAMing socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print('Failed to create socket')
        sys.exit()
         
    print('Socket Created')
     
     
    try:
        remote_ip = socket.gethostbyname( host )
     
    except socket.gaierror:
        #could not resolve
        print('Hostname could not be resolved. Exiting')
        sys.exit()
     
    #Connect to remote server
    s.connect((remote_ip , port))
     
    print('Socket Connected to ' + host + ' on ip ' + remote_ip)
     
    #Send some data to remote server
    message = "GET / HTTP/1.1\r\n\r\n"
     
    try :
        #Set the whole string
        print(message)
        s.sendall(message.encode())
    except socket.error:
        #Send failed
        print('Send failed')
        sys.exit()
     
    print('Message send successfully')
     
    #Now receive data
    reply = s.recv(4096)
     
    print(reply)
# This is a Python's special:
# The only way to tell wether we are running the program as a binary,
# or if it was imported as a module is to check the content of
# __name__.
# If it is `__main__`, then we are running the program
# standalone, and we run the main() function.
if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]))
