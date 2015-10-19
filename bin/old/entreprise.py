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
import http.client
import urllib.request

<<<<<<< HEAD
=======
class HttpToSSH(threading.Thread):
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
>>>>>>> f0ddfe85ff6d2362a864ed538ba76fe5a97ba2b9

def connectHttp():
    
    proxy_support = urllib.request.ProxyHandler({"http":"http://proxy.univ-lille1.fr:3128"})
    opener = urllib.request.build_opener(proxy_support)
    urllib.request.install_opener(opener)

<<<<<<< HEAD
    # html = urllib.request.urlopen("http://vps205524.ovh.net/", b'salut').read()
    html = urllib.request.urlopen("http://vps205524.ovh.net/", b'salut').read()
    print(html)
=======

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
        data = ssh_socket.recv(8192)
        print("[ssh] data received = " + data.decode())
        http_con = client(self.host, self.portOut).initConnection()
        HttpToSSH(ssh_socket, http_con, data).start()

        while True:
            data = ssh_socket.recv(8192)
            if data:
                print("[ssh] data received = " + str(data))
                print("[http] sending the data")
                proceesSSHRequests(data, http_con)
                time.sleep(0.1)
            else:
                break
        http_con.close()
>>>>>>> f0ddfe85ff6d2362a864ed538ba76fe5a97ba2b9

# This is a Python's special:
# The only way to tell wether we are running the program as a binary,
# or if it was imported as a module is to check the content of
# __name__.
# If it is `__main__`, then we are running the program
# standalone, and we run the main() function.
if __name__ == "__main__":
<<<<<<< HEAD
=======
    params = urllib.parse.urlencode({'@number': 12524, '@type': 'issue', '@action': 'show'})
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = http.client.HTTPConnection("vps205524.ovh.net")
    conn.request("GET", "")#, params, headers)
>>>>>>> f0ddfe85ff6d2362a864ed538ba76fe5a97ba2b9
    # tunnel(sys.argv[1], int(sys.argv[2]), int(sys.argv[3])).init()
    connectHttp()
