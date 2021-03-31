FORMAT = "latin-1"
HEADER = 4096


def head(command, target_host, client):
    """
    Uses the given command, uri and client to construct a HEAD request that it will send to the server.
    """
    # make and send request to server
    request = command + " / HTTP/1.1\r\nConnection: close\r\nHost:%s\r\n\r\n" % target_host
    client.send(request.encode(FORMAT))

    # receive response from server
    complete_response = ''
    while True:
        response = client.recv(HEADER).decode(FORMAT)
        complete_response += response
        if "\r\n\r\n" in response:
            break
    print(complete_response)
