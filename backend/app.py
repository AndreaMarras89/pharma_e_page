"""Main App Logic."""

from fastapi import Depends, FastAPI


from backend.api.routers import router


def create_app() -> FastAPI:
    """Creates the server application with FastAPI."""

    this_app = FastAPI(
        title="be-commerce: ",
    )
    this_app.include_router(
        router,
    )
    return this_app


app = create_app()
