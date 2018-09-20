import os


class DB:
    hostname: str = os.environ.get("DB_HOSTNAME", "localhost")
    port: int = int(os.environ.get("DB_PORT", 27017))
    username = os.environ.get("DB_USERNAME")
    password = os.environ.get("DB_PASSWORD")


class Secrets:
    jwt_sign = os.environ.get("JWT_SECRET", "test")
    vk_app = os.environ.get("VK_SECRET", "test")
    google_app = os.environ.get("GOOGLE_SECRET", "test")


class Server:
    host = "localhost"
    port = 5000
    in_debug = os.environ.get("APP_DEBUG", False)
