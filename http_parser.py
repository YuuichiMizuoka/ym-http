class HttpParser:

    @staticmethod
    def parse_http_request(request: str):
        request_lines = request.split('\r\n')
        preamble = request_lines[0].split(' ')

        if len(preamble) < 3:
            return "", "", "", None

        method = preamble[0]
        path = preamble[1]
        protocol = preamble[2]

        return method, path, protocol, None
