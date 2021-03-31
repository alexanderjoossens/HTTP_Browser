from sys import getsizeof
FORMAT = "latin-1"
HEADER = 4096


def post(command, uri, client):
    """
    Uses the given command, uri and client to construct a POST request that it will send to the server.
    """
    # ask the client for a string
    message = input('Enter a string: ')

    # make and send a request to the server
    size = getsizeof(message)
    target_host = uri.replace('http://', '') # uri -> target_host -> file_path -> request
    file_path = target_host.split('/', 1)[1]
    target_host = target_host.split('/')[0]
    request = command + " " + file_path + " HTTP/1.1\r\nConnection: close\r\nHost: " + target_host + \
        "\r\nContent-Length: " + str(size) + "\r\n\r\n" + message
    client.send(request.encode(FORMAT))
    # print("[POST request sent]")
