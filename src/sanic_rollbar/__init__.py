import os

import rollbar
from sanic import Sanic
from sanic.exceptions import SanicException
from sanic.handlers import ErrorHandler

__version__ = '0.1.0'


class RollbarHandler(ErrorHandler):

    def default(self, request, exception):
        # Here, we have access to the exception object
        # and can do anything with it (log, send to external service, etc)

        # Some exceptions are trivial and built into Sanic (404s, etc)
        if not issubclass(type(exception), SanicException):
            rollbar.report_exc_info(request=request)

        # Then, we must finish handling the exception by returning
        # our response to the client
        # For this we can just call the super class' default handler
        return super().default(request, exception)


class SanicRollbar:
    def __init__(self, app=None, ignore_exc=None):
        self.app = None
        self.handler = None
        self.client = None
        self.ignore_exc = ignore_exc or []
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Sanic):
        self.app = app

        ignored = [(exc, 'ignored') for exc in self.ignore_exc]
        rollbar.init(
            app.config['ROLLBAR_TOKEN'],
            environment=app.config.get('ROLLBAR_ENV', 'dev'),
            root=os.path.dirname(os.path.realpath(__file__)),
            allow_logging_basic_config=False,
            exception_level_filters=ignored,
            # **self.init_kwargs
        )

        def _hook(request, data):
            data['framework'] = 'sanic'

            if request:
                data['context'] = str(request.url_rule)

        rollbar.BASE_DATA_HOOK = _hook

        self.handler = RollbarHandler()
        app.error_handler = self.handler
