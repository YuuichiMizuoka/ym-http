from http_status import HttpStatus

PROTOCOL = 'HTTP/1.1'


class Response:

    def __init__(self, body: bytes, status: HttpStatus):
        self.headers = b''
        self.body = body
        self.status = status

    def to_bytes(self) -> bytes:
        preamble = bytes(PROTOCOL + str(self.status.status_code) + " " + self.status.reason_message, 'UTF-8')
        return preamble + b'\r\n' + self.headers + b'\r\n' + self.body
