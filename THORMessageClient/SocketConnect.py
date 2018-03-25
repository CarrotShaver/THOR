import socket

s = socket.socket()
port = 8000
host = "127.0.0.1"

s.connect((host, port))

while True:
    print(s.recv(1024))
    msg = input().encode("ascii")
    s.sendall(msg)

s.close()