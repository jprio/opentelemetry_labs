from collections import namedtuple
from urllib.parse import urlparse


class DSN:
    def __init__(self, dsn="", scheme="", host="", port="", project_id="", token=""):
        self.str = dsn
        self.scheme = scheme
        self.host = host
        self.port = port
        self.project_id = project_id
        self.token = token

    def __str__(self):
        return self.str

    @property
    def app_addr(self):
        if self.host == "uptrace.dev":
            return f"{self.scheme}://app.uptrace.dev"
        return f"{self.scheme}://{self.host}:14318"

    @property
    def otlp_http_addr(self):
        if self.host == "uptrace.dev":
            return "https://otlp.uptrace.dev"
        return f"{self.scheme}://{self.host}:{self.port}"

    @property
    def otlp_grpc_addr(self):
        if self.host == "uptrace.dev":
            return "https://otlp.uptrace.dev:4317"
        return f"{self.scheme}://{self.host}:{self.port}"


def parse_dsn(dsn: str) -> DSN:
    if dsn == "":
        raise ValueError("either dsn option or UPTRACE_DSN is required")

    o = urlparse(dsn)
    if not o.scheme:
        raise ValueError(f"can't parse DSN={dsn}")

    host = o.hostname
    if not host:
        raise ValueError(f"DSN={dsn} does not have a host")
    if host == "api.uptrace.dev":
        host = "uptrace.dev"

    if host != "uptrace.dev":
        return DSN(dsn=dsn, scheme=o.scheme, host=host, port=o.port)

    project_id = remove_prefix(o.path, "/")
    if not project_id:
        raise ValueError(f"DSN={dsn} does not have a project id")

    token = o.username
    if not token:
        raise ValueError(f"DSN={dsn} does not have a token")

    return DSN(
        dsn=dsn,
        scheme=o.scheme,
        host=host,
        port=o.port,
        project_id=project_id,
        token=token,
    )


def remove_prefix(s: str, prefix: str) -> str:
    return s[len(prefix):] if s.startswith(prefix) else s
