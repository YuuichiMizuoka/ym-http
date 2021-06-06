# This is a simple HTTP server implementation done by YM
import os
import sys

# "C:\\Users\\Isaiah\\Desktop\\http\\"
from connection_handler import DefaultConnectionHandler
from http_server import HttpServer

SERVER_ADDRESS = ('localhost', 42000)


def validate_path(path):
    if not os.path.isdir(path):
        raise ValueError(path + " must be a valid directory")


def determine_home_path():
    if len(sys.argv) > 1:
        potential_path = sys.argv[1]
    else:
        potential_path = os.getcwd() + "\\http\\"

    validate_path(potential_path)
    return potential_path


def main():
    # the default connection handler just delivers files out of the given directory
    default_connection_handler = DefaultConnectionHandler(determine_home_path())
    HttpServer(SERVER_ADDRESS, default_connection_handler)


if __name__ == "__main__":
    main()
