from http import HTTPStatus
from urllib.parse import urlencode

import jwt
from apistar import http
from apistar.exceptions import BadRequest
from apistar.http import Response

from readit import settings
from readit.users.auth import AuthClient, AuthTypes
from . import schema
from .models import User


def auth_user(auth_service_name: str, code: http.QueryParam, path: http.Path):
    try:
        auth_type = AuthTypes[auth_service_name]
    except KeyError:
        raise BadRequest(f"Invalid auth type. Must be one of {AuthTypes.options()}")

    auth_client = AuthClient(auth_type, code)
    user = User.find_external(auth_client.user_id, auth_type.value)
    if not user:
        user = User(
            name=auth_client.user.name,
            surname=auth_client.user.surname,
            external_id=auth_client.user.id,
            auth_type=auth_type.value,
        )
        user.save()
    token = jwt.encode({"userID": str(user.id)}, key=settings.Secrets.jwt_sign)
    query = urlencode({"access_token": token.decode("utf-8")})
    return Response(
        b"",
        status_code=HTTPStatus.SEE_OTHER,
        headers={"Location": f"http://localhost:8080/authenticated?{query}"},
    )


def get_user(user_id: str) -> schema.User:
    user = User.objects.with_id(user_id)
    return schema.User(id=str(user.id), name=user.name, surname=user.surname)
