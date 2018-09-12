from __future__ import annotations

from collections import namedtuple

import requests
from enum import IntEnum
from typing import ClassVar, Dict, Type, Tuple, Optional
from readit import settings

User = namedtuple("User", "name surname id")


class AuthTypes(IntEnum):
    vk = 0
    google = 1
    github = 2

    @classmethod
    def options(cls):
        return [v.name for v in cls]


class AuthClient:
    _clients: Dict[AuthTypes, Type[AuthClientBase]] = {}

    def __init__(self, service: AuthTypes, code: str):
        self._client = self._clients[service](code)

    def __getattr__(self, item):
        return getattr(self._client, item)

    @classmethod
    def add_client(cls, client_type: AuthTypes, client: Type[AuthClientBase]):
        cls._clients[client_type] = client


class AuthClientBase:
    service_type: ClassVar[AuthTypes]

    def __init__(self, code: str) -> None:
        self.code = code
        self.user_id: str
        self.token: str
        self.user: User

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        AuthClient.add_client(cls.service_type, cls)


class VKClient(AuthClientBase):
    service_type = AuthTypes.vk
    api_version: ClassVar[str] = "5.84"

    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.user_id, self.token = self._init_token(code)
        self._user: Optional[User] = None

    @staticmethod
    def _init_token(code: str) -> Tuple[str, str]:
        resp = requests.get(
            "https://oauth.vk.com/access_token",
            params={
                "client_id": 6684417,
                "client_secret": settings.Secrets.vk_app,
                "redirect_uri": "http://localhost:5000/auth/vk",  # todo: получать из вне?
                "code": code,
            },
        )
        resp.raise_for_status()
        data = resp.json()
        return str(data["user_id"]), data["access_token"]

    @property
    def user(self):
        if self._user is None:
            data = requests.get(
                "https://api.vk.com/method/users.get",
                params={"access_token": self.token, "v": self.api_version},
            ).json()
            user = data["response"][0]
            self._user = User(user["first_name"], user["last_name"], str(user["id"]))
        return self._user
