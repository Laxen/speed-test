import socket, ssl
from socket import AF_INET, SOCK_STREAM, IPPROTO_TCP, TCP_NODELAY
from string import ascii_lowercase
import sys
import os
import time
import cProfile, pstats

use_profiling = False

if use_profiling:
    pr = cProfile.Profile()

def client(address):
    sock = socket.socket(AF_INET, SOCK_STREAM)
    sock_ssl = ssl.wrap_socket(sock,
            cert_reqs=ssl.CERT_REQUIRED,
            ca_certs='../certs/server_cert.pem')
    sock_ssl.connect(address)
    sock_ssl.setsockopt(IPPROTO_TCP, TCP_NODELAY, 1)

    for f in os.listdir('../data'):
        start_time = time.time()

        data_storage = open('../data/' + f, "r")
        sock_ssl.write(data_storage.read())

        total_time = time.time() - start_time
        statinfo = os.stat('../data/' + f)
        print f, "speed", statinfo.st_size / 1000000 / total_time, "MB/s"

        data_storage.close()
        os.remove('../data/' + f)

    sock_ssl.close()

if use_profiling:
    pr.enable()

port = int(sys.argv[1])
client((socket.gethostbyname("localhost"), port))

if use_profiling:
    ps = pstats.Stats(pr, stream=sys.stdout)
    ps.print_stats()
