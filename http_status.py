class HttpStatus:

    def __init__(self, status_code: int, reason_message: str):
        self.status_code = status_code
        self.reason_message = reason_message


# HTTP STATUS CODES
OK = HttpStatus(200, "OK")

ACCESS_DENIED = HttpStatus(401, "Access Denied")
NOT_FOUND = HttpStatus(404, "Not Found")
METHOD_NOT_ALLOWED = HttpStatus(405, "Method Not Allowed")

INTERNAL_SERVER_ERROR = HttpStatus(500, "Internal Server Error")
