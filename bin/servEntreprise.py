import socket
import sys
from threading import Thread
from binascii import hexlify

cookie_header=b'Cookie: tok='

client_list={}

class HTTPRedirectToSSH(Thread):
    def __init__(self, http_socket ):
        Thread.__init__(self)
        self.http=http_socket
    
    def run(self):
        cookie=-1
        while True:
            # Receiving from client
            data = self.http.recv(8192)
            
            idx=data.find(b'\r\n\r\n')
            print("idx ="+str(idx))
            if idx == -1:
                headers = ""
                content = data
            else:
                headers=data[:idx]

                #Récupération du Cookie si il y est
                if "Cookie"  in headers :
                    idx_cookie=headers.find(cookie_header)
                    
                    idx_end_cookie=headers[idx_cookie+len(cookie_header):].find(b'\r\n')

                    cookie=int(headers[idx_cookie:idx_end_cookie])

                content=data[idx+4:]

            if cookie >0 :
                ssh=client_list[cookie].ssh

            else:
                ssh = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                ssh.connect(('localhost',22))
                SSHRedirectToHTTP(self.http,ssh).start()
            if len(headers > 0) :
                print("headers="+headers.decode('utf-8'))
            print("data="+str(data))
            
            ssh.sendall(data)
        
        self.http.close()



class SSHRedirectToHTTP(Thread):    
    def __init__(self, http_socket , ssh_socket ):
        Thread.__init__(self)
        self.ssh=ssh_socket
        self.http=http_socket
        
        tok=random.randint(0xffffffffffffffff)
        while tok in client_list.keys():
            tok = random.randint(0xffffffffffffffff)
        client_list[tok] = self

        message = ("HTTP/1.1 200 OK\r\n"
              +"Content-type: application/octet-stream\r\n"
              +"Transfer-Encoding: chunked\r\n"
              +"Set-Cookie: tok=%x\r\n"%tok
              +"\r\n")
        
        self.http.send(message)
    
    def run(self):
        

        while True:
            # Receiving from client
            data = self.ssh.recv(8192)
            
            print("data="+str(data))
            try:
                self.ssh.sendall(("%x\r\n"%(len(data)))+data+"\r\n")
            except socket.error as e:
                print(e)
                break

        self.conn.close()


class HttpServer(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.sock.bind((socket.gethostname(), 8081))
    
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
    HttpServer().start()
