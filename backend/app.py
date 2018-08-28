from apistar import App

from readit.db import db_init
from readit.routes import routes


app = App(routes=routes)


if __name__ == "__main__":
    db_init()
    app.serve("127.0.0.1", 5000, debug=True)
