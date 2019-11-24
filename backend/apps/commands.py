from flask.cli import (
    get_debug_flag,
    pass_script_info,
    run_command,
)

import click


@click.command()
@click.option(
    '--host',
    '-h',
    default='127.0.0.1',
    help='The interface to bind to.',
)
@click.option('--port', '-p', default=5000, help='The port to bind to.')
@pass_script_info
def run_socketio(info, host, port):
    app = info.load_app()
    if 'socketio' not in app.extensions:
        # flask-socketio is installed, but it isn't in this application
        # so we invoke Flask's original run command
        run_index = sys.argv.index('run_socketio')
        sys.argv = sys.argv[run_index:]
        return run_command()
    socketio = app.extensions['socketio']
    socketio.run(app, host=host, port=port)
