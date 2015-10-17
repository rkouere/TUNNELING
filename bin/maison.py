import socket
import sys
import time
from tools import client, tunnel


if __name__ == "__main__":
    tunnel(sys.argv[1], int(sys.argv[2]), int(sys.argv[3])).init()
