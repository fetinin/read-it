from app import app
from readit.db import db_init
from readit.sentry import init_sentry

app = app
db_init()
init_sentry()
