from __future__ import annotations

from collections import namedtuple
import base64
import requests
from enum import IntEnum
from typing import ClassVar, Dict, Type, Tuple, Optional
from readit import settings

User = namedtuple("User", "name surname id avatar")


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
                params={
                    "fields": "photo_50, has_photo",
                    "access_token": self.token,
                    "v": self.api_version,
                },
            ).json()
            user = data["response"][0]
            if user["has_photo"]:
                photo = base64.b64encode(requests.get(user["photo_50"]).content)
            else:
                photo = ""
            self._user = User(
                user["first_name"], user["last_name"], str(user["id"]), photo
            )
        return self._user


class GoogleClient(AuthClientBase):
    service_type = AuthTypes.google

    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.token = self._init_token(code)
        self._user: Optional[User] = None
        self.user_id = self.user.id

    @staticmethod
    def _init_token(code: str) -> Tuple[str, str]:
        resp = requests.post(
            "https://www.googleapis.com/oauth2/v4/token",
            data={
                "code": code,
                "client_id": "114302730103-6mjed5701n57tajalsqk280eg2u11m33.apps.googleusercontent.com",
                "client_secret": settings.Secrets.google_app,
                "redirect_uri": "http://localhost:5000/auth/google",  # todo: получать из вне?
                "grant_type": "authorization_code",
            },
        )
        resp.raise_for_status()
        data = resp.json()
        return data["access_token"]

    @property
    def user(self):
        if self._user is None:
            user = requests.get(
                "https://people.googleapis.com/v1/people/me",
                params={"resourceName": "people/me", "personFields": "names,photos"},
                headers={"Authorization": f"Bearer {self.token}"},
            ).json()
            if user["photos"] and not user["photos"][0].get("default"):
                photo = base64.b64encode(requests.get(user["photos"][0]["url"]).content)
            else:
                photo = ""
            self._user = User(
                name=user["names"][0]["givenName"],
                surname=user["names"][0]["familyName"],
                id=str(user["names"][0]["metadata"]["source"]["id"]),
                avatar=photo,
            )
        return self._user
