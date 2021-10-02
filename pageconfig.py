from auth_provider import AuthProvider

COMMENT_START = "#"


class PageConfig:

    def __init__(self, config_text):
        self.config_text = config_text
        self.config_lines = self._parse_config(config_text)

    def find_configured_line(self, path):
        for config_line in self.config_lines:
            if path.startswith(config_line.path):
                return config_line
        raise ValueError("no valid path configured")

    def _parse_config(self, config_text):
        parsed_config_lines = list()
        for line in config_text.split('\n'):
            if line.startswith(COMMENT_START) or line.strip() == "":
                continue
            parsed_config_lines.append(self._parse_line(line))
        return parsed_config_lines

    def _parse_line(self, line):
        values = list(filter(None, line.replace("\t", " ").split(" ")))
        path = values[0]
        target = values[1]
        return_type = values[2]

        if return_type not in ("FS", "RP"):
            raise ValueError("illegal return type configuration")

        auth_provider = AuthProvider.determine_auth_provider(values[3:])

        return ConfigLine(path, target, return_type, auth_provider)


class ConfigLine:

    def __init__(self, path, target, return_type, auth_provider: AuthProvider):
        self.path = path
        self.target = target
        self.return_type = return_type
        self.auth_provider = auth_provider
