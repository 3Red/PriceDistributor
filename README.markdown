# About

A simple client/server application that takes in stock price data and makes it available to multiple users.

The server reads stock price data from the network via UDP multicast and pushes the data to a redis server.

The clients read stock price data from the redis server via a Webdis HTTP adapter and displays data in webpage.

# Running

To run this application you must first have [Redis](https://github.com/antirez/reids) and [Webdis](https://github.com/nicolasff/webdis) installed and running.  This application expects that the default ports are used.

Next you can upload the website files to the redis.  This can be done by using curl to upload the files through the webdis HTTP interface like below.

<pre>
curl --upload-file stockgrid.html http://127.0.0.1:7379/SET/stockgrid
curl --upload-file main.js http://127.0.0.1:7379/SET/main
curl --upload-file jssub.js http://127.0.0.1:7379/SET/jssub
curl --upload-file jsstring.js http://127.0.0.1:7379/SET/jsstring
curl --upload-file jshash.js http://127.0.0.1:7379/SET/jshash
</pre>

Then you run publish.sh passing in a filename to the command line.  The file should be a tab delimited file containing data similar to below.

<pre>
time	bid	bid_depth	bid_depth_total	offer	offer_depth	offer_depth_total
20150205T011216	47.76	7200	7200	47.78	200	200
20150205T011223	47.76	80	80	47.78	200	200
</pre>

<pre>
./publish.py msft
</pre>

Finally run one of the write_to_redis files and point your browser to http:127.0.0.1:7379/GET/stockgrid.html.

<pre>
./write_to_redis_publish.py
</pre>
