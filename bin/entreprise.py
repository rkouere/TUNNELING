# ! /usr/bin/env python3
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



def sendToSSH(data):
    print(data)

def getSSH():
    """
    Sends GET messages to the maison
    Forward the message from the HTTP response to ssh
    """
    try: 
        proxy_support = urllib.request.ProxyHandler({"http":"http://proxy.univ-lille1.fr:3128"})
        opener = urllib.request.build_opener(proxy_support)
        urllib.request.install_opener(opener)

        req = urllib.request.Request("http://vps2055u24.ovh.net/", {"Cache-Control": "no-cache, no-store, must-revalidate"})
        html = urllib.request.urlopen(req).read()
        sendToSSH(html)
    except urllib.error.HTTPError:
        print("toto")
   

def connectHttp():
    try:
        proxy_support = urllib.request.ProxyHandler({"http":"http://proxy.univ-lille1.fr:3128"})
        opener = urllib.request.build_opener(proxy_support)
        urllib.request.install_opener(opener)

        # req = urllib.request.Request("http://vps205524.ovh.net/", {"Cache-Control": "no-cache"})
        req = urllib.request.Request("http://vps205524.ovh.net/")
        html = urllib.request.urlopen(req).read()
        return(html)
    except urllib.error.HTTPError:
        return False

def init():
    """
    Sends packets to maison all the time
    When a packet has arrived, we start a new process
    """
    req = connectHttp()
    while req is False:
        req = connectHttp()
    print(req)

# This is a Python's special:
# The only way to tell wether we are running the program as a binary,
# or if it was imported as a module is to check the content of
# __name__.
# If it is `__main__`, then we are running the program
# standalone, and we run the main() function.
if __name__ == "__main__":
    # tunnel(sys.argv[1], int(sys.argv[2]), int(sys.argv[3])).init()
    init()
