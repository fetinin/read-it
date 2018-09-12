from __future__ import annotations

import datetime

from mongoengine import StringField, DateTimeField, Document, IntField


class User(Document):
    created_date = DateTimeField(default=datetime.datetime.now)

    name = StringField(max_length=50, required=True)
    surname = StringField(max_length=50)
    avatar = StringField()
    external_id = StringField(required=True)
    auth_type = IntField(required=True)

    meta = {"db_alias": "core", "collection": "users"}

    @classmethod
    def find_external(cls, external_id: str, auth_type: int):
        return cls.objects(external_id=external_id, auth_type=auth_type).first()
