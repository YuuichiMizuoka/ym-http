from socket import socket


class HttpParser:

    @staticmethod
    def parse_preamble(preamble: str):
        if preamble is None:
            raise

        sp_preamble = preamble.split(' ')
        if len(sp_preamble) != 3:
            return

        method = sp_preamble[0]
        path = sp_preamble[1]
        protocol = sp_preamble[2]
        return method, path, protocol

    @staticmethod
    def parse_headers(headers: str):
        pass


class SocketHelper:

    @staticmethod
    def receive_until_char_sequence(connection: socket, seq: str, max_length: int):
        data = ""
        cnt = 0
        while True:
            data += connection.recv(1).decode('utf-8')
            cnt += 1

            if seq in data:
                break

            if cnt > max_length:
                break

        data.replace(seq, '')
        return data

    @staticmethod
    def parse_headers(headers):
        pass
