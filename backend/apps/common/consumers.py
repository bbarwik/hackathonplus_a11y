import logging
import typing

from flask_socketio import (
    Namespace,
    SocketIO,
    join_room,
    leave_room,
    rooms,
)

IterableOfDecorators = typing.Iterable[typing.Callable]
logger = logging.getLogger(__name__)


class SocketIOConsumer(Namespace):
    event_decorators: typing.Union[
        None,
        typing.Mapping[str, IterableOfDecorators],
        IterableOfDecorators,
    ] = None

    def _set_socketio(self, socketio: SocketIO) -> None:
        super()._set_socketio(socketio)
        exception_handler = getattr(self, 'exception_handler', None)
        if exception_handler:
            self.socketio.on_error(self.namespace)(exception_handler)

    def trigger_event(self, event: str, *args: typing.Any) -> typing.Any:
        event_handler = getattr(self, f'on_{event}', None)
        if not event_handler:
            # there is no handler for this event, so we ignore it
            logger.warning(
                f'Missing "{event}" handler for namespace: "{self.namespace}"',
            )
            return
        # apply decorators
        self.event_decorators = self.event_decorators or []
        if isinstance(self.event_decorators, typing.Mapping):
            decorators = self.event_decorators.get(event.lower(), [])
        else:
            decorators = self.event_decorators
        for decorator in decorators:
            event_handler = decorator(event_handler)
        return self.socketio._handle_event(
            event_handler,
            event,
            self.namespace,
            *args,
        )

    def join_room(
            self,
            room: str,
            sid: typing.Optional[str] = None,
            namespace: typing.Optional[str] = None,
    ) -> None:
        join_room(room, sid, namespace or self.namespace)

    def leave_room(
            self,
            room: str,
            sid: typing.Optional[str] = None,
            namespace: typing.Optional[str] = None,
    ) -> None:
        leave_room(room, sid, namespace or self.namespace)

    @property
    def rooms(self) -> typing.Iterable[str]:
        return rooms(namespace=self.namespace)
