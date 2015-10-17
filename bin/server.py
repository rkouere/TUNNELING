import socket
import threading
import time
from tools import server

if __name__ == "__main__":
    HOST = ""
    PORT = 80
    serv = server(HOST, PORT)
    serv.accept()
