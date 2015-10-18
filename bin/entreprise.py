#! /usr/bin/env python3
# entreprise.py
"""
Ecoute sur le port xxx les connections ssh
Renvoie les connections ssh vers le port 80 du client xxx
Renvoie les connections du port 80 vers le ssh
"""
import sys
import time
import socket
from tools import client, processHttpRequests, proceesSSHRequests
import threading


class sshToHttp(threading.Thread):
    """
    Redirects the connections from ssh client to ssh_socket
    """
    def __init__(self, ssh_socket, http_socket, first_data):
        threading.Thread.__init__(self)
        self.http = http_socket
        self.ssh = ssh_socket
        print(
            "[SSHRedirectToHTTP][http] send first message = "
            + str(first_data))
        proceesSSHRequests(first_data, self.http)

    def run(self):
        """
        Récupère le flux ssh et le renvoit au serveur
        """
        while True:
            # Receiving from http
            data = self.http.recv(1024)
            if data:
                print(
                    "[SSHRedirectToHTTP][http]  data received = " + str(data))
                try:
                    print("[SSHRedirectToHTTP][ssh] sendall")
                    time.sleep(0.01)
                    processHttpRequests(data, self.http, self.ssh)
                except socket.error as e:
                    print(e)
                    break
            else:
                print("========================")
                print("CLOSE")
                break
        self.http.close()


class tunnel:
    """
    Maison : "sudo python3 maison.py localhost 80 22"
    Entreprise : "python3 entreprise.py 192.168.0.19 9000 80"
    """
    def __init__(self, host, portIn, portOut):
        self.host = host
        self.portIn = portIn
        self.portOut = portOut

    def init(self):
        ssh_con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ssh_con.bind(("", self.portIn))
        # become a server socket
        ssh_con.listen(5)
        # accept connections from outside
        (ssh_socket, address) = ssh_con.accept()
        print("[ssh] connection ssh created")
        data = ssh_socket.recv(1024)
        print("[ssh] data received = " + data.decode())
        http_con = client(self.host, self.portOut).initConnection()
        sshToHttp(ssh_socket, http_con, data).start()

        while True:
            data = ssh_socket.recv(1024)
            if data:
                print("[ssh] data received = " + str(data))
                print("[http] sending the data")
                proceesSSHRequests(data, http_con)
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
    tunnel(sys.argv[1], int(sys.argv[2]), int(sys.argv[3])).init()
