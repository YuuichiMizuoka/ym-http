import os
from socket import socket

from helpers import HttpParser, SocketHelper
from response import Response, INTERNAL_SERVER_ERROR, OK, METHOD_NOT_ALLOWED, NOT_FOUND, ACCESS_DENIED


class ConnectionHandler:

    def __init__(self):
        # TODO: replace with config options
        self.resources = os.path.dirname(os.path.abspath(__file__)) + "\\resources\\"
        self.error_pages = self.resources + "error_pages\\"
        self.max_body = 16384  # 16KiB

    def get(self, path, headers) -> Response:
        raise NotImplemented

    def e_500(self) -> Response:
        return Response(INTERNAL_SERVER_ERROR)

    def e_405(self) -> Response:
        raise NotImplemented

    def e_404(self) -> Response:
        raise NotImplemented

    def e_401(self) -> Response:
        raise NotImplemented

    def evaluate(self, method, path, headers) -> Response:
        if method == "GET":
            try:
                return self.get(path, headers)
            except FileNotFoundError as e:
                print(e)
                return self.e_404()
            except PermissionError:
                return self.e_401()
        else:
            return self.e_405()

    def handle_connection(self, connection: socket, client_address):
        try:
            method, path, headers = self.receive_next_http_request(connection)
            response = self.evaluate(method, path, headers)

            print("{} {} {} ({})".format(client_address, method, path, response.status.status_code))
            connection.send(response.to_bytes())
        except Exception as e:  # TODO: find good exceptions
            print(e)
            connection.send(self.e_500().to_bytes())
        finally:
            connection.close()

    def receive_next_http_request(self, connection: socket):
        preamble = SocketHelper.receive_until_char_sequence(connection, b'\r\n', self.max_body)
        method, path, protocol = HttpParser.parse_preamble(preamble)

        headers = SocketHelper.receive_until_char_sequence(connection, b'\r\n\r\n', self.max_body)
        header_map = HttpParser.parse_headers(headers)

        return method, path, header_map

    def startup_message(self):
        pass


class DefaultConnectionHandler(ConnectionHandler):

    def __init__(self, home_path):
        super().__init__()
        self.home_path = home_path

    def e_405(self) -> Response:
        return Response(METHOD_NOT_ALLOWED, open(self.error_pages + "405.html", 'rb').read())

    def e_404(self) -> Response:
        return Response(NOT_FOUND, open(self.error_pages + "404.html", 'rb').read())

    def e_401(self) -> Response:
        return Response(ACCESS_DENIED, open(self.error_pages + "401.html", 'rb').read())

    def get(self, path, headers) -> Response:
        # TODO: range header
        # TODO: .htaccess
        if path == "/":
            path = 'index.html'

        return Response(OK, open(self.home_path + path, 'rb').read())

    def startup_message(self):
        print("delivering static content from " + self.home_path)
