from urllib.parse import urlencode, urljoin

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
            "response_type": "code",
            "v": "5.84",
        },
    },
    "google": {
        "url": "https://accounts.google.com/o/oauth2/v2/auth",
        "query": {
            "client_id": "114302730103-6mjed5701n57tajalsqk280eg2u11m33.apps.googleusercontent.com",
            "scope": "https://www.googleapis.com/auth/userinfo.profile",
            "response_type": "code",
            "include_granted_scopes": "true",
            "access_type": "online",
        },
    },
    "github": {
        "url": "https://github.com/login/oauth/authorize",
        "query": {"client_id": "ac99328569221f9822bc", "scope": "read:user"},
    },
}


def auth_user(auth_service_name: str, code: http.QueryParam, route_url: http.URL):
    route_url = route_url.split("?")[0]
    if not code and auth_service_name != AuthTypes.guest.name:
        # redirect to oauth service
        try:
            auth_params: dict = OAUTH_URLS[auth_service_name]
        except KeyError:
            raise NotFound()
        auth_query_params = auth_params["query"].copy()
        auth_query_params["redirect_uri"] = route_url
        query = urlencode(auth_query_params)
        return redirect(f"{auth_params['url']}?{query}")

    try:
        auth_type = AuthTypes[auth_service_name]
    except KeyError:
        raise BadRequest(f"Invalid auth type. Must be one of {AuthTypes.options()}")

    auth_client = AuthClient(auth_type, code, route_url)
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
    return redirect(f"{settings.Server.frontend_server_url}/authenticated?{query}")


def get_user(user: components.User) -> schema.User:
    user_db = User.objects.with_id(user.id)
    return schema.User(
        id=str(user_db.id),
        name=user_db.name,
        surname=user_db.surname,
        avatar=user_db.avatar,
    )
