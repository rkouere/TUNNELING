import http.server
import socketserver

PORT = 80



handler = http.server.CGIHTTPRequestHandler
handler.cgi_directories = ['/']  # this is the default


httpd = socketserver.TCPServer(("", PORT), handler)

print("serving at port", PORT)
httpd.serve_forever()

