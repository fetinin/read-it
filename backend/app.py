from apistar import App
from apistar_cors import CORSMixin

from readit import settings
from readit.books.routes import routes as book_routes
from readit.components import UserComponent
from readit.db import db_init
from readit.event_hooks import hooks
from readit.sentry import init_sentry
from readit.users.routes import routes as user_routes


class AppCORS(CORSMixin, App):
    pass


routes = book_routes + user_routes
components = [UserComponent()]

app = AppCORS(routes=routes, event_hooks=hooks, components=components)


if __name__ == "__main__":
    db_init()
    if not settings.Server.in_debug:
        init_sentry()
    app.serve(
        settings.Server.host, settings.Server.port, debug=settings.Server.in_debug
    )
