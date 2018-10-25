import logging
from inspect import Parameter
from typing import Optional

import jwt
from molten import HTTPError, HTTP_401, HTTP_403, Header

from readit.settings import Secrets

LOGGER = logging.getLogger(__name__)


class User:
    def __init__(self, id_: str) -> None:
        self.id = id_

    @classmethod
    def from_token(cls, token: str):
        data = jwt.decode(token, key=Secrets.jwt_sign)
        return cls(id_=data["userID"])

    def as_token(self):
        return jwt.encode({"userID": self.id}, key=Secrets.jwt_sign)


class UserComponent:
    is_cacheable = True
    is_singleton = False

    def can_handle_parameter(self, parameter: Parameter) -> bool:
        return parameter.annotation is User

    def resolve(self, authentication: Optional[Header]) -> User:
        """
        Determine the user associated with a request
        """
        if authentication is None:
            raise HTTPError(HTTP_401, {"error": "Authorization header is required."})

        try:
            return User.from_token(authentication)
        except Exception as err:
            LOGGER.error(f"Failed to parse token: {err}")
            raise HTTPError(HTTP_403, {"error": "Incorrect token."})
