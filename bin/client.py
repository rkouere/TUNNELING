#! /usr/bin/env python3
import sys
from tools import client, httpPacket


def main(host, port):
    # connection a la machine distante
    http_con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    http_con.connect((host, port))
    

# This is a Python's special:
# The only way to tell wether we are running the program as a binary,
# or if it was imported as a module is to check the content of
# __name__.
# If it is `__main__`, then we are running the program
# standalone, and we run the main() function.
if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]))
