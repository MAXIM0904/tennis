from fastapi import FastAPI
from profile.routers import router
from games.routers import game
from photo.routers import photo

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

app.include_router(
    photo,
    prefix="/add",
    tags=["add"],
    responses={418: {"description": "Teapot"}},
)
