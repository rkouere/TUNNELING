# maison.py
"""
Ecoute sur le port 80 les connections qui viennent à elle
Envoie les packet du port 80 au ssh
Envoie les packet du ssh vers le port 80
"""

import sys
import time
import socket
from tools import client, httpPacket, processHttpRequests, proceesSSHRequests
import threading
import time


class sshToHttp(threading.Thread):
    """
    Redirects the connections from ssh client to http_socket
    """
    def __init__(self, http_socket, ssh_client, first_data):
        threading.Thread.__init__(self)
        self.ssh = ssh_client
        self.http = http_socket
        print("[SSHRedirectToHTTP][ssh] send first message = " + str(first_data))
        processHttpRequests(first_data, self.http, self.ssh)

    def run(self):
        """
        Récupère le flux ssh et le renvoit au serveur
        """
        while True:
            # Receiving from ssh
            data = self.ssh.recv(1024)
            if data:
                print("[SSHRedirectToHTTP][ssh] dataSSH = " + str(data))
                try:
                    print("[SSHRedirectToHTTP][http] sendall")
                    time.sleep(0.01)
                    proceesSSHRequests(data, self.http)
                except socket.error as e:
                    print(e)
                    break
            else:
                print("============data=============")
                print(data)
                break
        self.ssh.close()

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
        http_connection_ok = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        http_connection_ok.bind(("", self.portIn))
        # become a server socket
        http_connection_ok.listen(5)
        # accept connections from outside
        (http_socket, address) = http_connection_ok.accept()
        print("[http ] connection http created")
        data = http_socket.recv(1024)
        print("[http] data received = " + data.decode())
        ssh_con = client(self.host, self.portOut).initConnection()
        sshToHttp(http_socket, ssh_con, data).start()
        while True:
            data = http_socket.recv(1024)

            if data:
                print("[http] data received  = " + str(data))
                print("[ssh] sending the data")
                processHttpRequests(data, http_socket, ssh_con)
                time.sleep(0.1)
            else:
                break
        http_con.close()


if __name__ == "__main__":
    tunnel(sys.argv[1], int(sys.argv[2]), int(sys.argv[3])).init()
