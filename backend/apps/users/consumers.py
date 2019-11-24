import functools
import typing

from flask import request

from flask_jwt_extended import (
    current_user,
    verify_jwt_in_request,
)
from flask_jwt_extended.exceptions import JWTExtendedException
from flask_socketio import (
    ConnectionRefusedError,
    disconnect,
    send,
)
from jwt.exceptions import PyJWTError

from apps.common.consumers import SocketIOConsumer


# TODO: move to common
def authenticated_only(event_handler: typing.Callable) -> typing.Callable:
    """Check if valid access token is passed via headers.

    Raises
    ------
    ConnectionRefusedError
        when token missin or invalid in `Authorization` header

    """

    @functools.wraps(event_handler)
    def wrapper(*args: typing.Any, **kwargs: typing.Any) -> typing.Any:
        try:
            verify_jwt_in_request()
        # `IndexError` is raised when there is empty token sent in
        # the `Authorization` header, precisely: "Bearer "
        except (JWTExtendedException, PyJWTError, IndexError) as exc:
            raise ConnectionRefusedError(
                # this message will be sent on `error` event
                {
                    'detail': 'authentication',
                    'message': 'Missing or invalid access token',
                },
            )
        return event_handler(*args, **kwargs)

    return wrapper


class UserSelfConsumer(SocketIOConsumer):
    event_decorators = {'connect': [authenticated_only]}
    # Use list of decorators to apply them on every event handler:
    # event_decorators = [authenticated_only]

    def on_connect(self) -> None:
        # TODO: verify if it works like expected
        # only `connect` event requires authentication so `current_user`
        # is set to authenticated `User` instance only in the context of
        # this event, so we retrieve this `User` instance and store it
        # in instance variable so it can be accessed in any other events.
        self.user = current_user._get_current_object()
        self.send(
            {'message': f'hello {self.user.email}!'},
            room=request.sid,
        )

    def on_disconnect(self) -> None:
        self.send(
            {'message': f'bye bye {self.user.email}! :('},
            room=request.sid,
        )

    def on_message_from_client(self, data: typing.Dict[str, typing.Any]) -> None:
        self.emit(
            'response_on_message_from_client',
            {'message': 'Response from the server!'},
            room=request.sid,
        )

    def exception_handler(self, exception: Exception) -> None:
        print(
            f'Exception handler of `{self.namespace}`.\nException '
            f'{type(exception)} - "{exception}".\nMessage: '
            f'"{request.event["message"]}", args: "{request.event["args"]}".'
        )
        raise exception


def exception_handler(exception: Exception) -> None:
    print(f'Default exception handler for {type(exception)} - "{exception}"')
    raise exception
