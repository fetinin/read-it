import os


class DB:
    hostname: str = os.environ["DB_HOSTNAME"]
    port: int = int(os.environ["DB_PORT"])
    username = os.environ["DB_USERNAME"]
    password = os.environ["DB_PASSWORD"]


class Secrets:
    jwt_sign = os.environ.get("JWT_SECRET", "test")
    vk_app = os.environ.get("VK_SECRET", "test")
    google_app = os.environ.get("GOOGLE_SECRET", "test")


class Server:
    host = "localhost"
    port = 5000
    in_debug = os.environ.get("APP_DEBUG", False)
