from __future__ import annotations

import datetime
from typing import Union

from mongoengine import StringField, DateTimeField, ListField, Document, IntField


class Book(Document):
    created_date = DateTimeField(default=datetime.datetime.now)

    title = StringField(max_length=50)
    pages = ListField(StringField())
    author = StringField(max_length=50)
    cover = StringField()
    page_active = IntField(default=1)
    owner_id = StringField(max_length=36)

    meta = {
        "db_alias": "core",
        "collection": "books",
        "indexes": ["created_date", "owner_id"],
    }

    @classmethod
    def get_user_book(cls, id_: str, owner_id: str) -> Union[Book, None]:
        return cls.objects(pk=id_, owner_id=owner_id).first()
