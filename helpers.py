from socket import socket


class HttpParser:

    @staticmethod
    def parse_preamble(preamble):
        if preamble is None:
            raise ValueError("http preamble is empty")

        sp_preamble = preamble.split(' ')
        if len(sp_preamble) != 3:
            return

        method = sp_preamble[0]
        path = sp_preamble[1]
        protocol = sp_preamble[2]
        return method, path, protocol

    @staticmethod
    def validate_http_preamble(preamble):
        if "/.." in preamble or "../" in preamble:
            raise ValueError("invalid characters in preamble (possible backtracking attack)")

        if "%7F" in preamble or "%7f" in preamble:
            raise ValueError("invalid characters in preamble")

    @staticmethod
    def parse_headers(headers: str):
        pass


class SocketHelper:

    @staticmethod
    def receive_until_char_sequence(connection: socket, seq: bytes, max_length: int):
        data = b''
        cnt = 0
        while True:
            data += connection.recv(1)
            cnt += 1

            if seq in data:
                break

            if cnt > max_length:
                break

        data.replace(seq, b'')
        return data.decode('utf-8')

    @staticmethod
    def parse_headers(headers):
        pass
