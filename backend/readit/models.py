from __future__ import annotations

import datetime
from typing import Union

from mongoengine import StringField, DateTimeField, ListField, Document
from mongoengine import errors as mongoerrors


class Book(Document):
    created_date = DateTimeField(default=datetime.datetime.now)

    title = StringField()
    content = ListField(StringField())
    author = StringField()
    cover = StringField()

    meta = {"db_alias": "core", "collection": "books"}

    @classmethod
    def get_by_id(cls, id_: str) -> Union[Book, None]:
        try:
            return cls.objects.with_id(id_)
        except mongoerrors.ValidationError:
            return None
