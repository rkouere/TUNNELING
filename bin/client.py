#! /usr/bin/env python3

import sys  # for exit
from tools import httpPacket, server


def main(host, port):
    # icreate an INET, STREAMing socket
    con = server(host, port, True)
    con.initConnection()
    # Send some data to remote server
    message = httpPacket(host)
    con.sendPacket(message.getGETPacket())
    print('Message send successfully')
    # Now receive data
    print(con.receivePacket())

# This is a Python's special:
# The only way to tell wether we are running the program as a binary,
# or if it was imported as a module is to check the content of
# __name__.
# If it is `__main__`, then we are running the program
# standalone, and we run the main() function.
if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]))
