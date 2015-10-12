import socket
import sys
from threading import Thread
from binascii import hexlify
from servEntreprise import *

server_hostname='localhost'
server_port=8081

tok=-1
# Gère le flux de retour HTTP vers le canal SSH
class HTTPTunnelToSSH(Thread):
    def __init__(self, ssh_socket , http_socket):
        Thread.__init__(self)
        self.ssh=ssh_socket
        self.http=http_socket
            
        data=self.http.recv(8192)
        
        idx=data.find(b'\r\n\r\n')
        if idx == -1:
            headers = ""
            content = data
        else:
            headers=data[:idx]

            #Récupération du Cookie si il y est
            if "Cookie"  in headers :
                idx_cookie=headers.find(cookie_header)
                
                idx_tok=data.find(b'tok=') 
                idx_end_cookie=headers[idx_cookie+len(cookie_header):].find(b'\r\n')
                self.tok=int(headers[idx_cookie:idx_end_cookie])
                tok=self.tok
    def run():
        while True:

            data=self.http.recv(8192)
            
            idx_end_size=data.find(b'\r\n')
            hex_size=data[:idx_end_size]
            size=int.from_bytes(hex_size)
            content=data[idx_end_size:-2]
            self.ssh.sendall(content)


# Gère la sortie du flux ssh et redirige en HTTP
class SSHTunnelClient(Thread):
    def __init__(self,ssh_socket):
        Thread.__init__(self)
        self.ssh=ssh_socket
        self.init_connection()  
        
    def init_connection(self):
        
        try:
            # create an AF_INET, STREAM socket (TCP)
            self.http = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as msg:
            print('Failed to create socket. Error code: ' +
                  str(msg[0]) + ' , Error message : ' + msg[1])
            sys.exit()

        print('Socket Created')

        try:
            remote_ip = socket.gethostbyname(server_hostname)

        except socket.gaierror:
            # could not resolve
            print('Hostname could not be resolved. Exiting')
            sys.exit()

        print('Ip address of ' + server_hostname + ' is ' + remote_ip)
        
        # Connect to remote server
        self.http.connect((remote_ip, server_port))
       
        
        HTTPTunnelToSSH(self.ssh,self.http).start()
        
        content=self.ssh.recv(8192)
        print('Socket Connected to ' + host + ' on ip ' + remote_ip)
        
        # Send some data to remote server
        header_base = ("POST / HTTP/1.1\r\n"
                  +"Host: %s\r\n"%(server_hostname))


        header=(header_base
              +"Content-Length: %d\r\n"%(len(content))
              +"\r\n"
              )
        message=header+content
        try:
            # Set the whole string
            self.http.sendall(message)
        
        except socket.error:
            # Send failed
            print('Send failed')
            sys.exit()

        print('Message send successfully')
        # Now receive data
    
    
    def run():
        
        header_base = ("POST / HTTP/1.1\r\n"
                  +"Host: %s\r\n"%(server_hostname))

        while True:
            content=self.ssh.recv(8192)
            
            header=(header_base
                    +"Content-Length: %d\r\n"%(len(content))
                    +"Cookie: tok="+str(tok)+"\r\n"               
                    +"\r\n"
                )
            message=header+content
            
            try:
                # Set the whole string
                self.http.sendall(message)
        
            except socket.error:
                # Send failed
                print('Send failed')
                sys.exit()



def wait_conn(sock):
    # Start listening on socket
    sock.listen(10)

    print('Socket now listening')
    # Function for handling connections. This will be used to create threads
    # now keep talking with the client
    while 1:
        # wait to accept a connection - blocking call
        conn, addr = sock.accept()
        

        print('Connected with ' + addr[0] + ':' + str(addr[1]))
        # start new thread takes 1st argument as a function name to be run,
        # second is the tuple of arguments to the function.
        SSHTunnelClient(conn).start()
        #start_new_thread(clientthread, (conn,))
    s.close()


def main():
    listen_port=8888
    
    #ssh_sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #ssh_sock.connect(("localhost",22))
    

    HOST = 'localhost'    # Symbolic name meaning all available interfaces
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Bind socket to local host and port
    try:
        sock.bind((HOST, listen_port))
    except socket.error as msg:
        print('Bind failed. Error Code : ' +
              str(msg[0]) + ' Message ' + str(msg[1]))
        sys.exit()
    print('Socket bind complete')
    wait_conn(sock)

if __name__=="__main__" :
    main()
