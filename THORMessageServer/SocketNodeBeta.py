import socket
import sys
from _thread import *
from Crypto.Cipher import AES # Used to create AES encrypted message
from Crypto.Hash import SHA256 # Used to convert a message into a 16 bit hash

class Node( ip, port, key ):
    
    def decrypt( key, data ):
        self.key = key
        
        chunksize = 64*1024
        outputtxt = data[11:]

        with open(data, "rb") as inmessage:
            messagesize = int(inmessage.read(16))
            IV = inmessage.read(16)

            decryptor = AES.new(key, AES.MODE_CBC, IV)

            with open("decryptedmsg", "wb") as outmessage:
                while True:
                    chunk = inmessage.read(chunksize)
                    
                    if len(chunk) == 0:
                        break

                    outmessage.write(decryptor.decrypt(chunk))
                outmessage.truncate(messagesize) # Removes padding from encryption

    def send_data ( data ):
        # TODO: function should be called from threaded_client
    
    def threaded_client(conn):
        
        while True:
            # Receive data
            data = conn.recv(4096)
            # Choose what to do with it here:
            print(data)

            if not data:
                break
        conn.close()

    def start():
        try:
            sock.bind((host, port))
        except socket.error as error:
            print(str("Error: "+ e))

        sock.listen(5)
        print("Socket created, waiting for connection...")

        while True:
            conn, addr = sock.accept()
            print("Received connection to: "+addr[0]+":"+str(addr[1]))

            start_new_thread( threaded_client, (conn,))

    def __init__(self):
        self.host = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.start()
    
    