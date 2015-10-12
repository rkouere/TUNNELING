#! /usr/bin/env python3

# first of all import the socket library
import socket               # Import socket module
import sys


def main():

    try:
        # create an AF_INET, STREAM socket (TCP)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as msg:
        print('Failed to create socket. Error code: ' +
              str(msg[0]) + ' , Error message : ' + msg[1])
        sys.exit()

    print('Socket Created')

    host = 'localhost'
    port = 8888
    try:
        remote_ip = socket.gethostbyname(host)

    except socket.gaierror:
        # could not resolve
        print('Hostname could not be resolved. Exiting')
        sys.exit()

    print('Ip address of ' + host + ' is ' + remote_ip)
    # Connect to remote server
    s.connect((remote_ip, port))
    print('Socket Connected to ' + host + ' on ip ' + remote_ip)
    # Send some data to remote server
    header_base = ("POST / HTTP/1.1\r\n"
              +"Host: %s\r\n"%("localhost"))


    while(1):
        content=sys.stdin.readline();
        header=(header_base
              +"Content-Length: %d\r\n"%(len(content))
              +"\r\n"
              )
        message=header+content
        try:
            # Set the whole string
            s.sendall(message.encode())
        except socket.error:
            # Send failed
            print('Send failed')
            sys.exit()

        print('Message send successfully')
        # Now receive data
        reply = s.recv(4096)
        print("reply="+reply.decode('utf-8'))
# This is a Python's special:
# The only way to tell wether we are running the program as a binary,
# or if it was imported as a module is to check the content of
# __name__.
# If it is `__main__`, then we are running the program
# standalone, and we run the main() function.
if __name__ == "__main__":
    main()
