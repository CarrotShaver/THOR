from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import requests
from Crypto.PublicKey import RSA


class Node(BaseHTTPRequestHandler):
    

    def generate_keys(self):
        return
        

    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_POST(self):
        # content_length = int(self.headers["Content-Length"])
        # post_data = str(self.rfile.read(content_length))
        # self._set_headers()
        # print(post_data[2:-1])

        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length).decode("utf-8")
        post_data = urllib.parse.unquote_plus(post_data)
        self._set_headers()
        print(post_data)

def run(server_class=HTTPServer, handler_class=Node, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print("Starting HTTP Server on port", port)
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()