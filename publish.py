#!/usr/bin/env python

import sys
import socket
import time
import json

def file_to_json(filename):
    """ Convert the input file to nicely formatted JSON. """
    fields = ["time",
              "bid", "bid_depth", "bid_depth_total",
              "offer", "offer_depth", "offer_depth_total"]

    for line in open(filename, "r").readlines()[1:]:
        book_as_dict = dict(zip(fields, line.strip().split()))
        book_as_dict["symbol"] = filename
        yield json.dumps(book_as_dict)


def main(filename):
    # http://stackoverflow.com/questions/603852/multicast-in-python
    multicast_group = '224.1.1.1'
    multicast_port = 5007
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF, socket.inet_aton("127.0.0.1"))

    while True:
        for book in file_to_json(filename):
            assert len(book) == sock.sendto(book, (multicast_group, multicast_port))
            #print json.dumps(book)
            time.sleep(0.2)

if __name__ == "__main__":
    import signal
    def handler(signum, frame): raise KeyboardInterrupt()
    signal.signal(signal.SIGINT, handler)
    try:
        main(sys.argv[1])
    except KeyboardInterrupt:
        pass
