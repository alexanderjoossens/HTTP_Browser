from bs4 import BeautifulSoup
import os
import sys
HEADER = 4096
FORMAT = 'latin-1'


def get(command, target_host, client):  # every site works but jmarshall.com moved permanently and tldp.org too
    """
    Uses the given command, uri and client to construct a GET request that it will send to the server.
    It will also go over all the found images and send a GET request for them.
    It will store the HTML body and all images in a directory with the name of the target host.
    """
    # make and send request to server
    request = command + " / HTTP/1.1\r\nHost: %s\r\n\r\n" % target_host  # no "Connection: close" (still GET things)
    print(request)
    client.send(request.encode(FORMAT))  # latin-1 because utf-8 didn't work
    complete_response = ''

    # receive answer from server (with or without 'Content-Length')
    while True:
        chunk = client.recv(HEADER).decode(FORMAT)

        if "Content-Length:" in chunk:  # (other websites) with Content-Length in chunk: receive until this length
            for line in chunk.split("\r\n"):
                if "Content-Length" in line:
                    # print('line ', line)
                    size = [int(word) for word in line.split() if word.isdigit()]
                    # print('size: ', size)
            complete_response += chunk
            while len(complete_response.encode(FORMAT)) < size[0]:
                complete_response += client.recv(HEADER).decode(FORMAT)
            break

        else:  # websites without "Content-Length" like google.com: last chunk contains '0\r\n\r\n'
            complete_response += chunk
            if chunk.endswith("0\r\n\r\n"):
                break
    print(complete_response)
    body = complete_response.split("\r\n\r\n")[1]
    # print('Complete Response: ', '\r\n', complete_response, '\r\n', ' end complete response')

    # save html body in a file
    path = target_host  # name of the directory = www.google.com (= target_host)
    if not os.path.exists(path):
        os.makedirs(path)
    name = target_host + '/' + target_host + ".html"  # name of the file inside the directory = www.google.com.html
    f = open(name, "w")
    f.write(body)
    f.close()

    # get all images from html body
    images = []
    soup = BeautifulSoup(complete_response, 'html.parser')
    for img in soup.findAll('img'):
        images.append((img.get('src')))

    # send GET request for every image
    for image in images:
        if not ("http" in image):  # use existing connection
            if image[0] != "/":
                image = "/" + image
            target_host_image = target_host.replace("http://", "") + image
            request = "GET " + image + " HTTP/1.1\r\nHost:%s\r\n\r\n" % target_host
            client.send(request.encode(FORMAT))
        response = client.recv(HEADER)
        complete_response = b''

        if b"Content-Length" in response:
            for line in response.split(b"\r\n"):
                if b"Content-Length" in line:
                    size = [int(word) for word in line.decode(FORMAT).split() if word.isdigit()]
            complete_response += response.split(b"\r\n\r\n")[1]
            while sys.getsizeof(complete_response) < size[0]:
                complete_response += client.recv(HEADER)

        # save image in a file
        if os.path.split(image)[0] == "":  # necessary if the image is stored in the same folder as the webpage
            image_path = image
        elif os.path.split(image)[0] != "/":
            image_path = target_host_image
        else:
            image_path = target_host_image
        head_tail = os.path.split(image_path)
        if not os.path.exists(head_tail[0]) and head_tail[0] != "":
            os.makedirs(head_tail[0])
        image_file = open(target_host_image, "wb")
        image_file.write(complete_response)
        image_file.close()

        # replace path of the image in the html body
        body_file = open(name, "rt")
        body = body_file.read()
        if image[0] == "/":
            body = body.replace(image, image[1:])
            image = image[1:]
        if "%" in image:  # Not allowed in linux
            body = body.replace(image, image.replace("%", ""))
        body_file.close()
        body_file = open(name, "wt")
        body_file.write(body)
        body_file.close()
