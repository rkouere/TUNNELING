import socket
import sys
from threading import Thread
from binascii import hexlify
import random
import time
cookie_header=b'Cookie: tok='

client_list={}




class HTTPRedirectToSSH(Thread):
    """
    Takes the data sent from http and executes it as ssh on the local host
    """
    def __init__(self, http_socket ):
        Thread.__init__(self)
        print("init httpredir")
        self.http=http_socket
    
    def run(self):
        print("run http redirect")
        cookie=b'-1'
        while True:
            # Receiving from client
            data = self.http.recv(8192)
            print("[HTTPRedirectToSSH] recv") 
            print("data = ")
            print(data) 
            print("=========================")
            idx=data.find(b'\r\n\r\n')
            print("idx ="+str(idx))
            if idx == -1:
                headers = ""
                content = data
            else:
                headers=data[:idx]

                #Récupération du Cookie si il y est
                if "Cookie"  in headers.decode():
                    idx_cookie=headers.find(cookie_header)
                    idx_end_cookie=headers[idx_cookie+len(cookie_header):].find(b'\r\n')
                    cookie=headers[idx_cookie + len(cookie_header):]

                content=data[idx+4:]
            # si ce n'est pas la premiere connection
            print("cookie = ")  
            print(cookie)
            if cookie != b'-1' :
                ssh=client_list[int(cookie)].ssh
                #ssh=client_ssh
            # sinon on créé un cookie pour la premiere connection
            else:
                """
                Connection au ssh du localhost
                """
                ssh = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                ssh.connect(('localhost',22))
                
                SSHRedirectToHTTP(self.http,ssh).start()
            if len(headers) > 0 :
                print("headers="+headers.decode('utf-8'))
            print("dataHTTP="+str(content))
            print("[HTTPRedirectToSSH] senall") 
            ssh.sendall(content)
        
        self.http.close()



class SSHRedirectToHTTP(Thread):    
    """
    
    """
    def __init__(self, http_socket , ssh_socket ):
        """
        Créé un cookie pour pouvoir gérer la première connection et faire en sorte que le proxy garde la connection ouverte
        Envoie au client une message disant que la connection est OK
        """
        Thread.__init__(self)
        self.ssh=ssh_socket
        self.http=http_socket
        
        tok=random.randint(0, 0xffffffffffffffff)
        """
        while tok in client_list.keys():
            tok = random.randint(0xffffffffffffffff)
        """
        tok = 1234567890
        client_list[tok] = self
        message = ("HTTP/1.1 200 OK\r\n"
              +"Content-type: application/octet-stream\r\n"
              +"Transfer-Encoding: chunked\r\n"
              +"Set-Cookie: tok=%x\r\n"%tok
              +"\r\n")
        print("[SSHRedirectToHTTP] send")
        self.http.send(message.encode())
    
    def run(self):
        """
        Récupère le flux ssh et le renvoit au serveur 
        """
        while True:
            # Receiving from ssh
            data = self.ssh.recv(8192)
            if data:
                print("[SSHRedirectToHTTP] recv")
                
                print("dataSSH="+str(data))
                try:
                    print("[SSHRedirectToHTTP] sendall")
                    print("length packer sent = " + str(("%x"%(len(data))).encode()))
                    time.sleep(0.01)
                    self.http.sendall((("%x"%(len(data))).encode())+b'\r\n'+data+b'\r\n')
                except socket.error as e:
                    print(e)
                    break

        self.ssh.close()


HOST=''
class HttpServer(Thread):
    """
    Demarre une socket sur le port PORT
    Ecoute les connection
    Des qu'il recoit une connection, il lance un thread pour s'occuper des interaction avec le ssh
    """
    def __init__(self):
        Thread.__init__(self)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((HOST, PORT))
    
    def run(self):
        # Start listening on socket
        self.sock.listen(10)

        print('Socket now listening')
        # Function for handling connections. This will be used to create threads
        # now keep talking with the client
        while 1:
            # wait to accept a connection - blocking call
            conn, addr = self.sock.accept()
            
            print('Connected with ' + addr[0] + ':' + str(addr[1]))
            # start new thread takes 1st argument as a function name to be run,
            # second is the tuple of arguments to the function.
            HTTPRedirectToSSH(conn).start()

            #start_new_thread(clientthread, (conn,))
        self.sock.close()

if __name__=="__main__":
    """
    Recuperation du port
    """
    PORT=int(sys.argv[1])
    HttpServer().start()
