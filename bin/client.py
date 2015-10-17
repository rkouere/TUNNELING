#! /usr/bin/env python3

import sys  # for exit
from tools import httpPacket, client


def main(host, port):
    # icreate an INET, STREAMing socket
    con = client(host, port, True)
    con.initConnection()
    # Send some data to remote server
    message = httpPacket(host)
    # Now receive data
    tok = 1
    for i in range(0, 2):
        tok += 1
        message.setData(str(tok))
        print("==============sending packet ==================")
        con.sendPacket(message.getGETPacket())
        print("==============receiving packet ==================")
        print(con.receivePacket())

# This is a Python's special:
# The only way to tell wether we are running the program as a binary,
# or if it was imported as a module is to check the content of
# __name__.
# If it is `__main__`, then we are running the program
# standalone, and we run the main() function.
if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]))
