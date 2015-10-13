import time
import socket
import sys
from threading import Thread
from binascii import hexlify
from servEntreprise import *

server_hostname='pcmt23'
server_port=8890


tok=-1
# Gère le flux de retour HTTP vers le canal SSH
class HTTPTunnelToSSH(Thread):
    def __init__(self, ssh_socket , http_socket):
        Thread.__init__(self)
        self.ssh=ssh_socket
        self.http=http_socket
            
        data=self.http.recv(8192)
        
        print("init httptunn content receive="+data.decode())
        idx=data.find(b'\r\n\r\n')
        if idx == -1:
            headers = ""
            content = data
        else:
            headers=data[:idx]

            #Récupération du Cookie si il y est
            if "Cookie"  in headers.decode() :
               	print("headears ="+headers.decode()) 
                idx_tok=headers.find("tok=".encode()) 
                idx_end_tok=headers[idx_tok:].find(b'\r\n')
                self.tok=headers[idx_tok+4:]
                tok=self.tok
                print("init tok="+str(tok))
            
            content=data[idx+4:] 
            print("httptun init send : "+content.decode())
            self.ssh.sendall(content)

    def run(self):
        while True:

            data=self.http.recv(8192)
            if data:            
              print("httptun run data="+str(data))
              idx_end_size=data.find(b'\r\n')
              #hex_size=data[:idx_end_size]
              #print("hex_size="+int(hex_size))
              #size=int.from_bytes(hex_size)
              content=data[idx_end_size+2:-2]

              print("httptun run content="+str(content))
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
       
        
        
        content=self.ssh.recv(8192)
        print("init content receive="+content.decode())
        
        # Send some data to remote server
        header_base = ("POST / HTTP/1.1\r\n"
                  +"Host: %s\r\n"%(server_hostname))


        header=(header_base
              +"Content-Length: %d\r\n"%(len(content))
              +"\r\n")
        message=header.encode() + content
 
        print("message="+message.decode())
        try:
            # Set the whole string
            self.http.sendall(message)
        
        except socket.error:
            # Send failed
            print('Send failed')
            sys.exit()

        print('Message send successfully')
        # Now receive data
        HTTPTunnelToSSH(self.ssh,self.http).start()



    def run(self):
        
        header_base = ("POST / HTTP/1.1\r\n"
                  +"Host: %s\r\n"%(server_hostname))

        while True:
            content=self.ssh.recv(8192)
            if content : 
              #print("content receive="+content.decode())
              header=(header_base
                      +"Content-Length: %d\r\n"%(len(content))
                      +"Cookie: tok="+str(1234567890)+"\r\n"               
                      +"\r\n"
                  )
              message=header.encode()+content
              #print("message="+message.decode())

              try:
                  time.sleep(0.01)
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
    sock.close()


def main():
	
    listen_port=int(sys.argv[1])
    
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
