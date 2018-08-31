from apistar import App

from apistar_cors import CORSMixin


from readit.db import db_init
from readit.routes import routes


class AppCORS(CORSMixin, App):
    pass


app = AppCORS(routes=routes)


if __name__ == "__main__":
    db_init()
    app.serve("127.0.0.1", 5000, debug=True)
