#! /usr/bin/env python
import socket
import struct
import redis
import json
import time
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
        self.listener.bind(('', listen_port))
        mreq = struct.pack("4sl", socket.inet_aton(listen_group), socket.INADDR_ANY)
        self.listener.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        self.listener.settimeout(0.01)

        self.redis = redis.StrictRedis()

        self.expire = 2
        self.refresh_interval = 1
        self.next_refresh = time.time()
        self.publish_interval = 0.05
        self.next_pub = time.time()

        self.changed_books = {}

        self.market_data_key = "stocks"

    def publish_book(self, symbol, book):
        print "hset", symbol
        self.redis.hset(self.market_data_key, symbol, json.dumps(book))

    def publish_changed_books(self):
        if self.changed_books:
            print "hmset"
            json_books = { k:json.dumps(v) for k,v in self.changed_books.iteritems() }
            self.redis.hmset(self.market_data_key, json_books)
            self.changed_books.clear()

    def update_expire(self):
        print "expire"
        self.redis.expire(self.market_data_key, self.expire)

    def check_actions(self):
        now = time.time()
        if now > self.next_pub:
            self.publish_changed_books()
            self.next_pub = now + self.publish_interval
        if now > self.next_refresh:
            self.update_expire()
            self.next_refresh = now + self.refresh_interval

    def convert(self, msg):
        try:
            data = json.loads(msg)
            symbol = data[SYMBOL]
            self.changed_books[symbol] = data
        except (ValueError, KeyError) as e: # msg may not be valid json, or fields might not exist
            print str(e)

    def run(self):
        while True:
            try:
                data = self.listener.recv(1024)
                self.convert(data)
            except socket.timeout:
                pass
            self.check_actions()

def main():
    runner = RedisWriter(MULTICAST_GROUP, MULTICAST_PORT) # TODO args or conf file
    runner.run()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
