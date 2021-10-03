import os
from socket import socket

from helpers import HttpParser, SocketHelper
from pageconfig import PageConfig
from response import Response, INTERNAL_SERVER_ERROR, OK, METHOD_NOT_ALLOWED, NOT_FOUND, NOT_AUTHORIZED


class ConnectionHandler:

    def __init__(self):
        # TODO: replace with config options
        self.project_folder = os.path.dirname(os.path.abspath(__file__)) + os.sep
        self.error_pages = self.project_folder + "resources" + os.sep + "error_pages" + os.sep
        self.max_body = 16384  # 16KiB

    def get(self, path, headers) -> Response:
        raise NotImplemented

    def unknown_http_method(self, method, path, headers) -> Response:
        return self.e_405()

    def e_405(self) -> Response:
        return Response(METHOD_NOT_ALLOWED, open(self.error_pages + "405.html", 'rb').read())

    def e_404(self) -> Response:
        return Response(NOT_FOUND, open(self.error_pages + "404.html", 'rb').read())

    def e_401(self, additional_headers=[]) -> Response:
        return Response(NOT_AUTHORIZED, open(self.error_pages + "401.html", 'rb').read(), additional_headers)

    def e_500(self) -> Response:
        return Response(INTERNAL_SERVER_ERROR, open(self.error_pages + "500.html", 'rb').read())

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

        headers = SocketHelper.receive_until_char_sequence(connection, b'\r\n\r\n', self.max_body - len(preamble))
        header_map = HttpParser.parse_headers(headers)

        HttpParser.validate_http_preamble(preamble)

        return method, path, header_map

    def evaluate(self, method, path, headers) -> Response:
        try:
            self.evaluate_firewall(method, path, headers)
        except PermissionError:
            return self.e_401(["WWW-Authenticate: Basic " + path])

        try:
            return self.evaluate_http_method(method, path, headers)
        except FileNotFoundError as e:
            print(e)
            return self.e_404()
        except PermissionError:
            return self.e_401()

    def evaluate_firewall(self, method, path, headers):
        pass

    def evaluate_http_method(self, method, path, headers) -> Response:
        if method == "GET":
            return self.get(path, headers)
        else:
            return self.unknown_http_method(method, path, headers)

    def startup_message(self):
        pass


class ConfiguredConnectionHandler(ConnectionHandler):

    def __init__(self, config=None):
        super().__init__()

        if config is None:
            config = self.read_config()
        self.page_config = PageConfig(config)
        self.list_dir = True

    def read_config(self):
        return open(self.project_folder + "conf" + os.sep + "ym-http.conf", 'rb').read().decode("utf-8")

    def startup_message(self):
        print("delivering static content: ")
        for c in self.page_config.config_lines:
            print("\t\"" + c.path + "\" mapped to \"" + c.target + "\"")

    def get(self, path, headers) -> Response:
        path = path.replace("%20", " ")  # TODO: better (real) http path encoding decoder

        config_line = self.page_config.find_configured_line(path)
        file_path = config_line.target + path.replace(config_line.path, '', 1)

        if os.path.isdir(file_path):
            return self._create_directory_response(path, file_path)

        if os.path.isfile(file_path):
            return self._create_file_response(file_path)

        raise FileNotFoundError("No such file or directory: " + file_path)

    def unknown_http_method(self, method, path, headers) -> Response:
        return self.e_405()

    def evaluate_firewall(self, method, path, headers):
        config_line = self.page_config.find_configured_line(path)
        if not config_line.auth_provider.is_authorized(path, headers):
            raise PermissionError("auth provider not authorized")

    def _create_directory_response(self, path, file_path):
        if os.path.isfile(self.join_paths(file_path, "index.html")):
            return self._create_file_response(self.join_paths(file_path, "index.html"))

        if self.list_dir:
            return self._create_folder_listing_response(path, file_path)

        raise PermissionError("folder listing disabled")

    def _create_file_response(self, file_path):
        return Response(OK, open(file_path, 'rb').read())

    def _create_folder_listing_response(self, path, folder_path):
        dir_listing = os.listdir(folder_path)

        dir_listing_html = b'<html><meta charset="utf-8"><body>Directory Listing: <br>'
        for file_name in dir_listing:
            file_name_b = bytes(file_name, 'utf-8')

            link_path = self.join_paths(path, file_name)
            link_path_b = bytes(link_path, 'utf-8')

            dir_listing_html += b'<a href="' + link_path_b + b'">' + file_name_b + b'</a><br>'

        dir_listing_html += b'</body></html>'
        return Response(OK, dir_listing_html)

    def join_paths(self, path1, path2):
        if path1.endswith('/'):
            return path1 + path2
        return path1 + '/' + path2
