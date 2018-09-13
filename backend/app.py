import os

from apistar import App

from apistar_cors import CORSMixin


from readit.db import db_init
from readit.event_hooks import hooks
from readit.books.routes import routes as book_routes
from readit.users.routes import routes as user_routes
from readit.components import UserComponent


class AppCORS(CORSMixin, App):
    pass


routes = book_routes + user_routes
components = [UserComponent()]

app = AppCORS(routes=routes, event_hooks=hooks, components=components)


if __name__ == "__main__":
    db_init()
    app.serve("127.0.0.1", 5000, debug=os.environ.get("APP_DEBUG", False))
