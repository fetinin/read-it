import mongoengine
import asyncio


def global_init():
    mongoengine.register_connection(alias="core", name="books_test")
