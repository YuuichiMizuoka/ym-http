
class AuthProvider:

    def is_authorized(self, path, headers):
        pass

    @staticmethod
    def determine_auth_provider(auth_provider):
        if auth_provider[0] == "NO_AUTH":
            return NoAuthProvider()
        if auth_provider[0] == "BASIC":
            return BasicAuthProvider(auth_provider[1])

        raise ValueError("illegal auth provider set")


class BasicAuthProvider(AuthProvider):

    def __init__(self, allowed_basic_values):
        self.allowed_basic_values = allowed_basic_values

    def is_authorized(self, path, headers):
        return True


class NoAuthProvider(AuthProvider):

    def is_authorized(self, path, headers):
        return True
