from apps.application import create_app
from apps.task_app.celery import celery_app  # noqa

flask_app = create_app()
flask_app.app_context().push()
