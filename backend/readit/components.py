import logging

import jwt

from apistar import exceptions, http
from apistar.server.components import Component
from readit.settings import Secrets

logger = logging.getLogger(__name__)


class User(object):
    def __init__(self, id_: str) -> None:
        self.id = id_


class UserComponent(Component):
    def resolve(self, authentication: http.Header) -> User:
        """
        Determine the user associated with a request
        """
        if authentication is None:
            raise exceptions.HTTPException("Authorization header is required.", 401)

        try:
            return self.get_user(authentication)
        except Exception as err:
            logger.error(f"Failed to parse token: {err}")
            raise exceptions.Forbidden("Incorrect token.")

    def get_user(self, token: str) -> User:
        data = jwt.decode(token, key=Secrets.jwt_sign)
        return User(id_=data["userID"])
