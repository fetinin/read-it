import logging

import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration

sentry_logging = LoggingIntegration(level=logging.INFO, event_level=logging.ERROR)


def init_sentry():
    sentry_sdk.init(
        "https://ff7c3869bf9c466590df3c95fa070dcd@sentry.io/1290604",
        integrations=[sentry_logging],
    )
    print("Sentry configured")
