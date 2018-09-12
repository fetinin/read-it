import mongoengine

from readit import settings


def db_init():
    mongoengine.register_connection(
        host=settings.DB.hostname,
        port=settings.DB.port,
        alias="core",
        name="books_test",
    )
