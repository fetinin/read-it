import os


class DB:
    hostname: str = os.environ["DB_HOSTNAME"]
    port: int = int(os.environ["DB_PORT"])


class Secrets:
    jwt_sign = os.environ.get("JWT_SECRET", "test")
    vk_app = os.environ.get("VK_SECRET", "test")
