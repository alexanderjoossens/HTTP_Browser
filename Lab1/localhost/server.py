import socket
import os
from sys import getsizeof
import threading
import email.utils
from status_codes import *

# make a socket for the server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
hostname = socket.gethostname()
SERVER = socket.gethostbyname(hostname)
print("IP: ", SERVER, "\r\n")

PORT = 5055  # random
HEADER = 4096  # default
LAST_MODIFICATION = datetime(2021, 3, 28)  # last time own webpage has been changed
ADDR = (SERVER, PORT)
server.bind(ADDR)

FORMAT = 'latin-1'
DISCONNECT_MESSAGE = 'DISCONNECT!'


def threaded(conn):
    """
    While the server is threading, it can support multiple clients.
    The function will look for errors and find which HTTP command was sent.
    """
    try:
        while True:

            # receive message from client and check for errors
            msg = conn.recv(HEADER)
            if b"Content-Length" not in msg:
                while b"\r\n\r\n" not in msg:
                    msg += conn.recv(HEADER)
            else:
                for line in msg.split(b"\r\n"):
                    if b"Content-Length" in line:
                        size = []
                        for word in line.split():
                            if word.isdigit():
                                size.append(int(word))
                while getsizeof(msg) < size[0]:
                    msg += conn.recv(HEADER)
            if b"Host" not in msg.split(b"\r\n\r\n")[0]:
                # 400 Bad Request Error
                send_error_400(conn)

            elif not (b"GET" or b"HEAD" or b"POST" or b"PUT" in msg.split(b"\r\n\r\n")[0]):
                # 400 Bad Request Error
                send_error_400(conn)

            elif msg[0:3] == b"GET":  # execute GET
                if not modified_since(msg, LAST_MODIFICATION):
                    get_server(msg, conn)
                else:
                    # 304 Not Modified Error
                    send_error_304(conn)

            elif msg[0:4] == b"HEAD":  # execute HEAD
                if not modified_since(msg, LAST_MODIFICATION):
                    head_server(msg, conn)
                else:
                    # 304 Not Modified Error
                    send_error_304(conn)

            elif msg[0:4] == b"POST":  # execute POST
                post_server(msg, conn)

            elif msg[0:3] == b"PUT":  # execute PUT
                put_server(msg, conn)

            if b"Connection: close" in msg.split(b"\r\n\r\n")[0]:  # close connection
                conn.close()
                return

    except:  # 500 Server Error
        send_error_500(conn)
        conn.close()
        return


def get_server(msg, conn):
    """
    Server uses the given message to execute a GET command and sends a GET response to the client.
    """
    # decode and modify received message from client
    requested_file = msg.decode(FORMAT).split("GET")[1].split("HTTP")[0].lstrip().rstrip()
    if requested_file[-1] == "/":
        requested_file = "index.html"
    else:
        if requested_file[0] == "/":  # if it starts with a slash, just start reading from the second character
            requested_file = requested_file[1:]

    # 404 Not Found Error
    if not os.path.exists("localhost/"+requested_file):
        send_error_404(conn)
        return

    else:
        # send GET response to the client
        current_date = format_date_time(int(mktime(datetime.now().timetuple())))
        page = open("localhost/" + requested_file, "rb")
        webpage = page.read()
        page_size = str(len(webpage))
        page.close()
        last_modification = str(format_date_time(mktime(datetime(2021, 3, 26).timetuple())))
        response = bytes("HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=ISO-8859-1\r\nDate: " + str(current_date)
                         + "\r\nContent-Length: " + page_size + "\r\nLast-Modified: " + last_modification + "\r\n\r\n",
                         encoding=FORMAT) + webpage

        conn.send(response)
        return


def head_server(msg, conn):
    """
    Server uses the given message to execute a HEAD command and sends a HEAD response to the client.
    """
    # decode and modify received message from client
    requested_file = msg.decode(FORMAT).split("HEAD")[1].split("HTTP")[0].lstrip().rstrip()
    if requested_file[-1] == "/":
        requested_file = "index.html"
    else:
        if requested_file[0] == "/":
            requested_file = requested_file[1:]
    # 404 Not Found Error
    if not os.path.exists("localhost/" + requested_file):
        send_error_404(conn)
        return
    else:
        # send HEAD response to the client
        current_date = format_date_time(int(mktime(datetime.now().timetuple())))
        page = open("localhost/" + requested_file, "rb")
        webpage = page.read()
        page_size = str(getsizeof(webpage))
        response = "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=ISO-8859-1\r\nDate: " + str(current_date) + \
                   "\r\nContent-Length: " + page_size + "\r\n\r\n"
        conn.send(response.encode(FORMAT))
        return


def post_server(msg, conn):
    """
    Server uses the given message to execute a POST command and sends a POST response to the client.
    """
    # decode received message from client and retrieve path of the file
    message = msg.decode(FORMAT)
    file_path = "localhost/" + message.split('POST')[1].split('HTTP')[0].rstrip().lstrip()
    client_response = message.split("\r\n\r\n")[1].rstrip().lstrip()

    if not os.path.isfile(file_path):
        # make a new file if it doesn't yet exist
        file = open(file_path, 'w')
        file.write(client_response)
        file.close()
    else:
        # file already exists
        file = open(file_path, 'r')
        text = file.read()
        file.close()
        text = text + "\r\n" + client_response  # append to the text that's already there

        file = open(file_path, 'w')
        file.write(text)
        file.close()

    current_date = format_date_time(mktime(datetime.now().timetuple()))
    response = "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=ISO-8859-1\r\nDate: " +\
        str(current_date) + '\r\nContent-Length: 0'
    conn.send(response.encode(FORMAT))


def put_server(msg, conn):
    """
    Server uses the given message to execute a PUT command and sends a PUT response to the client.
    """
    # decode received message from client and retrieve path of the file
    message = msg.decode(FORMAT)
    file_path = "localhost/" + message.split("PUT")[1].split("HTTP")[0].rstrip().lstrip()

    # # 404 Not Found Error
    # if not os.path.exists(file_path):
    #     send_error_404(conn)
    #     return
    client_response = message.split("\r\n\r\n")[1].rstrip().lstrip()

    # always make a new file
    file = open(file_path, "w")
    file.write(client_response)
    file.close()

    # send response to client
    current_date = format_date_time(mktime(datetime.now().timetuple()))
    response = "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset = ISO-8859-1\r\nDate: " + \
        str(current_date) + "\r\nContent-Length: 0"
    conn.send(response.encode(FORMAT))
    return


def modified_since(msg, last_modification):
    """
    This function checks if the given message was modified since the last modification.
    """
    modified_since_time = [line for line in msg.splitlines() if b"If-Modified-Since" in line]
    if not modified_since_time:  # no "If-Modified-Since" text found
        return False
    modified_since_time = modified_since_time[0].split(b"If-Modified-Since: ", 1)[1].lstrip().rstrip()
    modified_since_time = str(modified_since_time)
    modified_since_time = datetime(*email.utils.parsedate(modified_since_time)[:6])
    if last_modification < modified_since_time:
        return True  # message has been modified since last modification
    else:
        return False  # message has not been modified since last modification


def start():
    """
    Server starts listening and will start threading.
    """
    server.listen()
    while True:
        conn, addr = server.accept()
        print('new connection: ', addr[0], 'connected')
        threading.Thread(target=threaded, args=(conn,)).start()


print("[STARTING] server is threading on port %s ..." % int(PORT))
start()
