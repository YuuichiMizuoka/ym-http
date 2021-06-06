from enum import Enum

PROTOCOL = 'HTTP/1.1'


class HttpStatus(Enum):
    OK = (200, "OK")

    ACCESS_DENIED = (401, "Access Denied")
    NOT_FOUND = (404, "Not Found")
    METHOD_NOT_ALLOWED = (405, "Method Not Allowed")

    INTERNAL_SERVER_ERROR = (500, "Internal Server Error")

    def status_code(self) -> int:
        return self.value[0]

    def reason_message(self) -> str:
        return self.value[1]


class Response:
    
    def __init__(self, body: bytes, status: HttpStatus):
        self.headers = b''
        self.body = body
        self.status = status

    def to_bytes(self) -> bytes:
        preamble = bytes(PROTOCOL + str(self.status.status_code()) + " " + self.status.reason_message(), 'UTF-8')
        return preamble + b'\r\n' + self.headers + b'\r\n' + self.body


class ResponseBuilder:

    def __init__(self):
        self.body = b''
        self.reason_message = b''
        self.http_status = b'200'

    def with_body(self, body):
        self.body = body
        return self

    def with_status(self, status: HttpStatus):
        self.http_status = status

    def build(self) -> Response:
        return Response()
