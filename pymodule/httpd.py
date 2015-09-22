"""
Main daemon process for L1 GUI
"""

import SimpleHTTPServer
import SocketServer
import socket
import fcntl
import struct
import json
from urlparse import urlparse, parse_qs
from cgi import parse_header, parse_multipart
from createJsonResponse import LAYER1_PATH, createJsonResponse
from l1constants import *
import time

class MyHTTPHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):


    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    def do_GET(self):
        """
        handle GET request from browser
        """
        parsed_path = urlparse(self.path)
        message_parts = [
                'CLIENT VALUES:',
                'client_address=%s (%s)' % (self.client_address,
                                            self.address_string()),
                'command=%s' % self.command,
                'path=%s' % self.path,
                'real path=%s' % parsed_path.path,
                'query=%s' % parsed_path.query,
                'request_version=%s' % self.request_version,
                '',
                'SERVER VALUES:',
                'server_version=%s' % self.server_version,
                'sys_version=%s' % self.sys_version,
                'protocol_version=%s' % self.protocol_version,
                '',
                'HEADERS RECEIVED:',
                ]
        for name, value in sorted(self.headers.items()):
            message_parts.append('%s=%s' % (name, value.rstrip()))
        message_parts.append('')
        message = '\r\n'.join(message_parts)
        print message_parts
        if self.path == "/parseJson.js":
	    response = open("../js/parseJson.js").read()
        elif self.path == "/colossus.json":
            response = createJsonResponse(json_data)
        elif self.path == "/spirentx.jpg":
            response = open("../jpg/spirentx.jpg").read()
        else:
            response = open("../html/colossus_bootstrap.html").read()
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-Length", "%d" % len(response))
        self.end_headers()
        self.wfile.write(response)

    def parse_POST(self):
        """
        helper function to parse POST request
        """
        ctype, pdict = parse_header(self.headers['content-type'])
        if ctype == 'multipart/form-data':
            postvars = parse_multipart(self.rfile, pdict)
        elif ctype == 'application/x-www-form-urlencoded':
            length = int(self.headers['content-length'])
            postvars = parse_qs(
                    self.rfile.read(length),
                    keep_blank_values=1)
        else:
            postvars = {}
        return postvars

    def do_POST(self):
        """
        POST request handler function
        """
        postvars = self.parse_POST()
        response = ""
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-Length", "%d" % len(response))
        self.end_headers ()
        self.wfile.write (response)

class MyTCPServer(SocketServer.TCPServer):
    def server_bind(self):
        """
        set socket options to be reusable
        bind to the server address
        """
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.server_address)

def get_ip_address(ifname):
    """
    get the ip address for admin0
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

HOST, PORT = get_ip_address('admin0'), 40006

Handler = MyHTTPHandler

httpd = MyTCPServer((HOST, PORT), Handler)

print "serving at port", PORT
httpd.serve_forever()
