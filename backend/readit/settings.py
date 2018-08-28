import os


class CONF:
    class DB:
        hostname: str = os.environ["DB_HOSTNAME"]
        port: int = int(os.environ["DB_PORT"])
