
class AuthProvider:

    def is_authorized(self, path, headers):
        pass

    @staticmethod
    def determine_auth_provider(auth_provider):
        if auth_provider == "NO_AUTH":
            return NoAuthProvider()
        if auth_provider == "BASIC":
            return BasicAuthProvider()

        raise ValueError("illegal auth provider set")


class BasicAuthProvider(AuthProvider):

    def is_authorized(self, path, headers):
        return True


class NoAuthProvider(AuthProvider):

    def is_authorized(self, path, headers):
        return True
