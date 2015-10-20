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
import base64 as B64

# maison = "http://vps205524.ovh.net/"
maison = "http://5.196.70.218"

#proxy = "http://proxy.univ-lille1.fr:3128"
proxy = "http://pcmt17:8008"



def log(message):
    print("[maison] " + message)
    

def sendSSHRequestToMaison(data):
    try:
        proxy_support = urllib.request.ProxyHandler(
            {"http": proxy})
        opener = urllib.request.build_opener(proxy_support)
        urllib.request.install_opener(opener)
        # req = urllib.request.Request("http://vps205524.ovh.net/",
        # {"Cache-Control": "no-cache"})
        # req = urllib.request.Request("http://vps205524.ovh.net/")
        log("sending POST")
        req = urllib.request.Request(maison,B64.b64encode(data) )

        html = urllib.request.urlopen(req).read()
        print(html)
        return html
    except urllib.error.HTTPError:
        return False



def getSSHRequestFromMaison():
    try:
        proxy_support = urllib.request.ProxyHandler(
            {"http": proxy})
        opener = urllib.request.build_opener(proxy_support)
        urllib.request.install_opener(opener)
        # req = urllib.request.Request("http://vps205524.ovh.net/",
        # {"Cache-Control": "no-cache"})
        # req = urllib.request.Request("http://vps205524.ovh.net/")
        req = urllib.request.Request(maison)
        data = urllib.request.urlopen(req).read()
        print(str(data))
        if( len(data) < 1 ):
            return False
        elif ('<html>' in str(data)):
            return False    
        else :
            return data
    except urllib.error.HTTPError:
        return False


def sendToSSH(ssh_con, req):
    """
    Sends a request to ssh
    """
    print("REQ="+str(req))
    ssh_con.sendall(B64.b64decode(req))




class sendFromSSH(threading.Thread):
    def __init__(self, ssh_con):
        threading.Thread.__init__(self)
        self.ssh_con = ssh_con
        print("thread started")

    def run(self):
        while True:
            data = self.ssh_con.recv(1024)
            if data:
                print("[ssh] data received = " + str(data))
                print("[POST] sending the data")
                sendSSHRequestToMaison(data)
                time.sleep(0.1)
            else:
                break
        ssh_socket.close()




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
    while req is False or req is None:
        log("sending first request")
        req = getSSHRequestFromMaison()
        time.sleep(1)

    # initialise connection to ssh
    ssh_con = client("localhost", 22).initConnection()
    log("connected to ssh")
    # we start a new thread to deal with the ssh connection
    sendFromSSH(ssh_con).start()
    # we send the request to ssh
    sendToSSH(ssh_con, req)
    # we loop with a GET request
    while True:
        data = getSSHRequestFromMaison()
        if data is not False:
            sendToSSH(ssh_con, data)

# This is a Python's special:
# The only way to tell wether we are running the program as a binary,
# or if it was imported as a module is to check the content of
# __name__.
# If it is `__main__`, then we are running the program
# standalone, and we run the main() function.
if __name__ == "__main__":
    # tunnel(sys.argv[1], int(sys.argv[2]), int(sys.argv[3])).init()
    init()

