import datetime

from mongoengine import StringField, DateTimeField, ListField, Document

from .db import global_init

global_init()


class BookMongo(Document):
    created_date = DateTimeField(default=datetime.datetime.now)

    title = StringField()
    content = ListField(StringField())
    author = StringField()

    meta = {"db_alias": "core", "collection": "books"}
