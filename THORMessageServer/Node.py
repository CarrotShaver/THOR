import socket
import sys
from _thread import *

class Node( ip, port ):

    def __init__(self):
        self.host = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    
    def __threaded_client(conn):
        
        while True:
            # Receive 16 bytes of data
            data = conn.recv(16)
            # Choose what to do with it here:
            if not data:
                break
        conn.close()

    def start():
        try:
            sock.bind((host, port))
        except socket.error as error:
            print(str("Error: "+e))

        sock.listen(5)
        print("Socket created, waiting for connection...")

        while True:
            conn, addr = sock.accept()
            print("Received connection to: "+addr[0]+":"+str(addr[1]))

            start_new_thread(__threaded_client, (conn,))