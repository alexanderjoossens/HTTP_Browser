from time import mktime
from datetime import datetime
from wsgiref.handlers import format_date_time
FORMAT = 'latin-1'


def send_200(conn):  # this one isn't used but hardcoded (easier for filling in concrete values)
    """
    Sends a 200 OK message.
    """
    current_date = format_date_time(mktime(datetime.now().timetuple()))
    msg_200 = "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=latin-1\r\nDate: " + str(current_date) + \
              "\r\nContent-Length: 0\r\nConnection: Closed\r\n"
    print("200")
    conn.send(msg_200.encode(FORMAT))


def send_error_400(conn):
    """
    Sends a 400 Bad Request message.
    """
    current_date = format_date_time(mktime(datetime.now().timetuple()))
    msg_400 = "HTTP/1.1 400 Bad Request\r\nContent-Type: text/html; charset=latin-1\r\nDate: " + str(current_date) + \
              "\r\nContent-Length: 0\r\nConnection: Closed\r\n"
    print("error 400")
    conn.send(msg_400.encode(FORMAT))


def send_error_404(conn):
    """
    Sends a 404 Not Found message.
    """
    current_date = format_date_time(mktime(datetime.now().timetuple()))
    msg_404 = "HTTP/1.1 404 Not Found\r\nContent-Type: text/html; charset=latin-1\r\nDate: " + str(current_date) + \
              "\r\nContent-Length: 0\r\nConnection: Closed\r\n"
    print("error 404")
    conn.send(msg_404.encode(FORMAT))


def send_error_304(conn):
    """
    Sends a 304 Not Modified message.
    """
    current_date = format_date_time(mktime(datetime.now().timetuple()))
    msg_304 = "HTTP/1.1 304 Not Modified\r\nContent-Type: text/html; charset=latin-1\r\nDate: " + str(current_date) + \
              "\r\nContent-Length: 0\r\nConnection: Closed\r\n"
    print("error 304")
    conn.send(msg_304.encode(FORMAT))


def send_error_500(conn):
    """
    Sends a 500 Server Error message.
    """
    current_date = format_date_time(mktime(datetime.now().timetuple()))
    msg_500 = "HTTP/1.1 500 Server Error\r\nContent-Type: text/html; charset=latin-1\r\nDate: " + str(current_date) + \
              "\r\nContent-Length: 0\r\nConnection: Closed\r\n"
    print("error 500")
    conn.send(msg_500.encode(FORMAT))
