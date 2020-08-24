import http.server
import socket

class HTTPServerV6(http.server.HTTPServer):
    address_family = socket.AF_INET6

Handler = http.server.SimpleHTTPRequestHandler
server = HTTPServerV6(('::', 8000), Handler)
server.serve_forever()

