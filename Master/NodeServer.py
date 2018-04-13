from http.server import BaseHTTPRequestHandler, HTTPServer
import requests, random, string, urllib.parse
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from sys import argv

class Node(BaseHTTPRequestHandler):
    # Variables for Message handling
    ip = str(argv[1])
    port = str(argv[2])
    # stringFrom = ip+":"+port # Use if IP is implemented
    stringFrom = port
    stringTo = "" # Use to construct the post request first argument
    data = {
        "to": 0,
        "from": stringFrom,
        "message": ""
    }
    lastTo = "" # Variable to keep track of last node posted to
    lastFrom = "" # Variable to keep track of last node posted from
    # Variables for RSA
    code = None
    key = None
    encrypted_key = None
    public_key = None

    def code_gen(self, size):
        self.code = "".join(random.choices(
            string.ascii_letters + string.digits,
            k = size
        ))
        # Create code_gen file based on IP here

    def key_gen(self):
        self.code = self.code_gen(128)
        self.key = RSA.generate(2048)
        self.encrypted_key = self.key.exportKey(
            format = "PEM",
            passphrase = self.code,
            pkcs = 8,
            protection="scryptAndAES128-CBC"
        )
        
        priv_key = ("%s_key.pem" %(self.port))
        private_out = open(priv_key, "wb") # Create private key file
        private_out.write(self.encrypted_key) # Write private key to file

        pub_key = ("%s_pub.pem" %(self.port))
        public_out = open(pub_key, "wb") # Create public key file
        public_out.write(self.key.publickey().exportKey(format="PEM"))

    def get_key(self, filename): # server
        self.encrypted_key = open(filename, "rb").read()
        self.key = RSA.import_key(
            self.encrypted_key,
            passphrase = self.code
        )
        return self.key
        # Change to return a key object instead of setting global key variable
    
    def get_public(self, filename):
        public_key = RSA.import_key(open(filename).read()) # Creates public_key object
        return public_key # Returns the object, *use file.write(public.exportKey())

    def parse_dict_data(self, post_data):
        keys = post_data.split("&")
        self.lastTo = keys[0].partition("=")[2]
        self.lastFrom = keys[1].partition("=")[2]
        for x in range(0, len(keys)):
            keys[x] = keys[x].split("=")
        return keys
        # insert message deconstruction into dictionary object here

    def _send_pub_key(self):
        self.key_gen()
        pub_key = ("%s_pub.pem" %(self.port))
        print("Sending public key...\n",(self.get_public(pub_key)).exportKey(format="PEM").decode("utf-8"))
        self.send_response(200, "Request Successful")
        self.send_header("Content-type", "text/html")
        self.end_headers()
        pub_str = (self.get_public(pub_key)).exportKey(format="PEM")
        self.wfile.write(pub_str)

    # This is where the magic happens boys
    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length).decode("utf-8")
        post_data = urllib.parse.unquote_plus(post_data)
        
        
        # Parse Keys
        keys = self.parse_dict_data(post_data)
        print("Received:",keys)
        # If Key Request
        print (keys[2][1])
        if( keys[2][1] == "keyrequest"):
            self._send_pub_key()

def run(server_class=HTTPServer, handler_class=Node, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print("Starting HTTP Server on port", port)
    print("Server is alert and ready for work:")
    httpd.serve_forever()

if __name__ == "__main__":

    if len(argv) == 3:
        run(port=int(argv[2]))
    else:
        print("Not enough arguments: Expected arg[1]:IP, arg[2]:port")
        exit(0)