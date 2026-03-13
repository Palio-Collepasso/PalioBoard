"""ASGI entrypoint used by `fastapi dev`."""

from palio.app.factory import create_app

app = create_app()

__all__ = ["app", "create_app"]
