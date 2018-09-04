import logging

from apistar import http

logger = logging.getLogger(__name__)


class ErrorHandlingHook:
    def on_error(self, response: http.Response):
        logger.exception("An unhandled error was raised")


hooks = [ErrorHandlingHook]
