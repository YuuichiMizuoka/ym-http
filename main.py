# This is a simple HTTP server implementation done by YM

from connection_handler import DefaultConnectionHandler
from http_server import HttpServer

SERVER_ADDRESS = ('localhost', 42000)


def main():
    default_connection_handler = DefaultConnectionHandler()
    HttpServer(SERVER_ADDRESS, default_connection_handler)


if __name__ == "__main__":
    main()
