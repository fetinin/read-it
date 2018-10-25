from molten import App
from wsgicors import CORS

from readit import settings
from readit.books.routes import routes as book_routes
from readit.db import db_init

from readit.users.routes import routes as user_routes
from readit.components import UserComponent

routes = book_routes + user_routes

app = App(routes=routes, components=[UserComponent()])

if __name__ == "__main__":
    import werkzeug

    options = {
        "hostname": settings.Server.host,
        "port": settings.Server.port,
        "use_debugger": True,
        "use_reloader": True,
    }
    db_init()
    cors_app = CORS(app, headers="*", methods="*", origin="*", maxage="86400")
    werkzeug.run_simple(application=cors_app, **options)
