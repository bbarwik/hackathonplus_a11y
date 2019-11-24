import typing

from flask import (
    Response,
    request,
)
from flask.views import MethodView

IterableOfDecorators = typing.Iterable[typing.Callable]

class APIView(MethodView):
    method_decorators: typing.Union[
        typing.Mapping[str, IterableOfDecorators],
        IterableOfDecorators,
    ] = []

    def dispatch_request(
            self,
            *args: typing.Any,
            **kwargs: typing.Any,
    ) -> Response:
        # Taken from flask and flask-restful
        # noinspection PyUnresolvedReferences
        method = getattr(self, request.method.lower(), None)
        # If the request method is HEAD and we don't have a handler for it
        # retry with GET.
        if method is None and request.method == 'HEAD':
            method = getattr(self, 'get', None)

        assert method is not None, f'Unimplemented method {request.method}'

        if isinstance(self.method_decorators, typing.Mapping):
            decorators = self.method_decorators.get(request.method.lower(), [])
        else:
            decorators = self.method_decorators

        for decorator in decorators:
            method = decorator(method)

        return method(*args, **kwargs)
