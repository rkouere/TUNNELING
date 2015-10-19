# ! /usr/bin/env python3
# entreprise.py
"""
Ecoute sur le port xxx les connections ssh
Renvoie les connections ssh vers le port 80 du client xxx
Renvoie les connections du port 80 vers le ssh
"""
import time
import socket
from tools import processHttpRequests, client
import threading
import urllib.request


class sshToHttp(threading.Thread):
    """
    Redirects the connections from ssh client to http_socket
    """
    def __init__(self, http_socket, ssh_client, first_data):
        threading.Thread.__init__(self)
        self.ssh = ssh_client
        self.http = http_socket
        print(
            "[SSHRedirectToHTTP][ssh] send first message = " + str(first_data))
        processHttpRequests(first_data, self.http, self.ssh)

    def run(self):
        """
        Récupère le flux ssh et le renvoit au serveur
        """
        while True:
            # Receiving from ssh
            data = self.ssh.recv(8192)
            if data:
                print("[SSHRedirectToHTTP][ssh] dataSSH = " + str(data))
                try:
                    print("[SSHRedirectToHTTP][http] sendall")
                    time.sleep(0.01)
                    # proceesSSHRequests(data, self.http)
                except socket.error as e:
                    print(e)
                    break
            else:
                print("============data=============")
                print(data)
                break
        self.ssh.close()


def sendGET(ssh_con):
    """
    Sends GET messages to the maison
    If the message has content forward the message from the
    HTTP response to ssh
    Else sends another GET
    """
    while True:
        req = connectGET()
        if req is not False:
            sendToSSH(ssh_con, req)


class sendFromSSH(threading.Thread):
    def __init__(self, ssh_con):
        threading.Thread.__init__(self)
        self.ssh_con = ssh_con
        print("thread started")


def sendToSSH(ssh_con, req):
    """
    At first sends the request to ssh
    Waits for a message from ssh
    Sends the message as a POST
    Waits for a message from ssh
    Sends the message as a POST
    ...
    """
    print(req)
    ssh_con.sendall(req)


def connectGET(ssh_con=False):
    try:
        """
        proxy_support = urllib.request.ProxyHandler(
            {"http": "http://proxy.univ-lille1.fr:3128"})
        opener = urllib.request.build_opener(proxy_support)
        urllib.request.install_opener(opener)
        """
        # req = urllib.request.Request("http://vps205524.ovh.net/",
        # {"Cache-Control": "no-cache"})
        # req = urllib.request.Request("http://vps205524.ovh.net/")
        req = urllib.request.Request("http://192.168.0.13")

        html = urllib.request.urlopen(req).read()
        return html
    except urllib.error.HTTPError:
        return False


def init():
    """
    Sends packets to maison all the time
    When a packet has arrived
    - we initiate a new socket with the ssh server
    - we initiate a new thread that will listen to ssh and send post when
      ssh speaks
    - we send the first request to the ssh
    - we send GET all the time and when we have a OK reply we send it to ssh
    """
    req = False
    while req is False:
        req = connectGET()

    # initialise connection to ssh
    ssh_con = client("localhost", 22).initConnection()
    # we start a new thread to deal with the ssh connection
    sendFromSSH(ssh_con)
    # we send the request to ssh
    sendToSSH(ssh_con, req)
    # we loop with a GET request
    sendGET(ssh_con)

# This is a Python's special:
# The only way to tell wether we are running the program as a binary,
# or if it was imported as a module is to check the content of
# __name__.
# If it is `__main__`, then we are running the program
# standalone, and we run the main() function.
if __name__ == "__main__":
    # tunnel(sys.argv[1], int(sys.argv[2]), int(sys.argv[3])).init()
    init()
