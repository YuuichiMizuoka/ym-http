import hmac


class AuthProvider:

    def is_authorized(self, path, headers):
        pass

    @staticmethod
    def determine_auth_provider(auth_provider):
        if auth_provider[0] == "NO_AUTH":
            return NoAuthProvider()
        if auth_provider[0] == "BASIC":
            return BasicAuthProvider(''.join(auth_provider[1:]))

        raise ValueError("illegal auth provider set")


class BasicAuthProvider(AuthProvider):

    def __init__(self, past_auth_config):
        self.allowed_basic_values = past_auth_config.replace('[', '').replace(']', '').replace(' ', '').split(',')

    def is_authorized(self, path, headers):
        if "Authorization" not in headers:
            return False

        header_content = headers["Authorization"]
        auth_type, auth_value = header_content.split(" ")

        if not auth_type == "Basic":
            return False

        auth_value_bytes = bytes(auth_value, 'UTF-8')
        for allowed_basic_value in self.allowed_basic_values:
            allowed_basic_value_bytes = bytes(allowed_basic_value, 'UTF-8')

            if hmac.compare_digest(auth_value_bytes, allowed_basic_value_bytes):
                return True
        return False


class NoAuthProvider(AuthProvider):

    def is_authorized(self, path, headers):
        return True
