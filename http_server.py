import socket

from connection_handler import ConnectionHandler


class HttpServer:

    def __init__(self, server_address, connection_handler: ConnectionHandler):
        self.server_address = server_address
        self.connection_handler = connection_handler
        self.startup_server()

    def setup_socket(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create a new socket (AF_INET = internet protocol)
        sock.bind(self.server_address)  # bind the socket to the given port/address
        sock.listen(1)  # start listening to connections
        return sock

    def startup_server(self):
        sock = self.setup_socket()

        print("serving ym-http on {}:{}".format(self.server_address[0], self.server_address[1]))
        self.connection_handler.startup_message()
        
        # main connection loop TODO: add some simple threading
        while True:
            connection, client_addr = sock.accept()
            self.connection_handler.handle_connection(connection, client_addr)
