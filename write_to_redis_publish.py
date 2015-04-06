#! /usr/bin/env python
import socket
import struct
import redis
import json
from collections import defaultdict

# Assuming messages look like:
# { 'symbol':'AAPL', 'bid_depth': '300', 'offer': '119.45', 'bid': '119.4', 'offer_depth': '300', 'bid_depth_total': '300', 'time': '20150205T012707', 'offer_depth_total': '300' }
SYMBOL = 'symbol'
MULTICAST_GROUP = '224.1.1.1'
MULTICAST_PORT = 5007

class RedisWriter(object):
    def __init__(self, listen_group, listen_port):
        # Setup multicast listener socket
        # http://stackoverflow.com/questions/603852/multicast-in-python
        self.listener = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listener.bind((listen_group, listen_port))
        self.listener.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton(listen_group) + socket.inet_aton("127.0.0.1"))

        self.redis = redis.StrictRedis()

    def publish_book(self, symbol, book):
        self.redis.publish("stocks", json.dumps(book))

    def convert(self, msg):
        try:
            data = json.loads(msg)
            symbol = data[SYMBOL]
            self.publish_book(symbol, data)
        except (ValueError, KeyError) as e: # msg may not be valid json, or fields might not exist
            print str(e)

    def run(self):
        while True:
            data = self.listener.recv(1024 * 4)
            self.convert(data)

def main():
    runner = RedisWriter(MULTICAST_GROUP, MULTICAST_PORT) # TODO args or conf file
    runner.run()

if __name__ == '__main__':
    import signal
    def handler(signum, frame): raise KeyboardInterrupt()
    signal.signal(signal.SIGINT, handler)
    try:
        main()
    except KeyboardInterrupt:
        pass
