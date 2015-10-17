#! /usr/bin/env python3
import sys
from tools import client, httpPacket, sshToHttp
import socket
import time

def main(host, port):
    """
    Attend une connection sur le port port

    """
    ssh_con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssh_con.bind(("", port))
    # become a server socket
    ssh_con.listen(5)
    # accept connections from outside
    (ssh_socket, address) = ssh_con.accept()
    print("connection ssh created")
    data = ssh_socket.recv(1024)
    print("ssh data = " + data.decode())
    http_con = client(host, 80)
    sshToHttp(ssh_socket, http_con, data).start()
    while True:
        print("[http] waiting for data")
        data = ssh_socket.recv(1024)
        if data:
            print("[http] data " + str(data))
            print("[http] sending the data")
            http_con.send(data)
            time.sleep(0.1)
        else:
            break
    http_con.close()


# This is a Python's special:
# The only way to tell wether we are running the program as a binary,
# or if it was imported as a module is to check the content of
# __name__.
# If it is `__main__`, then we are running the program
# standalone, and we run the main() function.
if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]))
