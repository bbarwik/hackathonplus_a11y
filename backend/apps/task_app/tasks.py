from celery import current_app


@current_app.task(bind=True)
def debug_task(self) -> None:
    print(f'Request: {self.request!r}')  # pragma: no cover
