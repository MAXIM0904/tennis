from fastapi import FastAPI
from profile.routers import router
from games.application.routers import application
from games.scores.routers import scores


app = FastAPI()


app.include_router(
    router,
    prefix="/profile",
    tags=["profile"],
    responses={418: {"description": "Teapot"}},
)


app.include_router(
    application,
    prefix="/application",
    tags=["application"],
    responses={418: {"description": "Teapot"}},
)


app.include_router(
    scores,
    prefix="/scores",
    tags=["scores"],
    responses={418: {"description": "Teapot"}},
)
