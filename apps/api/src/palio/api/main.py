"""ASGI entrypoint used by `fastapi dev`."""

from palio.bootstrap.factory import create_app

app = create_app()

__all__ = ["app"]
