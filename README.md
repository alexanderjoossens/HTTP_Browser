# HTTP_Browser

How to run:

Server
python3 localhost/server.py

Client
GET command example:
python3 client.py GET http://www.tcpipguide.com 80
other possible websites: google.com, linux-ip.net, ...

HEAD command example:
python3 client.py GET http://www.tcpipguide.com 80

POST command example:
python3 client.py POST localhost/file.txt 5055

PUT command example:
python3 client.py PUT localhost/file.txt 5055

You can also open the client in a browser using http://IP:PORT
example: http://192.168.2.7:5055/
