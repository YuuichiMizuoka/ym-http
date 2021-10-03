# This is a simple HTTP server implementation done by YM
import os
import sys

from connection_handler import ConfiguredConnectionHandler
from http_server import HttpServer

SERVER_ADDRESS = ('localhost', 42000)


def validate_path(path):
    if not os.path.isdir(path):
        raise ValueError(path + " must be a valid directory")


def determine_config():
    if len(sys.argv) <= 1:
        return None

    potential_path = sys.argv[1]

    if not potential_path.endswith(os.sep):
        potential_path = potential_path + os.sep

    validate_path(potential_path)
    return "/ " + potential_path + " FS NO_AUTH"


def main():
    # The configuration connection handler delivers static content based on a given configuration
    # none -> configuration found in /conf/ym-http.conf will be used
    configured_connection_handler = ConfiguredConnectionHandler(determine_config())
    HttpServer(SERVER_ADDRESS, configured_connection_handler)


if __name__ == "__main__":
    main()
