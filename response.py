PROTOCOL = 'HTTP/1.1'
SP = " "


class HttpStatus:

    def __init__(self, status_code: int, reason_message: str):
        self.status_code = status_code
        self.reason_message = reason_message


class Response:

    def __init__(self, status: HttpStatus, body: bytes = b'', headers: [str] = []):
        self.headers = headers
        self.body = body
        self.status = status

    def to_bytes(self) -> bytes:
        byte_headers = b'Server: ym-http\r\n'

        for header in self.headers:
            byte_headers += bytes(header, "UTF-8") + b'\r\n'

        preamble = bytes(PROTOCOL + SP + str(self.status.status_code) + SP + self.status.reason_message, 'UTF-8')
        return preamble + b'\r\n' + byte_headers + b'\r\n' + self.body


# HTTP STATUS CODES
OK = HttpStatus(200, "OK")

NOT_AUTHORIZED = HttpStatus(401, "Not Authorized")
FORBIDDEN = HttpStatus(403, "Forbidden")
NOT_FOUND = HttpStatus(404, "Not Found")
METHOD_NOT_ALLOWED = HttpStatus(405, "Method Not Allowed")

INTERNAL_SERVER_ERROR = HttpStatus(500, "Internal Server Error")
