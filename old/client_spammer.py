import socket, ssl
from socket import AF_INET, SOCK_STREAM, IPPROTO_TCP, TCP_NODELAY
from random import randint
from string import ascii_lowercase

def spammer():
    sock = socket.socket(AF_INET, SOCK_STREAM)
    sock_ssl = ssl.wrap_socket(sock,
            cert_reqs=ssl.CERT_REQUIRED,
            ca_certs='server_cert.pem')
    sock_ssl.connect(('127.0.0.1', 8082))
    sock_ssl.setsockopt(IPPROTO_TCP, TCP_NODELAY, 1)

    for i in range(0, 600000):
        inp = ascii_lowercase * 50 # 1300 bytes
        sock_ssl.write(inp)

    # Total write: 780 MB

    sock_ssl.close()

spammer()
