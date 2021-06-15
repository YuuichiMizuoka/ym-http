import os
from socket import socket

from helpers import HttpParser, SocketHelper
from response import Response, INTERNAL_SERVER_ERROR, OK, METHOD_NOT_ALLOWED, NOT_FOUND, NOT_AUTHORIZED


class ConnectionHandler:

    def __init__(self):
        # TODO: replace with config options
        self.project_folder = os.path.dirname(os.path.abspath(__file__)) + os.sep
        self.error_pages = self.project_folder + "resources" + os.sep + "error_pages" + os.sep
        self.max_body = 16384  # 16KiB

    def get(self, path, headers) -> Response:
        raise NotImplemented

    def e_405(self) -> Response:
        return Response(METHOD_NOT_ALLOWED, open(self.error_pages + "405.html", 'rb').read())

    def e_404(self) -> Response:
        return Response(NOT_FOUND, open(self.error_pages + "404.html", 'rb').read())

    def e_401(self) -> Response:
        return Response(NOT_AUTHORIZED, open(self.error_pages + "401.html", 'rb').read())

    def e_500(self) -> Response:
        return Response(INTERNAL_SERVER_ERROR)

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

        headers = SocketHelper.receive_until_char_sequence(connection, b'\r\n\r\n', self.max_body - len(preamble))
        header_map = HttpParser.parse_headers(headers)

        return method, path, header_map

    def startup_message(self):
        pass


class ConfiguredConnectionHandler(ConnectionHandler):

    def __init__(self, config=None):
        super().__init__()

        if config is None:
            config = self.read_config()
        self.page_config = self.parse_config(config)
        self.list_dir = True

    def read_config(self):
        return open(self.project_folder + "conf" + os.sep + "ym-http.conf", 'rb').read().decode("utf-8")

    def parse_config(self, config):
        config = config.replace("\r", "").split("\n")

        parsed_config = dict()
        for line in config:
            delimiter_index = line.index(":")
            http_path = line[:delimiter_index]
            dir_path = line[delimiter_index + 1:]

            # simple way of making the path work for both unix and windows, no matter how you enter it
            dir_path = dir_path.replace("\\", os.sep).replace("/", os.sep)

            parsed_config[http_path] = dir_path

        return parsed_config

    def startup_message(self):
        print("delivering static content: ")
        for c in self.page_config.keys():
            print("\t\"" + c + "\" mapped to \"" + self.page_config[c] + "\"")

    def get(self, path, headers) -> Response:
        path = path.replace("%20", " ")  # TODO: better (real) http path encoding decoder

        for configured_path in self.page_config.keys():
            if path.startswith(configured_path):
                # TODO: better replace (e.g. index.html vs order structure)
                new_path = path.replace(configured_path, '', 1)

                file_path = self.page_config[configured_path] + new_path

                if os.path.isdir(file_path):
                    return self._create_directory_response(file_path)

                if os.path.isfile(file_path):
                    return self._create_file_response(file_path)

                raise FileNotFoundError("No such file or directory: " + file_path)

        raise FileNotFoundError

    def _create_directory_response(self, file_path):
        if os.path.isfile(file_path + "index.html"):
            return self._create_file_response(file_path + "index.html")

        if self.list_dir:
            return self._create_folder_listing_response(file_path)

        raise PermissionError("folder listing disabled")

    def _create_file_response(self, file_path):
        return Response(OK, open(file_path, 'rb').read())

    def _create_folder_listing_response(self, folder_path):
        dir_listing = os.listdir(folder_path)

        dir_listing_html = b'<html><meta charset="utf-8"><body>Directory Listing: <br>'
        for file in dir_listing:
            f = bytes(file, 'utf-8')
            dir_listing_html += b'<a href="./' + f + b'">' + f + b'</a><br>'

        dir_listing_html += b'</body></html>'
        return Response(OK, dir_listing_html)
