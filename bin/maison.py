import socket
import sys
import time
from tools import client, sshToHttp


def sshListening(host, port):
    """
    Listen to a tcp connection on port XX
    When a connection has been made
        - creates a new thread
        - creates a new socket and connects to the ssh server
        - redirects the connections made by the ssh server to the http socket
    """
    http_con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    http_con.bind(("", port))
    # become a server socket
    http_con.listen(5)
    # accept connections from outside
    (http_socket, address) = http_con.accept()
    print("connection tcp created")
    data = http_socket.recv(1024)
    print("http data = " + data.decode())
    ssh_con = client("localhost", 22)
    sshToHttp(http_socket, ssh_con, data).start()
    # on continue de recevoir ce que http recoit et de le renvoyer à ssh
    while True:
        print("[http] waiting for data")
        data = http_socket.recv(1024)
        if data:
            print("[http] data " + str(data))
            print("[http] sending the data")
            ssh_con.send(data)
            time.sleep(0.1)
        else:
            break
    ssh_con.close()


if __name__ == "__main__":
    sshListening(sys.argv[1], int(sys.argv[2]))
