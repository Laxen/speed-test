import socket, ssl
from socket import AF_INET, SOCK_STREAM, IPPROTO_TCP, TCP_NODELAY
from random import randint, choice
from string import ascii_lowercase
import cProfile

def spammer():
    sock = socket.socket(AF_INET, SOCK_STREAM)
    sock_ssl = ssl.wrap_socket(sock,
            cert_reqs=ssl.CERT_REQUIRED,
            ca_certs='server_cert.pem')
    sock_ssl.connect(('127.0.0.1', 8082))
    sock_ssl.setsockopt(IPPROTO_TCP, TCP_NODELAY, 1)

    lis = list(ascii_lowercase)
    for i in range(0, 100000):
        inp = ascii_lowercase * 300
        sock_ssl.write(inp)

    sock_ssl.close()

cProfile.run('spammer()')
