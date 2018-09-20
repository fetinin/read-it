from urllib.parse import urlencode

import jwt
from apistar import http
from apistar.exceptions import BadRequest, NotFound

from readit import components, settings
from readit.helpers import redirect
from readit.users.auth import AuthClient, AuthTypes
from . import schema
from .models import User

OAUTH_URLS = {
    "vk": {
        "url": "https://oauth.vk.com/authorize",
        "query": {
            "client_id": "6684417",
            "display": "page",
            "redirect_uri": "http://localhost:5000/auth/vk",
            "response_type": "code",
            "v": "5.84",
        },
    },
    "google": {
        "url": "https://accounts.google.com/o/oauth2/v2/auth",
        "query": {
            "client_id": "114302730103-6mjed5701n57tajalsqk280eg2u11m33.apps.googleusercontent.com",
            "scope": "https://www.googleapis.com/auth/userinfo.profile",
            "redirect_uri": "http://localhost:5000/auth/google",
            "response_type": "code",
            "include_granted_scopes": "true",
            "access_type": "online",
        },
    },
}


def auth_user(auth_service_name: str, code: http.QueryParam):
    if not code:
        # redirect to oauth service
        try:
            auth_path = OAUTH_URLS[auth_service_name]
        except KeyError:
            raise NotFound()
        query = urlencode(auth_path["query"])
        return redirect(f"{auth_path['url']}?{query}")

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
            avatar=auth_client.user.avatar,
        )
        user.save()
    token = jwt.encode({"userID": str(user.id)}, key=settings.Secrets.jwt_sign)
    query = urlencode({"access_token": token.decode("utf-8")})
    return redirect(f"http://localhost:8080/authenticated?{query}")


def get_user(user: components.User) -> schema.User:
    user_db = User.objects.with_id(user.id)
    return schema.User(
        id=str(user_db.id),
        name=user_db.name,
        surname=user_db.surname,
        avatar=user_db.avatar,
    )
