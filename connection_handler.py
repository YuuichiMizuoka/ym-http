from socket import socket

from http_parser import HttpParser
from response import Response, HttpStatus


class ConnectionHandler:

    def __init__(self):
        # TODO: replace with config options
        self.resources = "C:\\Users\\Isaiah\\PycharmProjects\\ym-http\\resources\\"
        self.error_pages = "C:\\Users\\Isaiah\\PycharmProjects\\ym-http\\resources\\error_pages\\"

    def get(self, path) -> Response:
        raise NotImplemented

    def e_500(self) -> Response:
        return Response(b'Internal Server Error', HttpStatus.INTERNAL_SERVER_ERROR)

    def e_405(self) -> Response:
        raise NotImplemented

    def e_404(self) -> Response:
        raise NotImplemented

    def e_401(self) -> Response:
        raise NotImplemented

    def evaluate(self, method, path) -> Response:
        if method == "GET":
            try:
                return self.get(path)
            except FileNotFoundError:
                return self.e_404()
            except PermissionError:
                return self.e_401()
        elif method == "ENKY":
            return Response(b'x3', HttpStatus.OK)
        else:
            return self.e_405()

    def handle_connection(self, connection: socket, client_address):
        try:
            data = connection.recv(2500).decode('utf-8')
            method, path, protocol, headers = HttpParser.parse_http_request(data)
            connection.send(self.evaluate(method, path).to_bytes())
        except Exception as e:  # TODO: find good exceptions
            print(e)
            connection.send(self.e_500().to_bytes())
        finally:
            connection.close()


class DefaultConnectionHandler(ConnectionHandler):

    def __init__(self):
        super().__init__()
        self.home_path = "C:\\Users\\Isaiah\\Desktop\\http\\"

    def e_405(self) -> Response:
        return Response(open(self.error_pages + "405.html", 'rb').read(), HttpStatus.METHOD_NOT_ALLOWED)

    def e_404(self) -> Response:
        return Response(open(self.error_pages + "404.html", 'rb').read(), HttpStatus.NOT_FOUND)

    def e_401(self) -> Response:
        return Response(open(self.error_pages + "401.html", 'rb').read(), HttpStatus.ACCESS_DENIED)

    def get(self, path) -> Response:
        if path == "/":
            path = 'index.html'
        
        return Response(open(self.home_path + path, 'rb').read(), HttpStatus.OK)
