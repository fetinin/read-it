from __future__ import annotations

import datetime
from typing import Union

from mongoengine import StringField, DateTimeField, ListField, Document, IntField
from mongoengine import errors as mongoerrors


class Book(Document):
    created_date = DateTimeField(default=datetime.datetime.now)

    title = StringField(max_length=50)
    pages = ListField(StringField())
    author = StringField(max_length=50)
    cover = StringField()
    page_active = IntField(default=1)

    meta = {"db_alias": "core", "collection": "books"}

    @classmethod
    def get_by_id(cls, id_: str) -> Union[Book, None]:
        try:
            return cls.objects.with_id(id_)
        except mongoerrors.ValidationError:
            return None
