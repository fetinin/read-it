from app import app
from wsgicors import CORS
from readit import settings
from readit.db import db_init
from readit.sentry import init_sentry

app = CORS(app, headers="*", methods="*", origin="*", maxage="86400")
db_init()
if not settings.Server.in_debug:
    init_sentry()
