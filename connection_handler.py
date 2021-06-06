from socket import socket

from http_parser import HttpParser


class ConnectionHandler:

    def __init__(self):
        # TODO: replace with config options
        self.resources = "C:\\Users\\Isaiah\\PycharmProjects\\ym-http\\resources\\"
        self.error_pages = "C:\\Users\\Isaiah\\PycharmProjects\\ym-http\\resources\\error_pages\\"

    def get(self, path) -> bytes:
        raise NotImplemented

    def e_500(self):
        return b'HTTP/1.1 500 Internal Server Error \r\n\r\nInternal Server Error'

    def e_405(self) -> bytes:
        raise NotImplemented

    def e_404(self) -> bytes:
        raise NotImplemented

    def e_401(self) -> bytes:
        raise NotImplemented

    def evaluate(self, method, path) -> bytes:
        if method == "GET":
            try:
                return self.get(path)
            except FileNotFoundError:
                return self.e_404()
            except PermissionError:
                return self.e_401()
        elif method == "ENKY":
            return b'HTTP/1.1 200 OK \r\n\r\n x3'
        else:
            return self.e_405()

    def handle_connection(self, connection: socket, client_address):
        try:
            data = connection.recv(2500).decode('utf-8')
            method, path, protocol, headers = HttpParser.parse_http_request(data)
            connection.send(self.evaluate(method, path))
        except Exception as e:  # TODO: find good exceptions
            print(e)
            connection.send(self.e_500())
        finally:
            connection.close()


class DefaultConnectionHandler(ConnectionHandler):

    def __init__(self):
        super().__init__()
        self.home_path = "C:\\Users\\Isaiah\\Desktop\\http\\"

    def e_405(self) -> bytes:
        return b'HTTP/1.1 405 Method Not Allowed \r\n\r\n' + open(self.error_pages + "405.html", 'rb').read()

    def e_404(self) -> bytes:
        return b'HTTP/1.1 404 Not Found \r\n\r\n' + open(self.error_pages + "404.html", 'rb').read()

    def e_401(self) -> bytes:
        return b'HTTP/1.1 401 Access Denied \r\n\r\n' + open(self.error_pages + "401.html", 'rb').read()

    def get(self, path) -> bytes:
        if path == "/":
            path = 'index.html'

        return b'HTTP/1.1 200 OK \r\n\r\n' + open(self.home_path + path, 'rb').read()
