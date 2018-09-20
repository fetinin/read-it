import mongoengine

from readit import settings


def db_init():
    params = {
        "username": settings.DB.username,
        "host": settings.DB.hostname,
        "password": settings.DB.password,
        "db_name": "books",
    }
    mongoengine.register_connection(
        host="mongodb+srv://{username}:{password}@{host}/{db_name}"
        "?retryWrites=true".format(**params),
        alias="core",
    )
