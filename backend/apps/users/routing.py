from ..extensions import socketio
from . import consumers

# TODO: get prefix from blueprint
socketio.on_namespace(consumers.UserSelfConsumer('/users'))
socketio.on_error_default(consumers.exception_handler)
