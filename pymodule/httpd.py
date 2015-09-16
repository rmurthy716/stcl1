import SimpleHTTPServer
import SocketServer
import socket
import fcntl
import struct
import json
import urlparse

class MyHTTPHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    def do_GET (self):
	parsed_path = urlparse.urlparse(self.path)
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
	    response = open("parseJson.js").read()
        elif self.path == "/colossus.json":
            response = open("colossus.json").read()
        elif self.path == "/spirentx.jpg":
            response = open("spirentx.jpg").read()
        else:
            response = open("colossus_bootstrap.html").read()
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-Length", "%d" % len(response))
        self.end_headers ()
        self.wfile.write (response)


class MyTCPServer(SocketServer.TCPServer):
    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.server_address)
    
def get_ip_address(ifname):
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
