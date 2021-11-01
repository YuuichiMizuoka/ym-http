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
        header_list = headers.split('\r\n')
        header_map = {}

        for header_entry in header_list:
            if header_entry == '':
                continue

            split_header = header_entry.split(': ')
            header_map[split_header[0]] = split_header[1]

        return header_map


class UrlParser:

    @staticmethod
    def decode_url(url: str):
        return UrlParser.decode_utf8_encoded_characters(url)

    @staticmethod
    def decode_utf8_encoded_characters(url: str):
        while UrlParser._has_utf8_segment(url):
            encoded_segment = UrlParser._get_next_utf8_segment(url)
            decoded_segment = UrlParser._decode_utf8_segment(encoded_segment)
            url = url.replace(encoded_segment, decoded_segment)
        return url

    @staticmethod
    def _has_utf8_segment(url: str):
        return "%" in url

    @staticmethod
    def _get_next_utf8_segment(url: str):
        utf_8_segment_start = UrlParser._get_start_of_next_utf_segment(url)
        utf_8_segment_end = UrlParser._get_end_of_next_utf8_segment(url)
        return url[utf_8_segment_start:utf_8_segment_end]

    @staticmethod
    def _get_start_of_next_utf_segment(url: str):
        return url.index("%")

    @staticmethod
    def _get_end_of_next_utf8_segment(url: str):
        utf_8_segment_end = UrlParser._get_start_of_next_utf_segment(url) + 3
        while utf_8_segment_end < len(url) and url[utf_8_segment_end] == "%":
            utf_8_segment_end += 3
        return utf_8_segment_end

    @staticmethod
    def _decode_utf8_segment(utf8_segment: str):
        segment_without_encoder = utf8_segment.replace('%', '')
        return bytes.fromhex(segment_without_encoder).decode('UTF-8')


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
