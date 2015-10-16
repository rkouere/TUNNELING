#! /usr/bin/env python3
import socket
import sys
from tools import httpPacket, server




def clientthread(conn):
    # Sending message to connected client
    # send only takes string
    conn.send(b'Welcome to the server. Type something and hit enter\n')
    # infinite loop so that function do not terminate and thread do not end.
    while True:
        # Receiving from client
        data = conn.recv(1024)
        reply = 'OK...' + data.decode()
        if not data:
            break
        conn.sendall(reply.encode())
    # came out of loop
    conn.close()


def main(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Socket created')
    # Bind socket to local host and port
    try:
        s.bind((host, port))
    except socket.error as msg:
        print('Bind failed. Error Code : ' +
              str(msg[0]) + ' Message ' + msg[1])
        sys.exit()
    print('Socket bind complete')
    # Start listening on socket
    s.listen(10)
    print('Socket now listening')
    # Function for handling connections. This will be used to create threads
    # now keep talking with the client
    while 1:
        # wait to accept a connection - blocking call
        conn, addr = s.accept()
        print('Connected with ' + addr[0] + ':' + str(addr[1]))
        # start new thread takes 1st argument as a function name to be run,
        # second is the tuple of arguments to the function.
        clientthread(conn)
    s.close()


# This is a Python's special:
# The only way to tell wether we are running the program as a binary,
# or if it was imported as a module is to check the content of
# __name__.
# If it is `__main__`, then we are running the program
# standalone, and we run the main() function.
if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]))


