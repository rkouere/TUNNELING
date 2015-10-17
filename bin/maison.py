import socket
import sys
from threading import Thread
import time


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
    ssh_con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssh_con.connect(("localhost", 22))
    print("connection ssh ok")
    # on s'occupe de renvoyer les messages venant de ssh vers http
    sshToHttp(http_socket, ssh_con, data).start()
    # on continue de recevoir ce que http recoit et de le renvoyer à ssh
    while True:
        print("[http] waiting for data")
        data = http_socket.recv(1024)
        print("[http] data " + str(data))
        print("[http] sending the data")
        ssh_con.sendall(data)
        time.sleep(0.1)


class sshToHttp(Thread):
    def __init__(self, http_socket, ssh_socket, first_data):
        Thread.__init__(self)
        self.ssh = ssh_socket
        self.http = http_socket

        print("[SSHRedirectToHTTP] send first message = " + str(first_data))
        self.ssh.send(first_data)

    def run(self):
        """
        Récupère le flux ssh et le renvoit au serveur
        """
        while True:
            # Receiving from ssh
            print("[SSHRedirectToHTTP] waiting for data to receive")
            data = self.ssh.recv(8192)
            if data:
                print("[SSHRedirectToHTTP] recv")
                print("[SSHRedirectToHTTP] dataSSH = " + str(data))
                try:
                    print("[SSHRedirectToHTTP] sendall")
                    time.sleep(0.01)
                    self.http.sendall(data)
                except socket.error as e:
                    print(e)
                    break
            else:
                break
        self.ssh.close()

if __name__ == "__main__":
    sshListening(sys.argv[1], int(sys.argv[2]))
