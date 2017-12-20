import rollbar
from sanic.exceptions import SanicException
from sanic.handlers import ErrorHandler

__version__ = '0.1.0'


class RollbarHandler(ErrorHandler):
    """
    A subclass of built-in Sanic exception handle, sending data to Rollbar
    """

    def default(self, request, exception):
        if not issubclass(type(exception), SanicException):
            rollbar.report_exc_info(request=request)
        return super().default(request, exception)


def _hook(request, data):
    data['framework'] = 'sanic'

    if request:
        data['context'] = str(request.url)


class SanicRollbar:
    """
    A "plugin" to automatically configure Rollbar and connect Sanic app to custom error handler.
    """

    def __init__(self, app=None, ignore_exc=None):
        self.handler = None
        self.ignore_exc = ignore_exc or []
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        ignored = [(exc, 'ignored') for exc in self.ignore_exc]
        rollbar.init(
            app.config['ROLLBAR_TOKEN'],
            environment=app.config.get('ROLLBAR_ENV', 'dev'),
            # root=os.path.dirname(os.path.realpath(__file__)),
            allow_logging_basic_config=False,
            exception_level_filters=ignored,
            # **self.init_kwargs
        )
        rollbar.BASE_DATA_HOOK = _hook

        self.handler = RollbarHandler()
        app.error_handler = self.handler


__all__ = [SanicRollbar]
