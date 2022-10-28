from fastapi import FastAPI
from profile.routers import router
from games.game.routers import game


app = FastAPI()


app.include_router(
    router,
    prefix="/user",
    tags=["user"],
    responses={418: {"description": "Teapot"}},
)


app.include_router(
    game,
    prefix="/game",
    tags=["game"],
    responses={418: {"description": "Teapot"}},
)
