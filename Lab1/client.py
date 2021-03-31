import socket
import sys
from get_command import get
from head_command import head
from post_command import post
from put_command import put

# retrieve input arguments from the client (command, uri and port)
cmd = sys.argv[1]
uri = sys.argv[2]
if len(sys.argv) - 1 == 3:
    PORT = sys.argv[3]
elif len(sys.argv) - 1 == 2:
    PORT = 80

full_uri = uri
full_uri = full_uri.replace('http://', '') # http has to be removed from the string

# usi ip-address if client connects to 'localhost'
hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)
if ip in uri or "localhost" in uri:  # when connecting to own server -> replace uri (localhost) with IP address
    uri = ip

# create socket
target_host = uri.replace('http://', '')  # http has to be removed from the string
SERVER = socket.gethostbyname(target_host)
ADDR = (SERVER, int(PORT))
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
print("")

if cmd == 'GET':
    get(cmd, target_host, client)
elif cmd == 'HEAD':
    head(cmd, target_host, client)
elif cmd == 'POST':
    post(cmd, full_uri, client)
elif cmd == 'PUT':
    put(cmd, full_uri, client)

client.close()
