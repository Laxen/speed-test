import socket
from socket import AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
import ssl
import select
import cProfile, pstats, sys
import time
import os

KEYFILE = 'server_key.pem'
CERTFILE = 'server_cert.pem'

use_profiling = False

if use_profiling:
    pr = cProfile.Profile()

def server(address):
    sock = socket.socket(AF_INET, SOCK_STREAM)
    sock.bind(address)
    sock.listen(1)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    sock_ssl = ssl.wrap_socket(sock,
            keyfile=KEYFILE,
            certfile=CERTFILE,
            server_side=True)

    potential_readers = [sock_ssl]
    potential_writers = []
    potential_errs = []

    data_storage = open("data_storage", "w", 0)

    started = False
    while True:
        # Break when all clients are finished
        if started and len(potential_readers) == 1:
            end = time.time()
            print "Cleaning up..."
            if use_profiling:
                pr.disable()
            sock_ssl.close()
            data_storage.close()
            return end

        ready_read, ready_write, ready_err = select.select(potential_readers,
                potential_writers, potential_errs)

        for r in ready_read:
            if r == sock_ssl:
                (c, a) = sock_ssl.accept()
                potential_readers.append(c)
                started = True
                print len(potential_readers), "New connection", c
            else:
                data = r.recv(8192)
                if data == '':
                    r.close()
                    potential_readers.remove(r)
                    print len(potential_readers), "Connection closed", r
                else:
                    data_storage.write(data)

if use_profiling:
    pr.enable()

start_time = time.time()
end_time = server((socket.gethostbyname("localhost"), 8082))

if use_profiling:
    ps = pstats.Stats(pr, stream=sys.stdout)
    ps.print_stats()

statinfo = os.stat('data_storage')

print "Time elapsed:", end_time - start_time
print "File size:", statinfo.st_size
print "Speed:", statinfo.st_size / 1000000 / (end_time - start_time), "MB/s"
