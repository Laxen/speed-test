import socket
from socket import AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
import ssl
import time
import os
import sys

KEYFILE = '../certs/server_key.pem'
CERTFILE = '../certs/server_cert.pem'

def server(address):
    sock = socket.socket(AF_INET, SOCK_STREAM)
    sock.bind(address)
    sock.listen(1)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    sock_ssl = ssl.wrap_socket(sock,
            keyfile=KEYFILE,
            certfile=CERTFILE,
            server_side=True)
    sock_ssl.settimeout(5)

    started = False
    while True:
        if not started:
            try:
                (c, a) = sock_ssl.accept()
                started = True
                print address[1], "New connection", c
            except socket.timeout as e:
                print address[1], "Timed out"
                return -1
        else:
            data = c.recv(8192)
            if data == '':
                c.close()
                print address[1], "Connection closed", c
                return


port = int(sys.argv[1])
total_time = server((socket.gethostbyname("localhost"), port))

