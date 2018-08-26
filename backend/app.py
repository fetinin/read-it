from apistar import App, Route
from readit.routes import routes


app = App(routes=routes)


if __name__ == "__main__":
    app.serve("127.0.0.1", 5000, debug=True)
