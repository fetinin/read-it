import mongoengine

from readit.settings import CONF


def db_init():
    mongoengine.register_connection(
        host=CONF.DB.hostname, port=CONF.DB.port, alias="core", name="books_test"
    )
