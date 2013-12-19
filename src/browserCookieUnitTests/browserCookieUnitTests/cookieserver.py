#!/usr/bin/env python
import BaseHTTPServer
import sys
import urlparse


class WebRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path.startswith('/set/header/set-cookie'):
            self.send_response(200, 'OK')
            query = urlparse.parse_qs(urlparse.urlparse(self.path).query)
            cookie = query.get('cookie', None)
            if cookie is not None:
                self.send_header('Set-Cookie', cookie[0])
            self.end_headers()
            self.wfile.write("<p>The header has been set.</p>")
            self.finish()
        else:
            self.send_error(500)

PORT = int(sys.argv[1])
server = BaseHTTPServer.HTTPServer(('localhost', PORT), WebRequestHandler)
scheme = 'http'

print 'Starting server on %s://localhost:%d/' % (scheme, PORT)

server.serve_forever()
