import importlib
import logging

import flask

from typing_extensions import Final

BLUEPRINT_RELATIVE_IMPORTS: Final = (
    ('.urls', '.views'),
    ('.models',),
    ('.routing', '.consumers'),
    ('.hooks',),
    ('.exceptions',),
)
logger: logging.Logger = logging.getLogger(__name__)


def import_blueprint(blueprint_path: str) -> flask.Blueprint:
    blueprint_module_path, *blueprint_name = blueprint_path.rsplit(':', 1)
    blueprint_module = importlib.import_module(blueprint_module_path)
    if blueprint_name:
        return getattr(blueprint_module, blueprint_name[0])
    for name, object_ in blueprint_module.__dict__.items():
        if isinstance(object_, flask.Blueprint):
            return object_


def register_blueprint(flask_app: flask.Flask, blueprint_path: str) -> None:
    blueprint = import_blueprint(blueprint_path)
    with flask_app.app_context():
        for relative_modules in BLUEPRINT_RELATIVE_IMPORTS:
            for relative_module in relative_modules:
                try:
                    importlib.import_module(
                        relative_module,
                        blueprint.import_name,
                    )
                except ModuleNotFoundError:
                    logger.info(
                        f'Cannot find `{blueprint.import_name}'
                        f'.{relative_module}` module. Skipping..'
                    )
                else:
                    break
    flask_app.register_blueprint(blueprint)
