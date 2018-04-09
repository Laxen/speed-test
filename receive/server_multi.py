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

    data_storage = open("../data/data_storage_" + str(address[1]), "w", 0)

    started = False
    # size = 0
    while True:
        if not started:
            try:
                (c, a) = sock_ssl.accept()
                started = True
                start_time = time.time()
                print address[1], "New connection", c
            except socket.timeout as e:
                print address[1], "Timed out"
                return -1
        else:
            data = c.recv(8192)
            # size = size + len(data)
            # print address[1], "speed", size / 1000000 / (time.time() - start_time), "MB/s"
            if data == '':
                c.close()
                print address[1], "Connection closed", c
                return time.time() - start_time
            else:
                data_storage.write(data)

port = int(sys.argv[1])
total_time = server((socket.gethostbyname("localhost"), port))

statinfo = os.stat('../data/data_storage_' + str(port))

print port, "speed", statinfo.st_size / 1000000 / total_time, "MB/s"
