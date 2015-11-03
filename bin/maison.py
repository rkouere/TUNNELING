# maison.py
"""
Ecoute sur le port 80 les connections qui viennent à elle
Envoie les packet du port 80 au ssh
Envoie les packet du ssh vers le port 80
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import sys
import socket
import cgi
from tools import encode_data, decode_data


class MyServer(BaseHTTPRequestHandler):
    def __init__(self, ssh_socket, *args):
        self.ssh = ssh_socket
        BaseHTTPRequestHandler.__init__(self, *args)

    def do_GET(self):
        self.send_response(200)
        self.ssh.settimeout(0.1)
        try:
            data = self.ssh.recv(4092)
            print("data="+str(data))
            self.send_header("Content-type", "application/octet-stream")
            self.end_headers()
            data_to_send = encode_data(data)
            self.wfile.write(data_to_send)
        except socket.timeout:
            print("No response from server")
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(
                "<html><head><title>GET : Title goes here.</title>" +
                "</head><body>TEST</body></html>", "utf-8"))

    def do_POST(self):
        print("========= path " + self.path)
        if self.path.find("/get") != -1:

            self.send_response(200)
            self.ssh.settimeout(0.1)
            try:
                data = self.ssh.recv(4092)
                print("data="+str(data))
                self.send_header("Content-type", "application/octet-stream")
                self.end_headers()
                data_to_send = encode_data(data)
                self.wfile.write(data_to_send)
            except socket.timeout:
                print("No response from server")
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(bytes(
                    "<html><head><title>GET : Title goes here.</title>" +
                    "</head><body>TEST</body></html>", "utf-8"))

        else:

            if(self.headers.get('Content-Type', False)):
                ctype, pdict = cgi.parse_header(self.headers['Content-Type'])
                print(str(ctype))
                if ctype == 'application/x-www-form-urlencoded':
                    length = int(self.headers['Content-Length'])
                    print(str(length))
                    data = decode_data(self.rfile.read(length))
                else:
                    print("parse error")

                print(str(data))
                # data=postvars['data'.encode()][0]
                if data:
                    self.ssh.sendall(data)

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(
                "<html><head><title>GET : Title goes here.</title>" +
                "</head><body>TEST</body></html>", "utf-8"))

            # self.send_header("Content-type", "text/html")
            #self.end_headers()
            # self.wfile.write()
            """
            self.wfile.write(bytes(
                "<html><head><title>POST :Title goes here.</title>" +
                "</head>", "utf-8"))
            self.wfile.write(bytes("<body><p>This is a test.</p>", "utf-8"))
            self.wfile.write(bytes(
            "<p>You accessed path: %s</p>" % self.path, "utf-8"))
            self.wfile.write(bytes("</body></html>", "utf-8"))
            """


class tunnel:
    """
    Maison : "sudo python3 maison.py localhost 80 22"
    Entreprise : "python3 entreprise.py 192.168.0.19 9000 80"
    """
    def __init__(self, host, http_port, ssh_port):
        self.host = host
        self.http_port = http_port
        self.ssh_port = ssh_port

    def init(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Bind socket to local host and port
        try:
            sock.bind((self.host, self.ssh_port))
        except socket.error as msg:
            print('Bind failed. Error Code : ' +
                  str(msg[0]) + ' Message ' + str(msg[1]))
            sys.exit()
        print('Socket bind complete')
        # Start listening on socket
        sock.listen(10)

        print('Socket now listening')
        # Function for handling connections.
        # This will be used to create threads
        # now keep talking with the client
        # while 1:
        # wait to accept a connection - blocking call
        conn, addr = sock.accept()

        print('Connected with ' + addr[0] + ':' + str(addr[1]))
        handler = handleRequestsUsing(conn)
        myServer = HTTPServer(('', self.http_port), handler)
        # start new thread takes 1st argument as a function name to be run,
        # second is the tuple of arguments to the function.
        # SSHTunnelClient(conn).start()
        # start_new_thread(clientthread, (conn,))

        try:
            myServer.serve_forever()
        except KeyboardInterrupt:
            pass

        myServer.server_close()

        sock.close()


def handleRequestsUsing(ssh_socket):
    return lambda *args: MyServer(ssh_socket, *args)

if __name__ == "__main__":
    # host http_port ssh_port
    tunnel(sys.argv[1], int(sys.argv[2]), int(sys.argv[3])).init()
